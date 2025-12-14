#!/usr/bin/env python3
"""
Living Paper Reviewer Interface v0.5

A lightweight Flask app for external reviewers to verify claims against evidence.
Follows QDR/AJPS verification methodology.

Usage:
    python reviewer_app.py [--port 5000] [--db path/to/lp_public.sqlite] [--entities path/to/entities.yaml]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from functools import wraps

from flask import Flask, render_template_string, request, jsonify, g

# Import redactor (optional)
try:
    from redact import EntityRedactor
    HAS_REDACTOR = True
except ImportError:
    HAS_REDACTOR = False
    EntityRedactor = None

app = Flask(__name__)

# Configuration
DB_PATH = None  # Set via command line or default
REDACTOR = None  # Optional entity redactor

def get_db():
    """Get database connection for current request."""
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Close database connection at end of request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def now() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def redact_text(text: str) -> str:
    """Apply redaction if redactor is configured."""
    if REDACTOR and text:
        return REDACTOR.redact(text)
    return text

# =============================================================================
# API Routes
# =============================================================================

@app.route('/api/papers')
def api_papers():
    """List all papers in the database."""
    db = get_db()
    papers = db.execute("""
        SELECT p.paper_id, p.title,
               COUNT(DISTINCT c.claim_id) as claim_count,
               COUNT(DISTINCT e.evidence_id) as evidence_count
        FROM paper p
        LEFT JOIN claim c ON c.paper_id = p.paper_id
        LEFT JOIN evidence e ON e.paper_id = p.paper_id
        GROUP BY p.paper_id
        ORDER BY p.paper_id
    """).fetchall()
    return jsonify([dict(p) for p in papers])

@app.route('/api/papers/<paper_id>/claims')
def api_claims(paper_id):
    """Get all claims for a paper with their evidence links."""
    db = get_db()
    claims = db.execute("""
        SELECT claim_id, paper_id, claim_type, text, confidence, status,
               verification_status, verified_by, verified_at,
               informant_coverage, contradicting_count, saturation_note, prevalence_basis
        FROM claim
        WHERE paper_id = ?
        ORDER BY claim_id
    """, (paper_id,)).fetchall()

    result = []
    for c in claims:
        # Get evidence links
        links = db.execute("""
            SELECT l.evidence_id, l.relation, l.weight, l.note, l.analytic_note,
                   l.verification_status, l.verified_by, l.verified_at,
                   e.summary, e.sensitivity_tier, e.evidence_type
            FROM claim_evidence_link l
            JOIN evidence e ON e.evidence_id = l.evidence_id
            WHERE l.claim_id = ?
            ORDER BY
                CASE l.weight
                    WHEN 'central' THEN 1
                    WHEN 'supporting' THEN 2
                    ELSE 3
                END,
                l.relation
        """, (c['claim_id'],)).fetchall()

        claim_data = dict(c)
        # Apply redaction to text fields
        claim_data['text'] = redact_text(claim_data['text'])
        evidence_list = []
        for l in links:
            ev = dict(l)
            ev['summary'] = redact_text(ev['summary'])
            if ev.get('note'):
                ev['note'] = redact_text(ev['note'])
            evidence_list.append(ev)
        claim_data['evidence'] = evidence_list

        # Compute support status
        supports = sum(1 for l in links if l['relation'] == 'supports')
        challenges = sum(1 for l in links if l['relation'] == 'challenges')
        if challenges > supports:
            claim_data['support_status'] = 'contested'
        elif challenges > 0:
            claim_data['support_status'] = 'partial'
        elif supports > 0:
            claim_data['support_status'] = 'supported'
        else:
            claim_data['support_status'] = 'undocumented'

        result.append(claim_data)

    return jsonify(result)

@app.route('/api/claims/<claim_id>/verify', methods=['POST'])
def api_verify_claim(claim_id):
    """Update verification status for a claim."""
    db = get_db()
    data = request.json

    status = data.get('status', 'unverified')
    reviewer = data.get('reviewer', 'anonymous')

    if status not in ('unverified', 'author_verified', 'external_verified'):
        return jsonify({'error': 'Invalid status'}), 400

    # Get old status for audit
    old = db.execute("SELECT verification_status FROM claim WHERE claim_id = ?", (claim_id,)).fetchone()
    old_status = old['verification_status'] if old else None

    db.execute("""
        UPDATE claim
        SET verification_status = ?, verified_by = ?, verified_at = ?
        WHERE claim_id = ?
    """, (status, reviewer, now(), claim_id))

    # Audit trail
    db.execute("""
        INSERT INTO verification_audit (action_type, target_id, old_status, new_status, reviewer, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ('claim_verify', claim_id, old_status, status, reviewer, now()))

    db.commit()

    return jsonify({'success': True, 'claim_id': claim_id, 'status': status})

@app.route('/api/links/<claim_id>/<evidence_id>/verify', methods=['POST'])
def api_verify_link(claim_id, evidence_id):
    """Update verification status for a claim-evidence link."""
    db = get_db()
    data = request.json

    status = data.get('status', 'unverified')
    reviewer = data.get('reviewer', 'anonymous')
    analytic_note = data.get('analytic_note')

    if status not in ('unverified', 'author_verified', 'external_verified'):
        return jsonify({'error': 'Invalid status'}), 400

    # Get old status for audit
    old = db.execute("""
        SELECT verification_status FROM claim_evidence_link
        WHERE claim_id = ? AND evidence_id = ?
    """, (claim_id, evidence_id)).fetchone()
    old_status = old['verification_status'] if old else None

    # Update link
    if analytic_note:
        db.execute("""
            UPDATE claim_evidence_link
            SET verification_status = ?, verified_by = ?, verified_at = ?, analytic_note = ?
            WHERE claim_id = ? AND evidence_id = ?
        """, (status, reviewer, now(), analytic_note, claim_id, evidence_id))
    else:
        db.execute("""
            UPDATE claim_evidence_link
            SET verification_status = ?, verified_by = ?, verified_at = ?
            WHERE claim_id = ? AND evidence_id = ?
        """, (status, reviewer, now(), claim_id, evidence_id))

    # Audit trail
    target_id = f"{claim_id}:{evidence_id}"
    db.execute("""
        INSERT INTO verification_audit (action_type, target_id, old_status, new_status, reviewer, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ('link_verify', target_id, old_status, status, reviewer, analytic_note, now()))

    db.commit()

    return jsonify({'success': True, 'claim_id': claim_id, 'evidence_id': evidence_id, 'status': status})

@app.route('/api/papers/<paper_id>/report')
def api_generate_report(paper_id):
    """Generate a verification report for a paper."""
    db = get_db()

    # Get timing info from query params
    session_seconds = request.args.get('session_seconds', type=int, default=0)
    reviewer = request.args.get('reviewer', 'anonymous')

    # Get paper info
    paper = db.execute("SELECT * FROM paper WHERE paper_id = ?", (paper_id,)).fetchone()
    if not paper:
        return jsonify({'error': 'Paper not found'}), 404

    # Get claims with evidence
    claims = db.execute("""
        SELECT claim_id, claim_type, text, confidence, verification_status, verified_by, verified_at
        FROM claim WHERE paper_id = ? ORDER BY claim_id
    """, (paper_id,)).fetchall()

    # Get verification audit for this paper
    audit_entries = db.execute("""
        SELECT * FROM verification_audit
        WHERE target_id LIKE ? OR target_id IN (SELECT claim_id FROM claim WHERE paper_id = ?)
        ORDER BY created_at
    """, (f'{paper_id}%', paper_id)).fetchall()

    # Build report
    lines = []
    lines.append(f"# Verification Report: {paper_id}")
    lines.append(f"\nGenerated: {now()}")
    lines.append(f"\n## Summary\n")

    total = len(claims)
    verified = sum(1 for c in claims if c['verification_status'] == 'external_verified')
    author_only = sum(1 for c in claims if c['verification_status'] == 'author_verified')
    unverified = total - verified - author_only

    lines.append(f"- Reviewer: {reviewer}")
    lines.append(f"- Review session duration: {session_seconds // 60}m {session_seconds % 60}s")
    lines.append(f"- Total claims: {total}")
    lines.append(f"- Externally verified: {verified} ({round(verified/total*100) if total else 0}%)")
    lines.append(f"- Author verified only: {author_only} ({round(author_only/total*100) if total else 0}%)")
    lines.append(f"- Not verified: {unverified} ({round(unverified/total*100) if total else 0}%)")

    lines.append(f"\n## Claims Detail\n")

    for c in claims:
        status_icon = {"external_verified": "[VERIFIED]", "author_verified": "[AUTHOR ONLY]", "unverified": "[NOT VERIFIED]"}.get(c['verification_status'], "[?]")
        lines.append(f"### {c['claim_id']} {status_icon}")
        lines.append(f"**Type:** {c['claim_type']} | **Confidence:** {c['confidence']}")
        # Apply redaction to claim text
        claim_text = redact_text(c['text'])
        lines.append(f"\n> {claim_text}\n")

        if c['verified_by']:
            lines.append(f"*Verified by {c['verified_by']} on {c['verified_at']}*\n")

        # Get evidence links
        links = db.execute("""
            SELECT l.*, e.summary, e.sensitivity_tier
            FROM claim_evidence_link l
            JOIN evidence e ON e.evidence_id = l.evidence_id
            WHERE l.claim_id = ?
            ORDER BY l.weight, l.relation
        """, (c['claim_id'],)).fetchall()

        if links:
            lines.append("**Evidence links:**\n")
            for l in links:
                link_status = {"external_verified": "[V]", "author_verified": "[A]", "unverified": "[ ]"}.get(l['verification_status'], "[ ]")
                lines.append(f"- {link_status} {l['evidence_id']} ({l['relation']}, {l['weight']})")
                if l['analytic_note']:
                    # Apply redaction to analytic notes
                    analytic_note = redact_text(l['analytic_note'])
                    lines.append(f"  - *Analytic note:* {analytic_note}")
            lines.append("")

    lines.append(f"\n## Audit Trail\n")
    for a in audit_entries:
        audit_line = f"- {a['created_at']}: {a['action_type']} on {a['target_id']} ({a['old_status']} → {a['new_status']}) by {a['reviewer']}"
        # Redact notes if present in audit
        if a['notes']:
            audit_notes = redact_text(a['notes'])
            audit_line += f" - {audit_notes}"
        lines.append(audit_line)

    report_text = "\n".join(lines)

    return jsonify({
        'paper_id': paper_id,
        'report': report_text,
        'summary': {
            'total': total,
            'verified': verified,
            'author_only': author_only,
            'unverified': unverified
        }
    })

@app.route('/api/stats')
def api_stats():
    """Get overall verification statistics."""
    db = get_db()

    # Claims stats
    claim_stats = db.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN verification_status = 'external_verified' THEN 1 ELSE 0 END) as verified,
            SUM(CASE WHEN verification_status = 'author_verified' THEN 1 ELSE 0 END) as author_verified
        FROM claim
    """).fetchone()

    # Link stats
    link_stats = db.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN verification_status = 'external_verified' THEN 1 ELSE 0 END) as verified
        FROM claim_evidence_link
    """).fetchone()

    # Evidence by tier
    tier_stats = db.execute("""
        SELECT sensitivity_tier, COUNT(*) as count
        FROM evidence
        GROUP BY sensitivity_tier
    """).fetchall()

    return jsonify({
        'claims': {
            'total': claim_stats['total'],
            'external_verified': claim_stats['verified'],
            'author_verified': claim_stats['author_verified'],
            'unverified': claim_stats['total'] - claim_stats['verified'] - claim_stats['author_verified']
        },
        'links': {
            'total': link_stats['total'],
            'verified': link_stats['verified']
        },
        'evidence_by_tier': {t['sensitivity_tier']: t['count'] for t in tier_stats}
    })

# =============================================================================
# HTML Templates
# =============================================================================

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Living Paper: Reviewer Interface</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header {
            background: #1a1a2e;
            color: white;
            padding: 20px;
            margin-bottom: 20px;
        }
        header h1 { font-size: 1.5rem; font-weight: 500; }
        header p { opacity: 0.8; font-size: 0.9rem; margin-top: 5px; }

        .stats-bar {
            display: flex;
            gap: 20px;
            background: white;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .stat { text-align: center; }
        .stat-value { font-size: 1.5rem; font-weight: 600; color: #1a1a2e; }
        .stat-label { font-size: 0.75rem; color: #666; text-transform: uppercase; }

        .paper-list {
            display: grid;
            gap: 15px;
        }
        .paper-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: transform 0.1s, box-shadow 0.1s;
        }
        .paper-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .paper-card h2 { font-size: 1.1rem; margin-bottom: 10px; }
        .paper-meta { display: flex; gap: 20px; font-size: 0.85rem; color: #666; }

        .claim-list { display: grid; gap: 15px; }
        .claim-card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .claim-header {
            padding: 15px 20px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 15px;
        }
        .claim-id {
            font-family: monospace;
            font-size: 0.8rem;
            color: #666;
            background: #f0f0f0;
            padding: 2px 8px;
            border-radius: 4px;
        }
        .claim-text { font-size: 1rem; flex: 1; }
        .claim-type {
            font-size: 0.7rem;
            text-transform: uppercase;
            padding: 3px 8px;
            border-radius: 4px;
            background: #e0e0e0;
        }
        .claim-type.empirical { background: #e3f2fd; color: #1565c0; }
        .claim-type.theoretical { background: #f3e5f5; color: #7b1fa2; }

        .status-badge {
            font-size: 0.7rem;
            text-transform: uppercase;
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: 500;
        }
        .status-supported { background: #c8e6c9; color: #2e7d32; }
        .status-partial { background: #fff3e0; color: #ef6c00; }
        .status-contested { background: #ffcdd2; color: #c62828; }
        .status-undocumented { background: #e0e0e0; color: #616161; }

        .evidence-list { padding: 15px 20px; }
        .evidence-item {
            padding: 12px;
            margin-bottom: 10px;
            background: #fafafa;
            border-radius: 6px;
            border-left: 3px solid #ccc;
        }
        .evidence-item.supports { border-left-color: #4caf50; }
        .evidence-item.challenges { border-left-color: #f44336; }
        .evidence-item.qualifies { border-left-color: #ff9800; }
        .evidence-item.illustrates { border-left-color: #2196f3; }

        .evidence-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        .evidence-id { font-family: monospace; font-size: 0.8rem; color: #666; }
        .evidence-relation {
            font-size: 0.7rem;
            text-transform: uppercase;
            padding: 2px 6px;
            border-radius: 3px;
            background: #e0e0e0;
        }
        .evidence-summary { font-size: 0.9rem; color: #444; }
        .evidence-note { font-size: 0.8rem; color: #666; font-style: italic; margin-top: 5px; }
        .evidence-controlled {
            color: #999;
            font-style: italic;
        }

        .verify-controls {
            display: flex;
            gap: 8px;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #eee;
        }
        .verify-btn {
            padding: 6px 12px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: background 0.2s;
        }
        .verify-btn.verified { background: #4caf50; color: white; }
        .verify-btn.uncertain { background: #ff9800; color: white; }
        .verify-btn.incorrect { background: #f44336; color: white; }
        .verify-btn:hover { opacity: 0.9; }
        .verify-btn.active { box-shadow: 0 0 0 2px #333; }

        .reviewer-input {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            align-items: center;
        }
        .reviewer-input label { font-size: 0.9rem; color: #666; }
        .reviewer-input input {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 0.9rem;
        }

        .back-link {
            display: inline-block;
            margin-bottom: 15px;
            color: #1a1a2e;
            text-decoration: none;
            font-size: 0.9rem;
        }
        .back-link:hover { text-decoration: underline; }

        .confidence-bar {
            width: 60px;
            height: 6px;
            background: #e0e0e0;
            border-radius: 3px;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
            margin-left: 8px;
        }
        .confidence-fill {
            height: 100%;
            background: #1a1a2e;
        }

        .analytic-note-input {
            width: 100%;
            margin-top: 8px;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 0.85rem;
            resize: vertical;
            min-height: 60px;
        }
        .analytic-note-input:focus {
            outline: none;
            border-color: #1a1a2e;
        }

        .verification-status {
            font-size: 0.75rem;
            color: #666;
            margin-top: 5px;
        }
        .verification-status.verified { color: #2e7d32; }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Living Paper Reviewer</h1>
            <p>A reviewer interface for bidirectional claim-evidence traceability in qualitative research<sup style="font-size: 0.7em; cursor: help;" title="Drawing on approaches from QDR Annotation for Transparent Inquiry, AJPS verification policies, and Aguinis & Solarino (2019) transparency criteria.">[*]</sup></p>
        </div>
    </header>

    <div class="container" style="margin-bottom: 0;">
        <div class="instructions" style="background: #fff8e1; border: 1px solid #ffe082; border-radius: 8px; padding: 15px 20px; margin-bottom: 20px; font-size: 0.9rem;">
            <strong>What is this?</strong> This interface helps verify that claims in a qualitative research paper are adequately supported by the evidence cited. For each claim, you'll see linked evidence items. Your task is to assess whether each evidence-claim link is valid and well-documented.
            <br><br>
            <strong>How to use:</strong> (1) Enter your name below. (2) Click a paper to see its claims. (3) For each evidence item, write an analytic note explaining how the evidence relates to the claim, then mark your verification status. (4) When finished, generate a verification report.
        </div>
    </div>

    <div class="container">
        <div id="app">Loading...</div>
    </div>

    <script>
        const API = {
            async get(url) {
                const res = await fetch(url);
                return res.json();
            },
            async post(url, data) {
                const res = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                return res.json();
            }
        };

        let currentPaper = null;
        let reviewerName = localStorage.getItem('reviewerName') || '';
        let sessionStartTime = null;
        let timerInterval = null;

        function startSessionTimer() {
            sessionStartTime = new Date();
            // Timer runs silently - no visible display to prevent gaming
        }

        async function generateReport(paperId) {
            const elapsed = sessionStartTime ? Math.floor((new Date() - sessionStartTime) / 1000) : 0;
            const minTime = 60; // At least 1 minute expected

            // Good-faith attestation
            const attestation = confirm(
                "Before generating the report, please confirm:\\n\\n" +
                "I attest that I have made a good-faith effort to verify each claim-evidence link, " +
                "reading the evidence summaries carefully and providing analytic notes where appropriate.\\n\\n" +
                "Click OK to generate the report, or Cancel to continue reviewing."
            );

            if (!attestation) return;

            if (elapsed < minTime) {
                const proceed = confirm(
                    "You may want to spend more time reviewing the evidence links.\\n\\n" +
                    "Are you sure you want to generate the report now?"
                );
                if (!proceed) return;
            }

            const response = await API.get(`/api/papers/${paperId}/report?session_seconds=${elapsed}&reviewer=${encodeURIComponent(reviewerName || 'anonymous')}`);

            // Create download
            const blob = new Blob([response.report], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `verification_report_${paperId}_${new Date().toISOString().slice(0,10)}.md`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            alert(`Report generated!\\n\\nSummary:\\n- Verified: ${response.summary.verified}/${response.summary.total}\\n- Author Only: ${response.summary.author_only}\\n- Not Verified: ${response.summary.unverified}`);
        }

        async function renderPaperList() {
            const [papers, stats] = await Promise.all([
                API.get('/api/papers'),
                API.get('/api/stats')
            ]);

            const app = document.getElementById('app');
            app.innerHTML = `
                <div class="stats-bar">
                    <div class="stat">
                        <div class="stat-value">${stats.claims.total}</div>
                        <div class="stat-label">Claims</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${stats.claims.external_verified}</div>
                        <div class="stat-label">Verified</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${Math.round(stats.claims.external_verified / stats.claims.total * 100) || 0}%</div>
                        <div class="stat-label">Progress</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${stats.links.total}</div>
                        <div class="stat-label">Evidence Links</div>
                    </div>
                </div>

                <div class="reviewer-input">
                    <label>Your name:</label>
                    <input type="text" id="reviewer-name" placeholder="Reviewer name" value="${reviewerName}">
                </div>

                <h2 style="margin-bottom: 15px;">Papers</h2>
                <div class="paper-list">
                    ${papers.map(p => `
                        <div class="paper-card" onclick="renderClaims('${p.paper_id}')">
                            <h2>${p.paper_id}</h2>
                            <div class="paper-meta">
                                <span>${p.claim_count} claims</span>
                                <span>${p.evidence_count} evidence items</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;

            document.getElementById('reviewer-name').addEventListener('change', (e) => {
                reviewerName = e.target.value;
                localStorage.setItem('reviewerName', reviewerName);
            });
        }

        async function renderClaims(paperId) {
            currentPaper = paperId;
            const claims = await API.get(`/api/papers/${paperId}/claims`);

            const app = document.getElementById('app');
            app.innerHTML = `
                <a href="#" class="back-link" onclick="renderPaperList(); return false;">&larr; Back to papers</a>

                <h2 style="margin-bottom: 15px;">${paperId}</h2>

                <div class="status-key" style="background: #f5f5f5; border-radius: 8px; padding: 15px 20px; margin-bottom: 20px; font-size: 0.85rem;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div>
                            <strong>Verification Status (your input):</strong>
                            <div style="margin-top: 8px;">
                                <div style="margin-bottom: 6px;"><span style="background: #4caf50; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem;">Verified</span> = You can trace this claim to the cited evidence; the link is well-documented</div>
                                <div style="margin-bottom: 6px;"><span style="background: #ff9800; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem;">Author Only</span> = The link relies on context only the author has access to (e.g., confidential data)</div>
                                <div><span style="background: #f44336; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem;">Not Verified</span> = You cannot confirm the claim-evidence relationship from the materials provided</div>
                            </div>
                        </div>
                        <div>
                            <strong>Claim Labels (pre-computed):</strong>
                            <div style="margin-top: 8px;">
                                <div style="margin-bottom: 6px;"><span class="claim-type empirical" style="font-size: 0.75rem;">empirical</span> = Based on data/observations &nbsp; <span class="claim-type theoretical" style="font-size: 0.75rem;">theoretical</span> = Conceptual/framework claim</div>
                                <div style="margin-bottom: 6px;"><span class="status-badge status-supported" style="font-size: 0.75rem;">supported</span> = More supporting than challenging evidence</div>
                                <div style="margin-bottom: 6px;"><span class="status-badge status-partial" style="font-size: 0.75rem;">partial</span> = Mixed evidence (some challenges) &nbsp; <span class="status-badge status-contested" style="font-size: 0.75rem;">contested</span> = More challenges than support</div>
                                <div><span class="status-badge status-undocumented" style="font-size: 0.75rem;">undocumented</span> = No supporting evidence linked</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="display: flex; justify-content: flex-end; margin-bottom: 15px;">
                    <button onclick="generateReport('${paperId}')" style="background: #1a1a2e; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-size: 0.9rem;">
                        Generate Verification Report
                    </button>
                </div>

                <div class="claim-list">
                    ${claims.map(c => `
                        <div class="claim-card">
                            <div class="claim-header">
                                <div>
                                    <span class="claim-id">${c.claim_id}</span>
                                    <span class="claim-type ${c.claim_type}">${c.claim_type}</span>
                                    <span class="status-badge status-${c.support_status}">${c.support_status}</span>
                                    <span class="confidence-bar"><span class="confidence-fill" style="width: ${c.confidence * 100}%"></span></span>
                                </div>
                            </div>
                            <div style="padding: 0 20px 15px;">
                                <p class="claim-text">${c.text}</p>
                                ${(c.informant_coverage || c.saturation_note || c.prevalence_basis) ? `
                                <div style="margin-top: 8px; padding: 8px 12px; background: #f8f9fa; border-radius: 4px; font-size: 0.8rem; color: #555;">
                                    <strong>Prevalence:</strong>
                                    ${c.informant_coverage ? `<span style="margin-left: 8px;">📊 ${c.informant_coverage}</span>` : ''}
                                    ${c.prevalence_basis ? `<span style="margin-left: 8px; background: #e3f2fd; padding: 2px 6px; border-radius: 3px;">${c.prevalence_basis}</span>` : ''}
                                    ${c.contradicting_count === 0 ? `<span style="margin-left: 8px; color: #2e7d32;">✓ No contradicting evidence</span>` :
                                      c.contradicting_count > 0 ? `<span style="margin-left: 8px; color: #c62828;">⚠ ${c.contradicting_count} contradicting</span>` : ''}
                                    ${c.saturation_note ? `<div style="margin-top: 4px; font-style: italic;">${c.saturation_note}</div>` : ''}
                                </div>
                                ` : ''}
                                ${c.verification_status === 'external_verified' ?
                                    `<p class="verification-status verified">✓ Verified by ${c.verified_by} on ${c.verified_at}</p>` : ''}
                            </div>
                            <div class="evidence-list">
                                <strong style="font-size: 0.85rem; color: #666;">Evidence (${c.evidence.length})</strong>
                                ${c.evidence.map(e => `
                                    <div class="evidence-item ${e.relation}">
                                        <div class="evidence-header">
                                            <span class="evidence-id">${e.evidence_id}</span>
                                            <span>
                                                <span class="evidence-relation">${e.relation}</span>
                                                <span class="evidence-relation">${e.weight}</span>
                                            </span>
                                        </div>
                                        <p class="evidence-summary ${e.sensitivity_tier === 'CONTROLLED' ? 'evidence-controlled' : ''}">
                                            ${e.sensitivity_tier === 'CONTROLLED' && !e.summary.includes('[CONTROLLED]') ? e.summary :
                                              e.sensitivity_tier === 'CONTROLLED' ? '[CONTROLLED - Request access to view]' : e.summary}
                                        </p>
                                        ${e.note ? `<p class="evidence-note">Note: ${e.note}</p>` : ''}
                                        ${e.analytic_note ? `<p class="evidence-note">Analytic: ${e.analytic_note}</p>` : ''}
                                        ${e.verification_status === 'external_verified' ?
                                            `<p class="verification-status verified">✓ Verified by ${e.verified_by}</p>` : ''}

                                        <textarea class="analytic-note-input"
                                            placeholder="How does this evidence support/challenge the claim? (interpretive reasoning)"
                                            data-claim="${c.claim_id}"
                                            data-evidence="${e.evidence_id}">${e.analytic_note || ''}</textarea>

                                        <div class="verify-controls">
                                            <button class="verify-btn verified ${e.verification_status === 'external_verified' ? 'active' : ''}"
                                                onclick="verifyLink('${c.claim_id}', '${e.evidence_id}', 'external_verified')">
                                                ✓ Verified
                                            </button>
                                            <button class="verify-btn uncertain"
                                                onclick="verifyLink('${c.claim_id}', '${e.evidence_id}', 'author_verified')">
                                                ? Author Only
                                            </button>
                                            <button class="verify-btn incorrect ${e.verification_status === 'unverified' ? 'active' : ''}"
                                                onclick="verifyLink('${c.claim_id}', '${e.evidence_id}', 'unverified')">
                                                ✗ Not Verified
                                            </button>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;

            // Start session timer
            startSessionTimer();
        }

        async function verifyLink(claimId, evidenceId, status) {
            const textarea = document.querySelector(`textarea[data-claim="${claimId}"][data-evidence="${evidenceId}"]`);
            const analyticNote = textarea ? textarea.value : null;

            await API.post(`/api/links/${claimId}/${evidenceId}/verify`, {
                status,
                reviewer: reviewerName || 'anonymous',
                analytic_note: analyticNote
            });

            // Refresh
            renderClaims(currentPaper);
        }

        // Initial render
        renderPaperList();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_TEMPLATE)

# =============================================================================
# Main
# =============================================================================

def main():
    global DB_PATH, REDACTOR

    parser = argparse.ArgumentParser(description='Living Paper Reviewer Interface')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on')
    parser.add_argument('--db', type=str, help='Path to lp_public.sqlite')
    parser.add_argument('--entities', type=str, help='Path to entities.yaml for PII redaction')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    args = parser.parse_args()

    # Find database
    if args.db:
        DB_PATH = args.db
    else:
        # Default: look in standard location
        script_dir = Path(__file__).resolve().parent
        DB_PATH = script_dir.parent / "analysis" / "living_paper" / "lp_public.sqlite"

    if not Path(DB_PATH).exists():
        print(f"Database not found: {DB_PATH}")
        print("Run 'python lp.py init' first, or specify --db path")
        return 1

    # Set up redactor if entities file provided
    if args.entities:
        entities_path = Path(args.entities)
        if not entities_path.exists():
            print(f"Entities file not found: {entities_path}")
            return 1
        if not HAS_REDACTOR:
            print("Entity redaction requested but redact.py not available")
            return 1
        REDACTOR = EntityRedactor(entities_path=entities_path)
        print(f"[living_paper] Entity redaction enabled from: {entities_path}")

    print(f"[living_paper] Reviewer interface starting...")
    print(f"  Database: {DB_PATH}")
    print(f"  URL: http://localhost:{args.port}")

    app.run(host='0.0.0.0', port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()
