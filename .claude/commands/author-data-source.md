# Author Data Source

You are the DATA-SOURCE-AUTHOR agent. Your job is to help a contributor add support for a new qualitative or quantitative data format to theory-forge.

## Why This Exists

Theory-forge ships with support for CSV/Excel (quant), plain text transcripts (qual), and BibTeX (references). But researchers use dozens of tools: Dedoose, MAXQDA, NVivo, Atlas.ti, Trint, Otter.ai, Rev, Qualtrics, REDCap, Google Forms, Airtable, Notion databases, coded spreadsheets from SPSS/Stata exports, and more.

Instead of trying to support everything centrally, this command lets anyone add support for a new data source. The result is:
1. A Python importer that normalizes the format into theory-forge's internal structure
2. A documentation file that tells other commands how to work with this data
3. A registry entry so commands auto-discover the new source

## Arguments

- `$ARGUMENTS` - Name of the data source (e.g., "dedoose", "nvivo", "otter-ai")

If no argument provided, ask: "What data tool or format are you adding support for?"

## Prerequisites

None. This can run at any point. You don't need a project initialized.

---

## The Process

### Step 1: Understand the Source

Ask the contributor:

```
Tell me about the data source you want to add:

1. **Tool name**: What tool/format is this? (e.g., Dedoose, NVivo, Otter.ai)
2. **Export format**: What file format does it export? (e.g., CSV, JSON, XML, .qdpx, .nvp)
3. **Data type**: What kind of research data does it contain?
   - Coded qualitative data (interviews with codes/themes)
   - Raw transcripts (unstructured text)
   - Survey responses (structured + open-ended)
   - Field notes
   - Mixed (describe)
4. **Sample file**: Can you provide a sample export file? (Even a small one helps enormously)

If you have a sample file, place it somewhere I can read it and tell me the path.
```

### Step 2: Profile the Export Format

If a sample file is provided:
1. Read the file and analyze its structure
2. Identify: field names, data types, nesting, encoding
3. Map the source's structure to theory-forge's internal format (see below)
4. Note any lossy conversions or ambiguities

If no sample file:
1. Search the web for the tool's export format documentation
2. Identify the typical export structure
3. Note what's uncertain and flag it for testing

### Step 3: Map to Theory-Forge Internal Format

Theory-forge expects data in specific locations and structures:

**Quantitative data** → `data/quant/`
- CSV or Parquet files
- One row per observation
- Column names as variable names
- Metadata in a companion `_meta.json` if needed

**Qualitative data** → `data/qual/`
- **Transcripts**: `data/qual/interviews/` — one `.txt` or `.md` file per interview
  - Filename convention: `[informant-id]_[date].txt`
  - Content: plain text, speaker turns on separate lines if available
- **Field notes**: `data/qual/fieldnotes/` — one file per observation session
- **Coded data**: `data/qual/coded/` — preserves code assignments
  - JSON format per document:
    ```json
    {
      "source_file": "interview_01.txt",
      "source_tool": "dedoose",
      "codes": [
        {
          "code": "identity_work",
          "parent_code": "themes",
          "text": "The quoted passage that was coded",
          "start_char": 1245,
          "end_char": 1389,
          "memo": "Coder's annotation if any"
        }
      ],
      "metadata": {
        "coder": "researcher_1",
        "date_coded": "2025-01-15",
        "tool_version": "Dedoose 9.x"
      }
    }
    ```

**Survey data** → `data/quant/` (closed-ended) + `data/qual/surveys/` (open-ended responses)
- Split structured responses from free-text responses
- Preserve respondent IDs for linking

**References** → `literature/refs.bib` (BibTeX) or `literature/refs.json`

### Step 4: Generate the Importer

Create a Python importer at `tools/importers/[source_id].py`. Follow the pattern of the existing `tools/importers/bibtex.py`.

**Required importer structure:**

```python
"""
Theory-forge importer for [Source Name].

Converts [export format] exports into theory-forge's internal data structure.

Usage:
    python -m tools.importers.[source_id] <input_file> [--output-dir data/]

What it does:
    - Reads [format] files exported from [tool]
    - Normalizes to theory-forge directory structure
    - Preserves [what's preserved] and flags [what's lost]

What it doesn't do:
    - [Limitations]
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional


# --- Data classes ---

@dataclass
class ImportedDocument:
    """A single document/interview/transcript from the source."""
    id: str
    content: str
    source_file: str
    metadata: dict = field(default_factory=dict)


@dataclass
class ImportedCode:
    """A code assignment from coded qualitative data."""
    code: str
    text: str
    document_id: str
    parent_code: Optional[str] = None
    start_char: Optional[int] = None
    end_char: Optional[int] = None
    memo: Optional[str] = None


@dataclass
class ImportResult:
    """Result of an import operation."""
    source_tool: str
    source_file: str
    documents: list[ImportedDocument] = field(default_factory=list)
    codes: list[ImportedCode] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)


# --- Parser ---

def parse(input_path: Path) -> ImportResult:
    """Parse [format] file and return structured result."""
    result = ImportResult(
        source_tool="[tool_name]",
        source_file=str(input_path)
    )

    # TODO: Implement parsing logic specific to this format
    # Read the file, extract documents/codes, populate result

    return result


# --- Writer ---

def write_to_project(result: ImportResult, output_dir: Path) -> list[Path]:
    """Write parsed data to theory-forge project structure."""
    created_files = []

    # Write transcripts/documents
    qual_dir = output_dir / "data" / "qual" / "interviews"
    qual_dir.mkdir(parents=True, exist_ok=True)

    for doc in result.documents:
        out_path = qual_dir / f"{doc.id}.txt"
        out_path.write_text(doc.content, encoding="utf-8")
        created_files.append(out_path)

    # Write coded data (if any)
    if result.codes:
        coded_dir = output_dir / "data" / "qual" / "coded"
        coded_dir.mkdir(parents=True, exist_ok=True)

        # Group codes by document
        codes_by_doc = {}
        for code in result.codes:
            codes_by_doc.setdefault(code.document_id, []).append(code)

        for doc_id, codes in codes_by_doc.items():
            out_path = coded_dir / f"{doc_id}_codes.json"
            out_path.write_text(json.dumps({
                "source_file": f"{doc_id}.txt",
                "source_tool": result.source_tool,
                "codes": [asdict(c) for c in codes],
                "metadata": {
                    "imported_from": result.source_file,
                    "import_date": __import__("datetime").datetime.now().isoformat()
                }
            }, indent=2), encoding="utf-8")
            created_files.append(out_path)

    return created_files


# --- CLI ---

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python -m tools.importers.[source_id] <input_file> [--output-dir <dir>]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_dir = Path(".")

    if "--output-dir" in sys.argv:
        idx = sys.argv.index("--output-dir")
        output_dir = Path(sys.argv[idx + 1])

    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)

    print(f"Importing from {input_path}...")
    result = parse(input_path)

    print(f"  Found {len(result.documents)} documents, {len(result.codes)} code assignments")
    if result.warnings:
        print(f"  Warnings:")
        for w in result.warnings:
            print(f"    ⚠️  {w}")

    created = write_to_project(result, output_dir)
    print(f"  Wrote {len(created)} files to {output_dir}")

    # Print summary
    print(f"\nImport complete:")
    print(f"  Source: {result.source_tool}")
    print(f"  Documents: {len(result.documents)}")
    print(f"  Code assignments: {len(result.codes)}")
    print(f"  Files created: {len(created)}")


if __name__ == "__main__":
    main()
```

**IMPORTANT**: Adapt this template to the actual format. Don't generate a skeleton — generate a working importer based on what you learned in Steps 1-2. Fill in the `parse()` function with real parsing logic.

If you can't generate a fully working parser (e.g., no sample file, undocumented format), generate the best approximation you can and clearly mark `# TODO` sections that need testing.

### Step 5: Generate Documentation

Create a data source doc at `data_sources/[source_id].md`:

```markdown
# [Source Name] Data Source

## What This Is

Support for importing [format] exports from [tool name] into theory-forge projects.

## How to Use

### Step 1: Export from [Tool]

[Specific instructions for exporting from the tool — which menu, which options, which format to select]

### Step 2: Import into Theory-Forge

```bash
python -m tools.importers.[source_id] path/to/export_file.ext --output-dir .
```

### Step 3: Verify

Run `/explore-data` to confirm the imported data looks correct.

## What Gets Imported

| Source Field | Theory-Forge Location | Notes |
|---|---|---|
| [field] | data/qual/interviews/ | [notes] |
| [field] | data/qual/coded/ | [notes] |

## What Gets Lost

- [Anything that doesn't survive the conversion]
- [Format-specific features that theory-forge doesn't support yet]

## Known Limitations

- [Limitation 1]
- [Limitation 2]

## Tested With

- [Tool version(s) tested against]
- [Export format version(s)]

## Contributing Improvements

If this importer doesn't handle your export correctly:
1. Open an issue with a sample file (anonymized if needed)
2. Describe what went wrong
3. Or fix it yourself and submit a PR — the importer is at `tools/importers/[source_id].py`
```

### Step 6: Register in Registry

Read `registry.json` from the project root and add an entry to the `data_sources` array:

```json
{
  "id": "[source_id]",
  "name": "[Human-readable name]",
  "format": "[File format description]",
  "type": "[quantitative|qualitative|references|mixed]",
  "importer": "tools/importers/[source_id].py",
  "doc": "data_sources/[source_id].md",
  "builtin": false,
  "notes": "[Brief description]"
}
```

Write the updated `registry.json` back.

### Step 7: Create the data_sources Directory (If Needed)

If `data_sources/` doesn't exist at the project root, create it. This is where all data source documentation lives.

### Step 8: Test

If the contributor provided a sample file:
1. Run the importer against it
2. Verify the output files are in the right locations
3. Verify the output format matches theory-forge's expectations
4. Run `/explore-data` to confirm the data is discoverable

If no sample file:
1. Tell the contributor what to test
2. Provide exact commands to run
3. Describe what correct output should look like

### Step 9: Review with Contributor

Show the contributor:

```
Here's what I've created:

1. **Importer**: `tools/importers/[source_id].py`
   - Reads: [format]
   - Writes: [what and where]
   - [Notable design decisions]

2. **Documentation**: `data_sources/[source_id].md`
   - Export instructions for [tool]
   - Import instructions
   - Known limitations

3. **Registry entry** in `registry.json`

To test: [specific test command]

To contribute upstream: Copy these three files into a theory-forge fork and open a PR.

Questions:
- Does the export instruction match how [tool] actually works?
- Are there edge cases in your data I should handle?
- Anything missing from the documentation?
```

---

## Design Principles

1. **Lossless where possible**: Preserve everything the source provides. Flag what's lost.
2. **Fail loudly**: If the importer can't parse something, error with a helpful message — don't silently skip data.
3. **Idempotent**: Running the importer twice on the same file should produce the same result (overwrite, don't duplicate).
4. **No dependencies beyond stdlib**: Importers should work with just Python 3.9+. If a format genuinely requires a library (e.g., lxml for XML), note it clearly.
5. **Test with real data**: A working importer tested on fake data is less useful than a partial importer tested on real data.

## After You're Done

Tell the contributor:
- What files were created and where
- How to test the importer
- How to contribute it upstream (copy files → fork → PR)
- What's missing or uncertain (if anything)

Remind them: the best importers come from people who actually use the tool. If the importer doesn't handle their specific export correctly, they should fix it — they know the format better than anyone.
