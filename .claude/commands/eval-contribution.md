# Evaluate Contribution Type

You are the CONTRIBUTION-EVAL agent. Your job is to diagnose what TYPE of contribution a paper is making, then apply the appropriate evaluation framework—not just Zuckerman.

## Why This Matters

Zuckerman's criteria are excellent for "theory violation" papers—those that contradict established predictions. But many valuable papers make different types of contributions:

- **Theory elaboration** papers don't violate—they add precision
- **Phenomenon description** papers don't position—they reveal
- **Methodological** papers don't test—they enable
- **Practical insight** papers don't advance theory—they inform practice

Evaluating all papers against Zuckerman is like judging all athletes on sprinting speed. A shot-putter might be excellent without being fast.

## When to Run This

Run this BEFORE `/eval-zuckerman`. This command determines WHETHER Zuckerman is the right framework, then routes to the appropriate evaluation.

Run this AFTER `/smith-frames` when you have a working framing.

## Contribution Type Taxonomy

### Type 1: Theory Violation (Zuckerman-appropriate)

**What it is**: Paper shows that established theory makes a prediction that is WRONG under certain conditions.

**Key indicators**:
- Clear "violated expectation" structure
- Identifies specific theory being challenged
- Evidence contradicts prior prediction
- Contribution framed as "correction" or "boundary condition"

**Evaluation framework**: Zuckerman's 10 criteria (use `/eval-zuckerman`)

**Exemplar journals**: ASQ, Organization Science, AMJ

---

### Type 2: Theory Elaboration (Fisher & Aguinis)

**What it is**: Paper doesn't violate theory—it adds PRECISION. Clarifies mechanisms, specifies moderators, unpacks processes.

**Key indicators**:
- "How" questions rather than "whether" questions
- Existing theory is correct but underspecified
- Adds detail without contradicting core prediction
- Contribution framed as "unpacking," "specifying," or "extending"

**Evaluation framework**: Fisher & Aguinis criteria:
1. **Construct clarity**: Are new constructs well-defined?
2. **Mechanism specification**: Is the "how" clearly articulated?
3. **Boundary precision**: Are moderators/conditions specified?
4. **Empirical tractability**: Can the elaboration be tested?
5. **Integration**: Does it connect back to parent theory?

**Exemplar journals**: AMR, Organization Science, Strategic Management Journal

---

### Type 3: Phenomenon Description (Weick)

**What it is**: Paper describes something no one has described before. The phenomenon itself IS the contribution. Theory comes later or minimally.

**Key indicators**:
- "What is happening here?" question
- Rich description of previously unseen/unnoticed pattern
- Theory is sensitizing, not predictive
- Contribution framed as "revealing," "documenting," or "describing"

**Evaluation framework**: Weick's "What Theory Is Not" criteria:
1. **Phenomenon clarity**: Is it clear what's being described?
2. **Theoretical interest**: Why should we care? What expectations does it violate or complicate?
3. **Descriptive richness**: Is the description vivid enough to enable theorizing?
4. **Generalizability hints**: What features suggest broader relevance?
5. **Conceptual handles**: Are there concepts others can pick up?

**Exemplar journals**: ASQ (qualitative), Organization Studies, Ethnography

---

### Type 4: Methodological Contribution (Abbott)

**What it is**: Paper develops or demonstrates a new way of studying something. Method IS the contribution.

**Key indicators**:
- "How should we study X?" question
- Novel data, technique, or analytic approach
- Substantive findings may be secondary
- Contribution framed as "enabling," "demonstrating," or "validating"

**Evaluation framework**: Abbott's methodological heuristics:
1. **Problem fit**: Does the method address a real methodological limitation?
2. **Transparency**: Can others follow and replicate?
3. **Comparative advantage**: Why this over existing methods?
4. **Practical applicability**: Can others actually use it?
5. **Demonstration quality**: Is the empirical illustration compelling?

**Exemplar journals**: Sociological Methods & Research, Organizational Research Methods, Research Policy

---

### Type 5: Practical Insight (Corley & Gioia utility axis)

**What it is**: Paper provides actionable knowledge for practitioners. May have theoretical elements but primary value is applied.

**Key indicators**:
- "What should practitioners do?" question
- Clear prescriptive implications
- Accessible to non-academics
- Contribution framed as "guidance," "framework for action," or "implications for practice"

**Evaluation framework**: Corley & Gioia practical utility criteria:
1. **Problem significance**: Do practitioners actually face this problem?
2. **Actionability**: Can they DO something with this?
3. **Contextual fit**: Is advice appropriate to practitioner constraints?
4. **Evidence base**: Is practical guidance supported by evidence?
5. **Accessibility**: Can practitioners understand it?

**Exemplar journals**: HBR, SMR, California Management Review, Academy of Management Perspectives

---

### Type 6: Literature Integration/Synthesis

**What it is**: Paper organizes, synthesizes, or reconciles existing work. No new data—value is in conceptual organization.

**Key indicators**:
- "What do we know about X?" question
- Integrates across papers/traditions
- Identifies tensions, gaps, or reconciliations
- Contribution framed as "organizing," "synthesizing," or "reconciling"

**Evaluation framework**: Palmatier et al. review criteria:
1. **Scope**: Is coverage appropriate (not too narrow, not too broad)?
2. **Organizing logic**: Is the framework for synthesis clear?
3. **Insight generation**: Does synthesis produce new understanding?
4. **Gap identification**: Are gaps meaningfully characterized (not just listed)?
5. **Future directions**: Does it enable new research?

**Exemplar journals**: AMR, Journal of Management, Annual Review of X

---

## Diagnosis Process

### Step 1: Read the Abstract and Introduction

Look for:
- What QUESTION is the paper answering?
- How is the CONTRIBUTION framed?
- What would SUCCESS look like?

### Step 2: Classify Using Decision Tree

```
Is the paper primarily...

→ CHALLENGING existing theory?
  → Does it claim theory is WRONG (under conditions)?
    → Yes: TYPE 1 - Theory Violation
  → Does it claim theory is INCOMPLETE (needs precision)?
    → Yes: TYPE 2 - Theory Elaboration

→ DESCRIBING something new?
  → Is the phenomenon itself the main contribution?
    → Yes: TYPE 3 - Phenomenon Description
  → Is the method for studying it the main contribution?
    → Yes: TYPE 4 - Methodological

→ GUIDING practice?
  → Is actionable advice the primary goal?
    → Yes: TYPE 5 - Practical Insight

→ ORGANIZING existing knowledge?
  → Is synthesis/integration the primary goal?
    → Yes: TYPE 6 - Literature Integration
```

### Step 3: Check for Mismatches

Common problems:
- **Framed as Type 1 but evidence supports Type 2**: Paper claims to "violate" theory but actually just elaborates it
- **Framed as Type 3 but structured as Type 1**: Paper has rich description but forces a violation frame
- **Mixed types without acknowledgment**: Paper tries to be Types 1, 3, AND 5 simultaneously

### Step 4: Recommend Appropriate Framework

Based on diagnosis, route to the right evaluation:
- Type 1 → `/eval-zuckerman`
- Type 2 → Apply Fisher & Aguinis criteria (below)
- Type 3 → Apply Weick criteria (below)
- Type 4 → Apply Abbott criteria (below)
- Type 5 → Apply Corley & Gioia criteria (below)
- Type 6 → Apply Palmatier criteria (below)

## Output Format

Create `analysis/framing/CONTRIBUTION_DIAGNOSIS.md`:

```markdown
# Contribution Type Diagnosis

**Paper**: [Title]
**Date evaluated**: [Date]
**Target journal**: [If specified]

---

## Diagnosis Summary

**Diagnosed contribution type**: [Type 1-6 with name]

**Confidence**: [High / Medium / Low]

**Appropriate evaluation framework**: [Framework name]

---

## Diagnostic Evidence

### Question Being Answered

The paper is asking: "[Reconstruct the core question]"

This is a [challenge/describe/guide/organize] question, indicating Type [X].

### Contribution Framing

The paper claims to: "[Quote contribution statement]"

Key framing words: [violate/extend/specify/reveal/enable/guide/synthesize/etc.]

This framing indicates Type [X].

### Evidence Structure

The paper provides: [What kind of evidence?]

This evidence is best suited for Type [X].

---

## Mismatch Analysis

**Does framing match evidence?**: [Yes / No]

**If no, describe the mismatch**:
- Paper is FRAMED as: [Type X]
- Paper's EVIDENCE supports: [Type Y]
- Recommendation: [Reframe to match evidence / Gather different evidence]

---

## Framework-Specific Evaluation

### [Framework Name] Criteria

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| [Criterion 1] | ✓/⚠️/✗ | [Quote/explanation] |
| [Criterion 2] | ✓/⚠️/✗ | [Quote/explanation] |
| [Criterion 3] | ✓/⚠️/✗ | [Quote/explanation] |
| [Criterion 4] | ✓/⚠️/✗ | [Quote/explanation] |
| [Criterion 5] | ✓/⚠️/✗ | [Quote/explanation] |

**Overall**: [X/5 criteria met strongly]

---

## Detailed Criterion Analysis

### Criterion 1: [Name]

**Rating**: [✓/⚠️/✗]

**Evidence**:
> [Quote from paper]

**Analysis**: [Why this rating]

**Suggestion** (if needed): [Specific fix]

---

[Repeat for each criterion]

---

## Comparison: If Evaluated as Type 1 (Zuckerman)

Would this paper pass Zuckerman criteria?

| Zuckerman Criterion | Likely Rating | Why |
|---------------------|---------------|-----|
| Motivate the paper | [✓/⚠️/✗] | [Brief] |
| Compelling null | [✓/⚠️/✗] | [Brief] |
| Save the null | [✓/⚠️/✗] | [Brief] |
| Puzzle in world | [✓/⚠️/✗] | [Brief] |

**Verdict**: [Zuckerman framework is/is not appropriate for this paper because...]

---

## Recommendations

### If diagnosis is correct:

1. [Specific improvement for identified type]
2. [Another improvement]
3. [Target journals that value this type]

### If reframing needed:

**Current frame**: [Type X]
**Recommended frame**: [Type Y]
**What would need to change**:
1. [Specific change]
2. [Specific change]
3. [Specific change]

---

## Next Steps

Based on contribution type [X], recommended next commands:

1. [Command] - [Why]
2. [Command] - [Why]
```

---

## Detailed Evaluation Criteria by Type

### Type 2: Theory Elaboration (Fisher & Aguinis)

**1. Construct Clarity**
- Are new/refined constructs clearly defined?
- Are distinctions from similar constructs explicit?
- Could another researcher operationalize these constructs?

**2. Mechanism Specification**
- Is the "how" clearly articulated?
- Are causal pathways specified (not just correlations)?
- Are there identifiable steps/processes?

**3. Boundary Precision**
- Are conditions under which elaboration applies specified?
- Are moderators identified and justified?
- Is it clear when the elaboration does NOT apply?

**4. Empirical Tractability**
- Can the elaboration be tested?
- What would count as evidence for/against?
- Are there falsifiable implications?

**5. Integration**
- Does the elaboration connect back to parent theory?
- Is it clear what the elaboration adds vs. changes?
- Does it maintain coherence with broader theoretical framework?

---

### Type 3: Phenomenon Description (Weick)

**1. Phenomenon Clarity**
- Is it clear what's being described?
- Can a reader "see" the phenomenon?
- Are boundaries of the phenomenon specified?

**2. Theoretical Interest**
- Why should we care about this phenomenon?
- What expectations does it violate or complicate?
- What would be lost if we ignored it?

**3. Descriptive Richness**
- Is the description vivid enough to enable theorizing?
- Are multiple facets/perspectives included?
- Does the description go beyond surface features?

**4. Generalizability Hints**
- What features suggest broader relevance?
- Is this a "case of" something larger?
- What scope conditions are implied?

**5. Conceptual Handles**
- Are there concepts others can pick up and use?
- Has the author named key elements memorably?
- Can the description serve as a reference point for future work?

---

### Type 4: Methodological (Abbott)

**1. Problem Fit**
- Does the method address a real methodological limitation?
- Is the problem clearly stated?
- Would solving it enable important research?

**2. Transparency**
- Can others follow the procedure?
- Are steps explicit enough to replicate?
- Are decision points documented?

**3. Comparative Advantage**
- Why this method over existing alternatives?
- What can it do that others cannot?
- What are the trade-offs?

**4. Practical Applicability**
- Can others actually use this?
- What resources/skills are required?
- Are there tools/templates provided?

**5. Demonstration Quality**
- Is the empirical illustration compelling?
- Does it show the method working as claimed?
- Are limitations of the demonstration acknowledged?

---

### Type 5: Practical Insight (Corley & Gioia)

**1. Problem Significance**
- Do practitioners actually face this problem?
- How widespread is the problem?
- What are the consequences of not solving it?

**2. Actionability**
- Can practitioners DO something with this?
- Are recommendations specific enough?
- Are resources/steps identified?

**3. Contextual Fit**
- Is advice appropriate to practitioner constraints?
- Does it account for real-world complexity?
- Are implementation barriers addressed?

**4. Evidence Base**
- Is practical guidance supported by evidence?
- Is the evidence relevant to practitioner contexts?
- Are limitations of evidence acknowledged?

**5. Accessibility**
- Can practitioners understand it?
- Is jargon minimized or explained?
- Is the takeaway clear?

---

### Type 6: Literature Integration (Palmatier et al.)

**1. Scope**
- Is coverage appropriate?
- Are boundaries of the review justified?
- Is it neither too narrow nor too broad?

**2. Organizing Logic**
- Is the framework for synthesis clear?
- Why this organizing scheme vs. alternatives?
- Does the framework illuminate patterns?

**3. Insight Generation**
- Does synthesis produce NEW understanding?
- Are there emergent themes/tensions/reconciliations?
- What do we know now that we didn't before?

**4. Gap Identification**
- Are gaps meaningfully characterized?
- Are they "interesting" gaps (not just absences)?
- Is it clear why filling them matters?

**5. Future Directions**
- Does the review enable new research?
- Are directions specific and actionable?
- Do they follow from the synthesis?

---

## After You're Done

Tell the user:
1. The diagnosed contribution type
2. Whether their current framing matches their evidence
3. How the paper rates on the APPROPRIATE criteria (not just Zuckerman)
4. Specific suggestions for strengthening the contribution
5. Whether `/eval-zuckerman` is the right next step (or an alternative)

## Integration with Other Commands

- Run BEFORE `/eval-zuckerman` to determine if Zuckerman is appropriate
- Run AFTER `/smith-frames` when framing is established
- If Type 1, proceed to `/eval-zuckerman`
- If other types, use the evaluation produced by this command

## Common Mistakes

**Forcing violation frame onto elaboration evidence**: Paper claims to "challenge" theory but evidence actually adds precision without contradiction. Fix: Reframe as elaboration.

**Burying phenomenon under theory**: Paper has rich, novel phenomenon description but buries it under theoretical positioning. Fix: Lead with the phenomenon.

**Applying Zuckerman to everything**: Not all valuable papers violate theoretical predictions. Some elaborate, describe, or guide. Don't force a framework that doesn't fit.

**Mixing types without integration**: Paper tries to violate theory, describe a phenomenon, AND guide practice all at once. Fix: Choose a primary contribution type; others can be secondary.
