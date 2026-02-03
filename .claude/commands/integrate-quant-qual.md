# Integrate Quantitative and Qualitative Evidence

You are the INTEGRATION agent. Your job is to systematically connect quantitative patterns with qualitative mechanisms, identifying where evidence converges and where gaps exist.

## Why This Matters

Mixed-methods papers often bolt quant and qual together without true integration:
- Quant section finds patterns
- Qual section describes mechanisms
- Discussion vaguely gestures at connection
- Reviewers ask: "How do these actually relate?"

True integration means:
- Quant patterns identify WHAT happens and for WHOM
- Qual mechanisms explain WHY and HOW
- Each informs sampling/focus of the other
- Convergence strengthens claims; divergence reveals boundary conditions

## When to Run This

Run this AFTER both `/hunt-patterns` and `/mine-qual` have completed. You need:
- Quantitative pattern report with identified heterogeneity
- Qualitative mechanism report with coded evidence

This is the "translation point" between the two analyses.

## Prerequisites

Before starting, check `state.json`:
1. `workflow.hunt_patterns.status === "completed"`
2. `workflow.mine_qual.status === "completed"`

If either is incomplete, inform the user and suggest running that command first.

## The Integration Framework

### Level 1: Pattern-Mechanism Mapping

For each quantitative pattern, ask:
- Which qualitative mechanism(s) could explain it?
- Does the mechanism evidence match the pattern's heterogeneity?

For each qualitative mechanism, ask:
- Which quantitative pattern(s) does it explain?
- Does the pattern support the mechanism's proposed effect?

### Level 2: Convergence Analysis

Where do quant and qual point to the same conclusion?
- Strong convergence: Pattern X is explained by Mechanism Y, with consistent evidence
- Weak convergence: Pattern X might be explained by Mechanism Y, but evidence is thin

Where do they diverge?
- Unexplained patterns: Quant finding with no qualitative mechanism
- Unsupported mechanisms: Qual mechanism with no quantitative footprint
- Contradictions: Quant and qual point opposite directions

### Level 3: Gap Analysis

What's missing?
- Patterns needing mechanism evidence
- Mechanisms needing quantitative support
- Subgroups in quant not represented in qual
- Informant perspectives in qual not captured in quant

## Steps

### Step 1: Inventory Both Analyses

**From Pattern Report** (`analysis/patterns/PATTERN_REPORT.md`):
- List all robust patterns with effect sizes
- Note heterogeneity (who shows effect, who doesn't)
- Note any killed patterns (why they died)

**From Mechanism Report** (`analysis/mechanisms/MECHANISM_REPORT.md` or `/mine-qual` output):
- List all identified mechanisms
- Note supporting and challenging evidence counts
- Note informant roles/sites represented

### Step 2: Build the Mapping Matrix

Create a matrix mapping patterns to mechanisms:

```
                    | Mechanism A | Mechanism B | Mechanism C | No Mechanism
--------------------|-------------|-------------|-------------|-------------
Pattern 1 (strong)  |     ?       |     ?       |     ?       |
Pattern 2 (moderate)|     ?       |     ?       |     ?       |
Pattern 3 (hetero)  |     ?       |     ?       |     ?       |
No Pattern          |     ?       |     ?       |     ?       |
```

For each cell, assess:
- **✓ Strong link**: Mechanism clearly explains pattern; evidence converges
- **~ Partial link**: Mechanism might explain pattern; evidence thin
- **✗ No link**: Mechanism doesn't relate to pattern
- **? Unknown**: Haven't checked yet

### Step 3: Analyze Convergence

For each Pattern-Mechanism pair marked ✓ or ~:
- What evidence connects them?
- Does the mechanism operate for the same subgroups showing the pattern?
- Are there alternative mechanisms that could explain the pattern?

### Step 4: Analyze Divergence

**Unexplained Patterns** (Pattern row with all ✗):
- Why might this pattern lack mechanism evidence?
- Do we have qual data from the right informants?
- Is this pattern spurious?

**Unsupported Mechanisms** (Mechanism column with all ✗):
- Why might this mechanism lack quantitative support?
- Is it too context-specific to show in aggregate?
- Is it real but rare?

**Contradictions** (Quant and qual point opposite ways):
- Pattern suggests X, but mechanism suggests ¬X
- This is potentially the most interesting finding!
- Investigate: Is this a boundary condition? Measurement error? Different constructs?

### Step 5: Identify Gaps

**Sampling gaps in qual**:
- Which quant subgroups are underrepresented in qual?
- E.g., Pattern strongest for Group A, but qual mostly interviews Group B

**Variable gaps in quant**:
- Which mechanism-relevant factors aren't in the quant data?
- E.g., Mechanism involves "informal mentoring" but quant has no measure

**Temporal gaps**:
- When do patterns manifest vs. when were interviews conducted?
- E.g., Pattern appears in Year 3+, but interviews conducted Year 1

### Step 6: Generate Integration Claims

For each strong convergence, draft an integrated claim:

"[Pattern X] appears in the quantitative data (β = Y, p < Z). Qualitative analysis reveals that [Mechanism A] drives this effect. [Specific quote/evidence] illustrates how [mechanism operates]. This effect is strongest for [subgroup], consistent with the mechanism's emphasis on [factor]."

## Output Format

Create `analysis/integration/INTEGRATION_REPORT.md`:

```markdown
# Quantitative-Qualitative Integration Report

**Date**: [Date]
**Pattern Report**: analysis/patterns/PATTERN_REPORT.md
**Mechanism Report**: analysis/mechanisms/MECHANISM_REPORT.md

---

## Executive Summary

**Patterns identified**: [N]
**Mechanisms identified**: [N]
**Strong convergences**: [N] - [List briefly]
**Divergences requiring attention**: [N] - [List briefly]
**Critical gaps**: [N] - [List briefly]

---

## Pattern-Mechanism Mapping Matrix

|                     | Mech A: [Name] | Mech B: [Name] | Mech C: [Name] | No Mechanism |
|---------------------|----------------|----------------|----------------|--------------|
| Pattern 1: [Name]   | ✓ Strong       | ✗              | ~ Partial      |              |
| Pattern 2: [Name]   | ~ Partial      | ✓ Strong       | ✗              |              |
| Pattern 3: [Name]   | ✗              | ✗              | ✗              | ⚠️ Gap       |
| No Pattern          |                | ⚠️ Gap         |                |              |

**Legend**:
- ✓ Strong: Clear explanatory link with convergent evidence
- ~ Partial: Possible link, needs more evidence
- ✗ No link: Not related
- ⚠️ Gap: Pattern without mechanism OR mechanism without pattern

---

## Strong Convergences

### Convergence 1: [Pattern Name] ↔ [Mechanism Name]

**Quantitative evidence**:
- Effect size: [β, OR, difference]
- Statistical significance: [p-value]
- Heterogeneity: [Who shows effect vs. who doesn't]

**Qualitative evidence**:
- Mechanism: [Brief description]
- Supporting quotes: [N]
- Challenging quotes: [N]
- Key informant roles: [Who describes this mechanism]

**Alignment check**:
- ✓ Mechanism operates for same subgroups showing pattern: [Yes/No]
- ✓ Mechanism timing matches pattern timing: [Yes/No]
- ✓ Mechanism direction matches pattern direction: [Yes/No]

**Integrated claim** (draft):
> "[Pattern X] appears robustly in the quantitative data (β = Y). Qualitative evidence suggests [Mechanism A] drives this effect. As [Informant] described: '[Brief quote]'. This mechanism operates primarily among [subgroup], consistent with the quantitative finding that the effect is [stronger/weaker] for this group."

**Remaining questions**:
- [Question about the connection]

---

### Convergence 2: [Pattern Name] ↔ [Mechanism Name]

[Same structure]

---

## Partial Convergences (Need Strengthening)

### Partial 1: [Pattern Name] ↔ [Mechanism Name]

**Current state**: [Why partial—thin evidence, inconsistent subgroups, timing mismatch, etc.]

**What would strengthen this**:
1. [Specific evidence needed from qual]
2. [Specific analysis needed from quant]
3. [Specific informant type needed]

**Action items**:
- [ ] [Specific action]
- [ ] [Specific action]

---

## Unexplained Patterns (Quant without Qual)

### Pattern: [Name]

**Quantitative finding**: [Description with effect size]

**Why unexplained?**:
- [ ] No mechanism hypothesized
- [ ] Mechanism hypothesized but no qual evidence found
- [ ] Qual data doesn't cover relevant informants
- [ ] Other: [Explain]

**Possible mechanisms to investigate**:
1. [Candidate mechanism + why plausible]
2. [Candidate mechanism + why plausible]

**Action items**:
- [ ] [Specific action—e.g., "Interview 3 more workers from Site B"]
- [ ] [Specific action]

---

## Unsupported Mechanisms (Qual without Quant)

### Mechanism: [Name]

**Qualitative evidence**: [Description with evidence counts]

**Why no quantitative support?**:
- [ ] No relevant variable in quant data
- [ ] Effect too context-specific to aggregate
- [ ] Mechanism rare but impactful
- [ ] Possible measurement error
- [ ] Other: [Explain]

**Possible quant tests**:
1. [What analysis might capture this—even imperfectly]
2. [Proxy variable that might work]

**Decision**:
- [ ] Include in paper as qual-only mechanism (acknowledge limitation)
- [ ] Attempt quant proxy analysis
- [ ] Drop mechanism—evidence too thin

---

## Contradictions (Quant and Qual Diverge)

### Contradiction 1: [Brief description]

**Quantitative finding**: [X]

**Qualitative finding**: [Opposite or inconsistent with X]

**Possible explanations**:
1. **Boundary condition**: [Quant captures A; qual captures B; they're both right for different groups]
2. **Measurement issue**: [Quant variable doesn't capture qual construct well]
3. **Selection effect**: [Qual informants differ from quant sample]
4. **Temporal difference**: [Quant is cross-sectional; qual captures process]
5. **Construct confusion**: [Quant and qual actually measuring different things]

**Investigation needed**:
- [ ] [Specific check—e.g., "Re-run quant for subgroup matching qual informants"]
- [ ] [Specific check]

**Resolution strategy**:
[How to handle this in the paper—boundary condition? Limitation? Drop one finding?]

---

## Sampling and Coverage Gaps

### Qualitative Coverage of Quantitative Subgroups

| Quant Subgroup | N in Quant | Effect Size | Qual Interviews | Coverage |
|----------------|------------|-------------|-----------------|----------|
| Group A        | 150        | β = 0.3     | 12              | ✓ Good   |
| Group B        | 80         | β = -0.1    | 2               | ⚠️ Thin  |
| Group C        | 45         | β = 0.5     | 0               | ✗ None   |

**Gap implications**:
- [Group C shows strongest effect but has no qual coverage—can't explain mechanism]

### Quantitative Coverage of Qualitative Mechanisms

| Qual Mechanism | Supporting Quotes | Quant Variable Available | Coverage |
|----------------|-------------------|--------------------------|----------|
| Mechanism A    | 15                | Yes (direct)             | ✓ Good   |
| Mechanism B    | 8                 | Yes (proxy)              | ~ Partial|
| Mechanism C    | 12                | No                       | ✗ None   |

**Gap implications**:
- [Mechanism C is well-supported in qual but can't be tested quantitatively]

---

## Integrated Claims Summary

Ready-to-use claims that integrate quant and qual:

### Claim 1: [Title]

> [Full integrated claim with quant evidence, qual mechanism, and acknowledgment of limitations]

**Strength**: [Strong / Moderate / Tentative]
**Limitation**: [What weakens this claim]

---

### Claim 2: [Title]

[Same structure]

---

## Action Items Before Proceeding

### High Priority (Must address):
1. [ ] [Gap that undermines core claims]
2. [ ] [Contradiction that needs resolution]

### Medium Priority (Should address):
3. [ ] [Partial convergence that could be strengthened]
4. [ ] [Unexplained pattern that reviewers will notice]

### Low Priority (Nice to have):
5. [ ] [Additional analysis for robustness]

---

## Recommendations for Paper Structure

Based on integration analysis, recommend:

**Lead with**: [Pattern X + Mechanism Y convergence—strongest evidence]

**Supporting claims**: [Other convergences in order of strength]

**Acknowledge as limitations**:
- [Unexplained pattern Z]
- [Unsupported mechanism Q]

**Handle in boundary conditions discussion**:
- [Contradiction resolved as boundary condition]

---

## Next Steps

Recommended commands:
1. `/verify-claims` — Now that claims integrate quant and qual, verify them
2. `/audit-claims` — If not already run, audit integrated claims against raw data
3. `/draft-paper` — If integration is satisfactory, proceed to drafting
```

---

## After You're Done

Tell the user:
1. How many strong convergences were found
2. Which patterns lack mechanism evidence (and what to do about it)
3. Which mechanisms lack quantitative support (and what to do about it)
4. Any contradictions discovered and how to resolve them
5. Specific action items before proceeding to drafting

## Integration with Other Commands

- Run AFTER `/hunt-patterns` and `/mine-qual`
- Run BEFORE `/verify-claims` to ensure claims integrate both streams
- Run BEFORE `/draft-paper` to structure mixed-methods narrative
- If gaps are critical, may need to return to data collection or rerun `/mine-qual` with different focus

## Common Problems

**"Ships passing in the night"**: Quant and qual analyze different questions, making integration impossible. Fix: Ensure both address the same core phenomenon; may need to refocus one analysis.

**"Qual as illustration"**: Qual used only to put a human face on quant numbers, not to explain mechanisms. Fix: Qual should reveal WHY patterns exist, not just THAT they do.

**"Quant as validation"**: Quant used only to show qual findings are "real," not to identify heterogeneity. Fix: Quant should identify WHO shows the effect and WHO doesn't.

**"Sequential but not integrated"**: Paper presents quant, then qual, then discussion that waves at both. Fix: Explicit integration section showing where evidence converges/diverges.

## State Management

After completing:
1. Update `state.json`:
   - Set `workflow.integrate_quant_qual.status` to "completed"
   - Set `workflow.integrate_quant_qual.completed_at` to current ISO timestamp
   - Add output file paths to `workflow.integrate_quant_qual.outputs`
   - Update `updated_at` timestamp
2. Append entry to `DECISION_LOG.md`
