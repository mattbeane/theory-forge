# /eval-limitations - Limitations Section Genre Check

Evaluate whether the Limitations section follows academic genre conventions. Catches over-disclosure that undermines paper credibility.

## Why This Matters

Authors—especially careful ones—often write limitations sections that "give away more than necessary." This manifests as:
- Enumerated confessions with bold headers (looks like a defense brief)
- Pre-emptive responses to reviewer critiques not yet received
- Detailed hedging language that signals uncertainty rather than scientific precision
- Word counts 2-3x longer than genre norms

The result: readers/reviewers sense weakness even when the research is sound.

## When to Run

- After `/draft-paper` or any major revision
- Before submission
- Whenever limitations section feels "heavy"

## Benchmarks from Exemplar Papers

| Paper | Journal | Limitations Words | Structure |
|-------|---------|-------------------|-----------|
| Beane 2023 | ASQ | ~400 | 2 paragraphs (scope conditions → broader applicability) |
| O'Mahoney & Bechky 2006 | AMJ | ~350 | 2 paragraphs, general |
| Bernstein 2012 | ASQ | ~250 | Embedded in discussion flow |
| Brayne 2017 | ASR | ~200 | Brief, integrated with future research |

**Target**: 200-400 words in 1-2 flowing paragraphs

## Red Flags to Check

### Structure Red Flags

1. **Enumerated format with bold headers**
   - BAD: `\textbf{Limitation 1}. ... \textbf{Limitation 2}. ...`
   - GOOD: Flowing prose that acknowledges multiple issues in one paragraph

2. **More than 3 limitations explicitly named**
   - Pick the 2-3 that matter most; others can be implicit

3. **"Several limitations warrant discussion"** opening
   - Generic throat-clearing; cut it

4. **Limitations section longer than Theoretical Contributions**
   - Inverted priority signals lack of confidence

### Language Red Flags

| Over-Disclosure (BAD) | Confident Acknowledgment (GOOD) |
|-----------------------|--------------------------------|
| "This is the central limitation" | "This study has limitations characteristic of..." |
| "introducing potential circularity" | [Just don't mention circularity unless asked] |
| "better interpreted as... rather than a direct test" | "We infer X from Y rather than measuring directly" |
| "we cannot draw firm conclusions" | [State what you CAN conclude] |
| "Future research should..." (multiple times) | One brief forward pointer |

### Content Red Flags

1. **Explaining why a limitation is a limitation**
   - If reviewers need explanation, it's probably not worth mentioning

2. **Proposing solutions to your own limitations**
   - Save for R&R response; implies you know it's broken

3. **Acknowledging limitations that don't threaten core claims**
   - Only mention what could actually undermine the contribution

4. **Defensive language patterns**
   - "We acknowledge that..." "It must be noted that..." "We recognize..."

## The Two-Paragraph Pattern

### Paragraph 1: Limitations (~100-150 words)

Structure: "This study has [characteristic] limitations. [Limitation 1 in one sentence]. [Limitation 2 in one sentence]. [Limitation 3 if truly necessary]. [Optional: brief future research pointer]."

Example:
> This study has limitations characteristic of mixed-methods field research. We infer work orientation from qualitative evidence and behavioral patterns rather than measuring it directly; future research should develop direct measures such as surveys assessing desired versus actual employment arrangements. Our qualitative data come primarily from managers rather than workers themselves. And we cannot fully separate orientation from ability: the first-month performance gap for future converters could reflect either career orientation or underlying capability. These interpretations are not mutually exclusive.

### Paragraph 2: Generalizability (~100-150 words)

Structure: "[Setting characteristics]. But [abstract mechanism] should apply wherever [transferable conditions]. [Analog domains]. [Magnitude caveat]."

Example:
> The data come from one retailer's warehouse operations—a setting where performance is individually measurable, incentive pay is transparent, and advancement pathways are visible. But the core mechanism we propose—that work orientation moderates response to misfit, with advancement-seekers intensifying effort when signaling opportunities exist—should apply wherever three conditions hold: workers differ in orientation toward advancement, performance is observable and attributable to individuals, and realistic pathways exist from lower-status to higher-status positions. These conditions characterize settings beyond warehousing: sales organizations with performance-based promotion, professional services with partner tracks, skilled trades with apprentice-to-journeyman progression, and platform work where ratings shape access to higher-value tasks. The specific magnitudes will vary by context, but the qualitative pattern should operate wherever these conditions are met.

## Evaluation Steps

1. **Word count**: Count words in Limitations section
   - Flag if >400 words

2. **Structure check**:
   - Count enumerated items / bold headers
   - Flag if >2 explicit limitation labels

3. **Language scan**: Search for red-flag phrases
   - "central limitation"
   - "cannot draw firm conclusions"
   - "introducing potential"
   - "better interpreted as"
   - Multiple "Future research should"

4. **Ratio check**: Compare to Theoretical Contributions length
   - Flag if Limitations > 0.5 × Contributions

5. **Generalizability check**: Does second paragraph exist?
   - Must include: setting characteristics, abstract mechanism, transferable conditions, analog domains

## Output Format

Create `analysis/quality/LIMITATIONS_EVAL.md`:

```markdown
# Limitations Section Evaluation

**Paper**: [Title]
**Date**: [Date]

---

## Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Word count | X | 200-400 | ✓/✗ |
| Enumerated items | X | ≤2 | ✓/✗ |
| Bold headers | X | 0 | ✓/✗ |
| Ratio to Contributions | X:1 | <0.5:1 | ✓/✗ |

---

## Red Flags Found

| Flag | Location | Severity |
|------|----------|----------|
| [Phrase/pattern] | Line X | High/Medium/Low |

---

## Structure Assessment

**Current structure**: [Enumerated / Flowing / Mixed]

**Generalizability paragraph**: [Present / Missing / Incomplete]
- Setting characteristics: ✓/✗
- Abstract mechanism: ✓/✗
- Transferable conditions: ✓/✗
- Analog domains: ✓/✗

---

## Verdict

**Overall**: [PASS / REVISE / MAJOR REVISION]

---

## Recommended Revisions

[If REVISE or MAJOR REVISION, provide consolidated two-paragraph rewrite]
```

## After You're Done

Tell the user:
- Whether the section meets genre conventions
- Specific over-disclosures to cut
- If needed: a consolidated rewrite following the two-paragraph pattern

## Integration with Other Commands

- Run alongside `/eval-genre` (both check for over-hedging patterns)
- Run after `/eval-zuckerman` (which doesn't focus on limitations)
- Run before final submission

## Common Patterns

**"Pre-R&R defense"**: Author anticipates every possible reviewer objection. Fix: Save for actual R&R; initial submission should be confident.

**"Enumerated confession"**: Bold headers make each limitation visually prominent. Fix: Consolidate into flowing prose.

**"Missing generalizability"**: Limitations only, no scope conditions or transfer logic. Fix: Add second paragraph with Becker-style abstraction.

**"Single-site apology"**: Excessive hedging about one organization. Fix: State setting characteristics matter-of-factly, then explain why mechanism transfers.
