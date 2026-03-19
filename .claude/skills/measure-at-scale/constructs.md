## Constructs for Measurement

| Construct | Definition | Source | What to Look For | Scale |
|-----------|-----------|--------|-------------------|-------|
| [name] | [operational definition] | /mine-qual, Hypothesis 3 | [observable indicators] | 0-100 / binary / categorical |
| [name] | [operational definition] | /style-engine, Framing 2 | [observable indicators] | 0-100 / binary / categorical |
```

For each construct, define:
- **Operational definition**: What does this construct mean in concrete terms?
- **Observable indicators**: What words, phrases, descriptions, or behaviors indicate this construct?
- **Scale type**: Binary (present/absent), categorical (types), or continuous (0-100 intensity)
- **Disconfirmation criteria**: What would indicate this construct is NOT present?

**Critical**: The constructs must come from YOUR prior analysis, not from this skill inventing new ones. this skill *measures*; it does not *discover*.

### 2. Choose measurement approach

Two approaches available, depending on corpus size:

#### A. Direct measurement (for corpora ≤ 50 documents)

Measure each document within Claude's context window:
- Read each document
- Rate each construct per the specification
- Output structured ratings

#### B. GABRIEL export (for larger corpora or when inter-rater validation is needed)

Generate a GABRIEL-compatible measurement specification:

```python
# Generated GABRIEL measurement spec
# Install: pip install openai-gabriel
# Requires: OPENAI_API_KEY environment variable

import gabriel
import pandas as pd

# Load your data
df = pd.read_csv("data/qual/corpus_index.csv")
# Expected columns: doc_id, text (or file_path)

# Rate constructs
results = gabriel.rate(
    df,
    text_column="text",
    attributes={
        "[construct_1]": "[operational definition and indicators]",
        "[construct_2]": "[operational definition and indicators]",
    },
    scale="0-100",
    additional_instructions="[context about the research setting]",
)

# Classify categories
categories = gabriel.classify(
    df,
    text_column="text",
    categories={
        "[category_1]": "[definition]",
        "[category_2]": "[definition]",
        "[category_3]": "[definition]",
    },
    additional_instructions="[context]",
)
```

Save the generated spec to `analysis/measurement/gabriel_spec.py`.

### 3. Execute measurement

**For direct measurement:**

For each document in the corpus:
1. Read the full document
2. For each construct, rate according to the specification
3. Record: document ID, construct scores, key passages supporting the rating, confidence level

**Important rules for rating:**
- Rate EVERY document, not just ones that seem relevant
- Record a 0 / "absent" / "none" when a construct doesn't appear — zeros are data
- Note ambiguous cases explicitly — don't force a rating when the evidence is unclear
- Track which passages informed each rating (for verification)

### 4. Compute distributions

For each construct:
- Mean/median/SD (continuous scales)
- Frequency counts (binary/categorical)
- Distribution shape (normal? bimodal? skewed?)
- Missing/ambiguous rate

Cross-tabulate by available metadata:
- By informant role
- By site/location
- By time period
- By any other relevant grouping

### 5. Compare to qualitative findings

For each construct, compare the measurement distribution to the qualitative evidence:

| Construct | Qual Evidence (from /mine-qual) | Scale Measurement | Consistent? |
|-----------|-------------------------------|-------------------|-------------|
| [name] | "Strong support, 8 quotes" | Present in 73% of interviews, mean intensity 62/100 | ✓ Consistent |
| [name] | "Mixed, 3 support / 2 challenge" | Present in 41% of interviews, mean intensity 38/100 | ✓ Mixed confirmed |
| [name] | "Strong support, 6 quotes" | Present in only 22% of interviews | ⚠️ Possible cherry-picking |

**Flag mismatches** where:
- Qualitative analysis says "strong support" but measurement shows <40% prevalence
- Qualitative analysis says "challenging" but measurement shows >70% prevalence
- Distribution is bimodal (suggesting an unmeasured moderator)

### 6. Generate evidence for methods section

Produce measurement validity evidence:

**Internal consistency**: If multiple indicators per construct, report correlation between indicators.

**Prompt sensitivity** (if using GABRIEL or running multiple times): Does the exact wording of the construct definition change results? Report variance across prompt variations.

**Human-LLM agreement** (recommended): Select 20-30 documents, have the researcher rate them manually, compare to LLM ratings. Report agreement metrics (Cohen's kappa for binary, ICC for continuous).

### 7. Feed back to audit-claims

The measurement results should inform `/audit-claims`:
- Claims about pervasiveness can now cite measurement data
- Boundary conditions become visible through subgroup variation
- Alternative interpretations emerge from unexpected distributions
