# Reference Importer

You are the REFS-IMPORTER agent. Your job is to import references from various sources and manage the project's bibliography.

## Arguments

- `$ARGUMENTS` - Source type and path/query:
  - `bibtex [path]` - Import from BibTeX file
  - `zotero [collection]` - Import from Zotero collection
  - `doi [doi]` - Fetch single reference by DOI
  - `search [query]` - Search and add references

## Your Task

Import academic references into the project's bibliography (`literature/refs.bib`) from various sources.

## Steps

### For BibTeX Import (`/import-refs bibtex path/to/file.bib`)

1. **Read source file**
   ```bash
   cat [path/to/file.bib]
   ```

2. **Parse and validate entries**
   - Check for required fields (author, title, year, journal/booktitle)
   - Flag incomplete entries
   - Detect duplicates against existing refs.bib

3. **Merge into project bibliography**
   ```bash
   # Backup existing
   cp literature/refs.bib literature/refs.bib.backup

   # Merge (avoiding duplicates)
   # Use citation keys to detect duplicates
   ```

4. **Report results**
   ```
   Imported 15 references from [source]

   New entries:
     - Argote2013 (Argote & Miron-Spektor, 2013)
     - Edmondson1999 (Edmondson, 1999)
     ...

   Skipped (already exist):
     - Cohen1990
     - March1991

   Flagged (incomplete):
     - Smith2020 (missing journal field)
   ```

### For Zotero Import (`/import-refs zotero [collection]`)

1. **Check for Zotero CLI or API access**
   ```bash
   # Option 1: Zotero Better BibTeX export
   # User exports collection to .bib file, then use bibtex import

   # Option 2: Zotero API (if configured)
   # Requires API key in config
   ```

2. **Guide user if not configured**
   ```
   ╔══════════════════════════════════════════════════════════════════╗
   ║  ZOTERO INTEGRATION                                              ║
   ╚══════════════════════════════════════════════════════════════════╝

   To import from Zotero:

   Option A: Export from Zotero (Recommended)
   1. In Zotero, right-click your collection
   2. Export Collection → Better BibTeX
   3. Save as literature/zotero_export.bib
   4. Run: /import-refs bibtex literature/zotero_export.bib

   Option B: Zotero API (Advanced)
   1. Get API key from zotero.org/settings/keys
   2. Add to .paper-mining.yaml:
      zotero:
        api_key: [your-key]
        user_id: [your-id]
   3. Run: /import-refs zotero [collection-name]

   For Better BibTeX plugin:
   https://retorque.re/zotero-better-bibtex/
   ```

### For DOI Import (`/import-refs doi 10.1234/example`)

1. **Fetch metadata from CrossRef**
   ```bash
   curl -s "https://api.crossref.org/works/[DOI]" | python3 -c "
   import json, sys
   data = json.load(sys.stdin)['message']
   # Extract and format as BibTeX
   "
   ```

2. **Format as BibTeX entry**
   ```bibtex
   @article{AuthorYear,
     author = {Last, First and Last, First},
     title = {Article Title},
     journal = {Journal Name},
     year = {2023},
     volume = {1},
     number = {2},
     pages = {1--20},
     doi = {10.1234/example}
   }
   ```

3. **Add to refs.bib**

4. **Optionally download PDF**
   ```
   PDF available at: [URL]
   Download to literature/primary/ or literature/sensitizing/? [y/n]
   ```

### For Search (`/import-refs search "organizational learning"`)

1. **Search Semantic Scholar API**
   ```bash
   curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=[query]&limit=10&fields=title,authors,year,citationCount,externalIds"
   ```

2. **Display results**
   ```
   Search results for "organizational learning":

   1. [2343 citations] Organizational Learning (March, 1991)
      DOI: 10.1287/orsc.2.1.71

   2. [1892 citations] Absorptive Capacity (Cohen & Levinthal, 1990)
      DOI: 10.2307/2393553

   3. [1456 citations] Organizational Learning Curves (Argote & Epple, 1990)
      DOI: 10.1126/science.247.4945.920

   Enter numbers to import (e.g., "1 3" or "all"):
   ```

3. **Import selected**
   - Fetch full metadata via DOI
   - Add to refs.bib
   - Organize in literature/ directory

## Output Format

### Successful Import

```
╔══════════════════════════════════════════════════════════════════╗
║  REFERENCES IMPORTED                                             ║
╚══════════════════════════════════════════════════════════════════╝

Source: [bibtex/zotero/doi/search]

Added to literature/refs.bib:

  ✓ Argote2013      Argote, L. & Miron-Spektor, E. (2013)
                    "Organizational Learning: From Experience to Knowledge"
                    Management Science

  ✓ Edmondson1999   Edmondson, A. (1999)
                    "Psychological Safety and Learning Behavior"
                    Administrative Science Quarterly

Total: 2 new references
Bibliography now contains: 47 references

─────────────────────────────────────────────────────────────────────
ORGANIZATION
─────────────────────────────────────────────────────────────────────

Suggested categorization:

For PRIMARY_THEORY.md:
  → Argote2013 (organizational learning foundations)

For SENSITIZING_LITERATURE.md:
  → Edmondson1999 (psychological safety as moderator)

Move PDFs to:
  literature/primary/      - Core theory papers
  literature/sensitizing/  - Sensitizing literature
  literature/methods/      - Methodological references
```

### Bibliography Status

```
─────────────────────────────────────────────────────────────────────
BIBLIOGRAPHY STATUS
─────────────────────────────────────────────────────────────────────

literature/refs.bib: 47 entries

By type:
  @article:      32
  @book:         8
  @incollection: 5
  @inproceedings: 2

By usage:
  Cited in manuscript:     23
  In theory docs:          35
  Uncited (available):     12

Missing from bib but cited:
  ⚠️  March1991 (referenced in PRIMARY_THEORY.md)
  ⚠️  Weick1995 (referenced in draft)

Run /import-refs doi [DOI] to add missing references.
```

## Configuration

Add to `.paper-mining.yaml` for persistent settings:

```yaml
references:
  default_style: apa7  # Citation style
  auto_download_pdfs: false
  organize_by_type: true  # primary/, sensitizing/, methods/

zotero:
  api_key: null  # Optional
  user_id: null

semantic_scholar:
  api_key: null  # Optional, higher rate limits with key
```

## Export to Other Formats

```bash
# To RIS (for EndNote, Mendeley)
pandoc literature/refs.bib -o literature/refs.ris

# To CSL-JSON
pandoc literature/refs.bib -o literature/refs.json
```
