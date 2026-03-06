# Review Diff: Annotated HTML Diff Viewer for Manuscript Revisions

You are the REVIEW-DIFF agent. Your job is to generate an interactive HTML diff viewer that lets the author review AI-proposed changes to their manuscript with full context on what changed and why.

## Why This Exists

AI-generated manuscript revisions are opaque. Authors need to review every change, but raw diffs of LaTeX files are hard to read and provide no rationale. This tool generates a GitHub-style dark-mode HTML viewer where each change is annotated with a brief explanation of what was changed and why — giving the author confidence to accept, reject, or modify each revision.

## When to Run This

Run this **after any pipeline stage that modifies the manuscript** — particularly after:
- `/run-pipeline` with revision execution
- Manual revision sessions where multiple changes were applied
- Any batch of eval-driven fixes (genre subs, citation fixes, theory restructuring)

This is an **optional review tool**, not a gate. It does not block the pipeline.

## Arguments

- `$ARGUMENTS` - Two paths: `ORIGINAL PROPOSED`
  - Can be individual files or directories
  - When directories, all `.tex` and `.bib` files are matched by name
  - Overleaf download naming (e.g., `main (2).tex`) is handled automatically

Optional flags (passed to the Python script):
- `--annotations FILE` — JSON file with per-hunk annotations (see format below)
- `--output FILE` — Output path (default: `diff-review.html` in current directory)
- `--title TEXT` — Page title
- `--open` — Open in browser after generating

## Steps

### 1. Verify the tool exists

```bash
test -f /Users/mattbeane/knowledge-work/projects/theory-forge/tools/diff-review.py
```

If not found, inform the user the tool needs to be installed.

### 2. Determine what to compare

The user should provide two things:
- **Original**: Their current manuscript (e.g., Overleaf download, previous git commit)
- **Proposed**: The revised version (e.g., current working copy, revised files)

If the user provides a git commit range instead of file paths, generate the diff files:
```bash
git diff COMMIT1..COMMIT2 -- path/to/file > /tmp/review.diff
```

### 3. Generate annotations

This is the key value-add. For each hunk in the diff, write a JSON annotations file with:

```json
{
    "main.tex": {
        "0": {
            "title": "Short name of the change",
            "rationale": "Why this change was made — which eval flagged it, what principle it serves, what gate it addresses."
        },
        "1": { "title": "...", "rationale": "..." }
    },
    "references.bib": {
        "0": { "title": "...", "rationale": "..." }
    }
}
```

**How to write good annotations:**

- **title**: 3-8 words. Name the change type. E.g., "Genre word sub: 'test' → 'analysis'", "Add boundary conditions paragraph", "Remove unused bib entry"
- **rationale**: 1-3 sentences. Reference the specific eval that motivated it (Zuckerman, Becker, Genre, Citations, etc.), what criterion was scored Weak/Moderate, and what the fix accomplishes. Be specific enough that the author can judge whether they agree with the reasoning.

**Annotation generation workflow:**

1. Read both files to understand the content
2. Run `diff -u ORIGINAL PROPOSED` to get the raw diff
3. Parse the hunks (or use the Python script's parser)
4. For each hunk, examine the deleted and added lines
5. Cross-reference against any eval reports in `analysis/` to determine which eval drove the change
6. Write the annotations JSON
7. Save to `analysis/review/diff-annotations.json` (or a path the user specifies)

### 4. Run the tool

```bash
python3 /Users/mattbeane/knowledge-work/projects/theory-forge/tools/diff-review.py \
    ORIGINAL PROPOSED \
    --annotations analysis/review/diff-annotations.json \
    --title "Theory-Forge Revision Review" \
    --output analysis/review/diff-review.html \
    --open
```

### 5. Report

Tell the user:
- Where the HTML file was written
- How many files had changes, total hunks, total adds/dels
- That they can press **E** to expand all, **C** to collapse all, or click individual hunks

## Without Annotations

The tool works without annotations too — it just won't show the blue rationale banners:

```bash
python3 /Users/mattbeane/knowledge-work/projects/theory-forge/tools/diff-review.py \
    ORIGINAL PROPOSED --open
```

This is useful for quick diffs where the author just wants to see what changed.

## State Management

This command does not modify `state.json`. It is a pure read/review tool.

## Output

- `analysis/review/diff-review.html` — The interactive diff viewer
- `analysis/review/diff-annotations.json` — The annotations (if generated)

## Features of the HTML Viewer

- GitHub-style dark mode with syntax-colored diffs
- Collapsible hunks (click headers to toggle)
- Keyboard shortcuts: **E** expand all, **C** collapse all
- Per-hunk annotation banners (blue left border) with title + rationale
- File navigation links at top
- Summary stats (files changed, lines added/removed, hunk count)
- Sticky file headers for orientation while scrolling
- Line numbers for both original and proposed versions
- Handles long LaTeX lines with word-wrap
