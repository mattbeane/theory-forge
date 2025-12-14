# Living Paper (Bundled)

This is a bundled copy of [Living Paper](https://github.com/mattbeane/living-paper) for seamless integration with paper-mining-agent-suite.

## What This Does

Creates a verification layer linking claims to evidence without exposing protected data.

## Usage

These commands are run automatically by `/verify-claims`. You shouldn't need to run them manually.

```bash
python3 living_paper/lp.py init
python3 living_paper/lp.py ingest --claims ... --evidence ... --links ...
python3 living_paper/lp.py lint
python3 living_paper/lp.py export-package --paper PAPER_ID --out ./reviewer_package
```

## Updating

To update to the latest version:

```bash
# From paper-mining-agent-suite root
rm -rf living_paper/
git clone https://github.com/mattbeane/living-paper.git /tmp/lp-update
cp /tmp/lp-update/{lp.py,redact.py,*.sql,datasets.yaml,entities_example.yaml} living_paper/
rm -rf /tmp/lp-update
```

## Full Documentation

See the [Living Paper repo](https://github.com/mattbeane/living-paper) for complete documentation.
