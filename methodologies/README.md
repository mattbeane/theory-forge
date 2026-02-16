# Methodologies

This directory contains documentation for each methodological tradition registered in theory-forge.

## Built-in Methodologies

| ID | Name | Rubric | Eval Command |
|---|---|---|---|
| `theory-violation` | Zuckerman's 10 Criteria | `rubrics/zuckerman_criteria.json` | `/eval-zuckerman` |
| `theory-elaboration` | Fisher & Aguinis | Inline in `/eval-contribution` | — |
| `phenomenon-description` | Weick | Inline in `/eval-contribution` | — |
| `methodological` | Abbott | Inline in `/eval-contribution` | — |
| `practical-insight` | Corley & Gioia | Inline in `/eval-contribution` | — |
| `literature-integration` | Palmatier et al. | Inline in `/eval-contribution` | — |
| `paper-quality` | General Quality | `rubrics/paper_quality.json` | `/eval-paper-quality` |
| `claim-verification` | Claim-Evidence Integrity | `rubrics/claim_verification.json` | — |
| `qual-inductive` | Qualitative Inductive | `rubrics/qual_inductive_criteria.json` | — |

## Adding a New Methodology

Run `/author-methodology [tradition-name]` to generate:
1. An evaluation rubric at `rubrics/[name].json`
2. An eval command at `.claude/commands/eval-[name].md`
3. A documentation file in this directory
4. A registry entry in `registry.json`

See the [Contributing section](../README.md#contributing-add-your-own-data-sources--methodologies) in the README.
