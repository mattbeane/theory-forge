# Paper Extraction Schema

This schema defines the structure for extracting information from qualitative management papers. Used both for manual coding (Phase 1 calibration) and agent-assisted extraction.

---

## Paper Metadata

| Field | Description | Example |
|-------|-------------|---------|
| `citation` | Full APA citation | Edmondson, A. C. (1999). Psychological safety... |
| `journal` | Publication venue | Administrative Science Quarterly |
| `paper_type` | Inductive/Deductive/Mixed | Inductive |
| `empirical_setting` | Site(s) and context | 51 work teams across manufacturing firm |

---

## Core Extraction Fields

### 1. Empirical Pattern(s)

**Definition**: The observable regularity or finding the paper establishes.

**Not**: The theoretical claim or contribution—just what they found in the data.

| Subfield | Description |
|----------|-------------|
| `pattern_statement` | One-sentence description of what varies with what |
| `direction` | Positive/negative/curvilinear/conditional |
| `robustness` | How many ways is this pattern supported? |
| `boundary_conditions` | When does the pattern NOT hold? |

**Example**:
```
pattern_statement: "Teams with higher psychological safety exhibited higher learning behaviors"
direction: positive
robustness: Replicated across 51 teams; robust to multiple controls
boundary_conditions: Measured in hospital context; may not generalize to other settings
```

**Common Errors**:
- Conflating the pattern with the proposed explanation
- Over-stating robustness (the paper claims more than the data support)
- Missing key boundary conditions

---

### 2. Theoretical Violation

**Definition**: What prior theory would have predicted differently, and why this finding is surprising.

| Subfield | Description |
|----------|-------------|
| `violated_theory` | Name/cite the theory being challenged |
| `expected_prediction` | What would that theory have predicted? |
| `actual_finding` | How does the pattern contradict this? |
| `stakes` | Why does this matter? |

**Example**:
```
violated_theory: "Social loafing theory (Latané et al., 1979)"
expected_prediction: "Larger teams should show lower individual effort"
actual_finding: "Team psychological safety moderates this—high-safety large teams maintained effort"
stakes: "Suggests team climate can override structural disincentives"
```

**Common Errors**:
- Naming a vague "literature" instead of a specific prediction
- Choosing a straw-man theory that no one actually believed
- Overstating how surprising the finding is

---

### 3. Proposed Mechanism(s)

**Definition**: The causal pathway the paper proposes to explain WHY the pattern occurs.

| Subfield | Description |
|----------|-------------|
| `mechanism_name` | Short label for the mechanism |
| `mechanism_description` | How does it work? (1-2 sentences) |
| `type` | Behavioral/cognitive/relational/structural |
| `evidence_strength` | Strong/moderate/weak/theorized only |

**Example**:
```
mechanism_name: "Risk tolerance via blame reduction"
mechanism_description: "Psychological safety reduces perceived interpersonal risk of speaking up, enabling learning behaviors that would otherwise be self-censored"
type: cognitive/relational
evidence_strength: moderate (interview evidence supports; not directly measured)
```

**Common Errors**:
- Confusing correlation for mechanism (X and Y co-occur ≠ X causes Y)
- Accepting theorized mechanisms as established
- Missing alternative mechanisms the authors don't consider

---

### 4. Key Supporting Quotes

**Definition**: Direct quotes from the paper that support key claims.

| Subfield | Description |
|----------|-------------|
| `quote_text` | Exact text, in quotation marks |
| `page_number` | Page where quote appears |
| `quote_function` | What claim does this support? |
| `context` | What surrounds this quote? (important!) |

**Example**:
```
quote_text: "In teams where members trusted one another, individuals reported greater willingness to take interpersonal risks"
page_number: 354
quote_function: Supports psychological safety → learning behavior link
context: From Results section; precedes statistical analysis
```

**Common Errors**:
- Quoting out of context (changing meaning)
- Missing that the quote is from a literature review, not findings
- Selecting quotes that sound good but don't actually support the claim

---

### 5. Methodological Approach

**Definition**: How the paper generated and analyzed data.

| Subfield | Description |
|----------|-------------|
| `data_type` | Interview/observation/survey/archival/mixed |
| `sample` | N, sampling strategy, site description |
| `analysis_approach` | Grounded theory/template analysis/regression/etc. |
| `validity_strategies` | Member checking, triangulation, etc. |

**Example**:
```
data_type: mixed (survey + interview)
sample: 51 teams, 427 individuals; convenience sample from single firm
analysis_approach: Hierarchical regression for quantitative; template analysis for qualitative
validity_strategies: Multiple coders; member checking with subset of participants
```

**Common Errors**:
- Accepting stated method at face value (does the analysis actually match?)
- Missing important limitations the authors downplay
- Overstating generalizability

---

### 6. Contribution Claim

**Definition**: What the paper claims to add to knowledge.

| Subfield | Description |
|----------|-------------|
| `contribution_statement` | What does the paper claim to add? |
| `contribution_type` | Theory-building/theory-testing/phenomenon/method |
| `to_what_literature` | Which conversation is this joining? |
| `your_assessment` | Does the evidence support this contribution? |

**Example**:
```
contribution_statement: "Introduces psychological safety as team-level construct explaining learning behavior variance"
contribution_type: theory-building
to_what_literature: Team learning; organizational learning
your_assessment: Strong—construct has clear definition, discriminant validity shown, mechanism theorized and partially evidenced
```

---

## Validation Checklist

After completing extraction, verify:

- [ ] Pattern statement is purely empirical (no theoretical language)
- [ ] Theoretical violation cites a specific, credible prior prediction
- [ ] Mechanisms are distinguished from correlations
- [ ] All quotes verified against source (page numbers checked)
- [ ] Method description matches what the paper actually did
- [ ] Your assessment of contribution is honest, not just restating authors' claims

---

## Adding New Fields

When proposing schema extensions (Phase 3), include:

1. **Field name and definition**
2. **Subfields with descriptions**
3. **At least 3 worked examples**
4. **Common errors for this field**
5. **Validation criteria**

Submit as PR to this file with your examples in a separate document.
