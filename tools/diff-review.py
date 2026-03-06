#!/usr/bin/env python3
"""
theory-forge diff-review: Annotated HTML diff viewer for manuscript revisions.

Generates a GitHub-style dark-mode diff viewer comparing an original manuscript
against a proposed revision, with per-hunk annotations explaining what changed
and why. Designed for human review of AI-generated changes.

Usage:
    python3 diff-review.py ORIGINAL PROPOSED [--annotations FILE] [--output FILE] [--title TEXT] [--open]

    ORIGINAL and PROPOSED can be individual files or directories. When directories
    are given, all .tex and .bib files are diffed pairwise by filename.

Examples:
    # Compare two files
    python3 diff-review.py original/main.tex revised/main.tex --open

    # Compare two directories (matches files by name)
    python3 diff-review.py ~/Desktop/overleaf-export/ ./submission/ --open

    # With annotations from a JSON sidecar
    python3 diff-review.py original/ revised/ --annotations review-notes.json --open

Annotations JSON format:
    {
        "main.tex": {
            "0": {"title": "Restructure theory section", "rationale": "Zuckerman eval..."},
            "1": {"title": "Genre word sub", "rationale": "..."}
        },
        "references.bib": {
            "0": {"title": "Remove unused entry", "rationale": "..."}
        }
    }

When no annotations file is provided, Claude is expected to generate annotations
inline as part of the /review-diff command workflow.
"""

import argparse
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def unified_diff(file_a, file_b):
    """Run diff -u and return the output."""
    result = subprocess.run(
        ['diff', '-u', str(file_a), str(file_b)],
        capture_output=True, text=True
    )
    return result.stdout


def parse_diff(patch_text):
    """Parse unified diff into structured hunks."""
    hunks = []
    current_hunk = None
    for line in patch_text.split('\n'):
        if line.startswith('@@'):
            if current_hunk:
                hunks.append(current_hunk)
            match = re.match(r'@@ -(\d+),?\d* \+(\d+),?\d* @@(.*)', line)
            current_hunk = {
                'old_start': int(match.group(1)) if match else 0,
                'new_start': int(match.group(2)) if match else 0,
                'context': (match.group(3).strip() if match else ''),
                'lines': [],
            }
        elif current_hunk is not None:
            if line.startswith('+') and not line.startswith('+++'):
                current_hunk['lines'].append(('add', line[1:]))
            elif line.startswith('-') and not line.startswith('---'):
                current_hunk['lines'].append(('del', line[1:]))
            elif line.startswith(' '):
                current_hunk['lines'].append(('ctx', line[1:]))
            elif line == '':
                current_hunk['lines'].append(('ctx', ''))
    if current_hunk:
        hunks.append(current_hunk)
    return hunks


def render_hunks(hunks, file_label, annotations):
    """Render parsed hunks to HTML string."""
    out = []
    safe_id = re.sub(r'[^a-zA-Z0-9]', '-', file_label)
    out.append(
        f'<div class="file-header" id="{safe_id}">'
        f'<span class="file-icon">📄</span> {html.escape(file_label)}</div>'
    )

    for i, hunk in enumerate(hunks):
        hunk_id = f'{safe_id}-hunk-{i}'
        label = hunk.get('context', '') or f'Line {hunk["old_start"]}'
        adds = sum(1 for t, _ in hunk['lines'] if t == 'add')
        dels = sum(1 for t, _ in hunk['lines'] if t == 'del')
        stats = f'<span class="stat-add">+{adds}</span> <span class="stat-del">-{dels}</span>'

        ann = annotations.get(str(i), {})
        ann_title = ann.get('title', '')
        ann_rationale = ann.get('rationale', '')

        out.append('<div class="hunk">')
        out.append(f'<div class="hunk-header" onclick="toggleHunk(\'{hunk_id}\')">')
        out.append(f'<span class="toggle open" id="toggle-{hunk_id}">▶</span>')
        out.append(f'<span class="hunk-location">@@ Line {hunk["old_start"]} → {hunk["new_start"]}</span>')
        out.append(f'<span class="hunk-context">{html.escape(label)}</span>')
        out.append(f'<span class="hunk-stats">{stats}</span>')
        out.append('</div>')

        if ann_title:
            out.append('<div class="annotation">')
            out.append(f'<div class="ann-title">{html.escape(ann_title)}</div>')
            if ann_rationale:
                out.append(f'<div class="ann-rationale">{html.escape(ann_rationale)}</div>')
            out.append('</div>')

        out.append(f'<div class="hunk-body" id="{hunk_id}" style="display:block;">')

        old_num = hunk['old_start']
        new_num = hunk['new_start']

        for typ, content in hunk['lines']:
            escaped = html.escape(content)
            if typ == 'del':
                out.append(
                    f'<div class="line line-del">'
                    f'<span class="ln ln-old">{old_num}</span>'
                    f'<span class="ln ln-new"></span>'
                    f'<span class="sign">-</span>'
                    f'<span class="code">{escaped}</span></div>'
                )
                old_num += 1
            elif typ == 'add':
                out.append(
                    f'<div class="line line-add">'
                    f'<span class="ln ln-old"></span>'
                    f'<span class="ln ln-new">{new_num}</span>'
                    f'<span class="sign">+</span>'
                    f'<span class="code">{escaped}</span></div>'
                )
                new_num += 1
            else:
                out.append(
                    f'<div class="line line-ctx">'
                    f'<span class="ln ln-old">{old_num}</span>'
                    f'<span class="ln ln-new">{new_num}</span>'
                    f'<span class="sign"> </span>'
                    f'<span class="code">{escaped}</span></div>'
                )
                old_num += 1
                new_num += 1

        out.append('</div></div>')
    return '\n'.join(out)


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  :root {{
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --text: #c9d1d9; --text-dim: #8b949e;
    --add-bg: #12261e; --add-line: #aff5b4;
    --del-bg: #2d1215; --del-line: #ffa198;
    --header-bg: #1c2128; --accent: #58a6ff; --accent-dim: #388bfd44;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.5;
  }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
  .page-header {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 24px; margin-bottom: 20px;
  }}
  .page-header h1 {{ font-size: 20px; font-weight: 600; margin-bottom: 4px; }}
  .page-header .subtitle {{ color: var(--accent); font-size: 14px; margin-bottom: 8px; }}
  .page-header .meta {{ color: var(--text-dim); font-size: 13px; }}
  .summary-stats {{ display: flex; gap: 16px; margin-top: 12px; font-size: 13px; flex-wrap: wrap; }}
  .controls {{ display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }}
  .controls button {{
    background: var(--surface); border: 1px solid var(--border);
    color: var(--text); padding: 6px 14px; border-radius: 6px;
    cursor: pointer; font-size: 13px; transition: all 0.15s;
  }}
  .controls button:hover {{ background: var(--header-bg); border-color: var(--accent); }}
  .file-nav {{ display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }}
  .file-nav a {{
    color: var(--accent); text-decoration: none; background: var(--surface);
    border: 1px solid var(--border); padding: 6px 14px; border-radius: 6px; font-size: 13px;
  }}
  .file-nav a:hover {{ border-color: var(--accent); }}
  .file-header {{
    background: var(--header-bg); border: 1px solid var(--border); border-bottom: none;
    border-radius: 8px 8px 0 0; padding: 12px 16px; font-weight: 600; font-size: 14px;
    margin-top: 24px; position: sticky; top: 0; z-index: 10;
  }}
  .file-icon {{ margin-right: 8px; }}
  .hunk {{ border: 1px solid var(--border); border-top: none; overflow: hidden; }}
  .hunk:last-child {{ border-radius: 0 0 8px 8px; }}
  .hunk-header {{
    background: var(--surface); padding: 8px 16px; cursor: pointer;
    display: flex; align-items: center; gap: 10px; font-size: 13px;
    border-top: 1px solid var(--border); user-select: none; transition: background 0.15s;
  }}
  .hunk-header:hover {{ background: var(--header-bg); }}
  .toggle {{
    color: var(--text-dim); font-size: 11px; width: 14px;
    transition: transform 0.2s; display: inline-block;
  }}
  .toggle.open {{ transform: rotate(90deg); }}
  .hunk-location {{
    font-family: ui-monospace, SFMono-Regular, monospace;
    color: var(--accent); font-size: 12px; white-space: nowrap;
  }}
  .hunk-context {{
    color: var(--text-dim); flex: 1; overflow: hidden;
    text-overflow: ellipsis; white-space: nowrap;
  }}
  .hunk-stats {{
    white-space: nowrap; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 12px;
  }}
  .stat-add {{ color: var(--add-line); margin-right: 6px; }}
  .stat-del {{ color: var(--del-line); }}
  .annotation {{
    background: #1a1f2b; border-left: 3px solid var(--accent);
    padding: 10px 16px; font-size: 13px;
  }}
  .ann-title {{ color: var(--accent); font-weight: 600; margin-bottom: 4px; }}
  .ann-rationale {{ color: var(--text-dim); line-height: 1.5; }}
  .hunk-body {{ overflow-x: auto; }}
  .line {{
    display: flex; font-family: ui-monospace, SFMono-Regular, monospace;
    font-size: 12.5px; line-height: 20px; white-space: pre-wrap; word-break: break-word;
  }}
  .line-add {{ background: var(--add-bg); }}
  .line-del {{ background: var(--del-bg); }}
  .line-add .code {{ color: var(--add-line); }}
  .line-del .code {{ color: var(--del-line); }}
  .ln {{
    display: inline-block; width: 50px; min-width: 50px; text-align: right;
    padding-right: 8px; color: var(--text-dim); font-size: 11px; user-select: none; opacity: 0.5;
  }}
  .sign {{
    display: inline-block; width: 16px; min-width: 16px; text-align: center;
    user-select: none; font-weight: bold;
  }}
  .line-add .sign {{ color: var(--add-line); }}
  .line-del .sign {{ color: var(--del-line); }}
  .code {{ flex: 1; padding-right: 12px; }}
  .keyboard-hint {{
    position: fixed; bottom: 16px; right: 16px; background: var(--surface);
    border: 1px solid var(--border); border-radius: 8px; padding: 8px 14px;
    font-size: 12px; color: var(--text-dim); z-index: 100;
  }}
  kbd {{
    background: var(--header-bg); border: 1px solid var(--border);
    border-radius: 3px; padding: 1px 5px; font-size: 11px;
    font-family: ui-monospace, SFMono-Regular, monospace;
  }}
</style>
</head>
<body>
<div class="container">
  <div class="page-header">
    <h1>{title}</h1>
    <div class="subtitle">Original vs. proposed changes</div>
    <div class="meta">
      <span style="color:var(--del-line);">Red = original text (removed)</span> &middot;
      <span style="color:var(--add-line);">Green = proposed replacement</span> &middot;
      White = unchanged context
    </div>
    <div class="summary-stats">{stats_html}</div>
  </div>
  <div class="controls">
    <button onclick="expandAll()">Expand All</button>
    <button onclick="collapseAll()">Collapse All</button>
  </div>
  <div class="file-nav">{nav_html}</div>
  {body_html}
</div>
<div class="keyboard-hint">
  <kbd>E</kbd> expand all &ensp; <kbd>C</kbd> collapse all &ensp; Click hunk headers to toggle
</div>
<script>
function toggleHunk(id) {{
  const el = document.getElementById(id);
  const toggle = document.getElementById('toggle-' + id);
  if (el.style.display === 'none') {{
    el.style.display = 'block'; toggle.classList.add('open');
  }} else {{
    el.style.display = 'none'; toggle.classList.remove('open');
  }}
}}
function expandAll() {{
  document.querySelectorAll('.hunk-body').forEach(el => el.style.display = 'block');
  document.querySelectorAll('.toggle').forEach(el => el.classList.add('open'));
}}
function collapseAll() {{
  document.querySelectorAll('.hunk-body').forEach(el => el.style.display = 'none');
  document.querySelectorAll('.toggle').forEach(el => el.classList.remove('open'));
}}
document.addEventListener('keydown', function(e) {{
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  if (e.key === 'e' || e.key === 'E') expandAll();
  if (e.key === 'c' || e.key === 'C') collapseAll();
}});
</script>
</body>
</html>'''


def find_file_pairs(dir_a, dir_b):
    """Match .tex and .bib files between two directories by stem."""
    exts = {'.tex', '.bib'}
    files_a = {}
    files_b = {}
    for f in Path(dir_a).iterdir():
        if f.suffix in exts:
            # Normalize away Overleaf download suffixes like "main (2).tex"
            stem = re.sub(r'\s*\(\d+\)', '', f.stem)
            files_a[stem + f.suffix] = f
    for f in Path(dir_b).iterdir():
        if f.suffix in exts:
            stem = re.sub(r'\s*\(\d+\)', '', f.stem)
            files_b[stem + f.suffix] = f

    pairs = []
    for name in sorted(set(files_a.keys()) | set(files_b.keys())):
        if name in files_a and name in files_b:
            pairs.append((name, files_a[name], files_b[name]))
        elif name in files_a:
            print(f"  ⚠ {name} exists only in original (skipped)", file=sys.stderr)
        else:
            print(f"  ⚠ {name} exists only in proposed (skipped)", file=sys.stderr)
    return pairs


def main():
    parser = argparse.ArgumentParser(
        description='Generate annotated HTML diff for manuscript review'
    )
    parser.add_argument('original', help='Original file or directory')
    parser.add_argument('proposed', help='Proposed file or directory')
    parser.add_argument('--annotations', '-a', help='JSON annotations file')
    parser.add_argument('--output', '-o', help='Output HTML path (default: diff-review.html in cwd)')
    parser.add_argument('--title', '-t', default='Manuscript Diff Review',
                        help='Page title')
    parser.add_argument('--open', action='store_true', help='Open in browser after generating')
    args = parser.parse_args()

    orig = Path(args.original)
    prop = Path(args.proposed)

    # Load annotations if provided
    all_annotations = {}
    if args.annotations:
        with open(args.annotations) as f:
            all_annotations = json.load(f)

    # Build file pairs
    if orig.is_dir() and prop.is_dir():
        pairs = find_file_pairs(orig, prop)
    elif orig.is_file() and prop.is_file():
        name = orig.name
        pairs = [(name, orig, prop)]
    else:
        print("Error: ORIGINAL and PROPOSED must both be files or both be directories.",
              file=sys.stderr)
        sys.exit(1)

    if not pairs:
        print("No matching files found to diff.", file=sys.stderr)
        sys.exit(1)

    # Process each pair
    all_file_html = []
    stats_parts = []
    nav_parts = []

    for name, file_a, file_b in pairs:
        diff_text = unified_diff(file_a, file_b)
        hunks = parse_diff(diff_text)
        if not hunks:
            print(f"  ✓ {name}: no differences", file=sys.stderr)
            continue

        file_annotations = all_annotations.get(name, {})
        file_html = render_hunks(hunks, name, file_annotations)
        all_file_html.append(file_html)

        adds = sum(1 for h in hunks for t, _ in h['lines'] if t == 'add')
        dels = sum(1 for h in hunks for t, _ in h['lines'] if t == 'del')
        safe_id = re.sub(r'[^a-zA-Z0-9]', '-', name)

        stats_parts.append(
            f'<span>{html.escape(name)}: '
            f'<span class="stat-add">+{adds}</span> '
            f'<span class="stat-del">-{dels}</span> '
            f'({len(hunks)} hunks)</span>'
        )
        nav_parts.append(f'<a href="#{safe_id}">📄 {html.escape(name)}</a>')

        print(f"  {name}: +{adds} -{dels} ({len(hunks)} hunks)", file=sys.stderr)

    if not all_file_html:
        print("No differences found in any files.", file=sys.stderr)
        sys.exit(0)

    # Assemble page
    output_path = args.output or 'diff-review.html'
    page = HTML_TEMPLATE.format(
        title=html.escape(args.title),
        stats_html='\n'.join(stats_parts),
        nav_html='\n'.join(nav_parts),
        body_html='\n'.join(all_file_html),
    )

    with open(output_path, 'w') as f:
        f.write(page)
    print(f"\n✓ Written to {output_path}", file=sys.stderr)

    if args.open:
        subprocess.run(['open', output_path])


if __name__ == '__main__':
    main()
