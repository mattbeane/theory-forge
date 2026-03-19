# Paper 2 Journey: From "Seasonal Staffing" to "Learning to Automate"

**Timeline**: November 25, 2025 → January 13, 2026 (49 days)
**Frame Shifts**: 10
**Final Title**: "Learning to Automate: How Multi-Site Firms Distribute Exploration and Exploitation Across Facilities"
**Target Journal**: Management Science

---

## 2025-11-25: Initial Exploration — Descriptive Patterns

**Framing**: Purely descriptive: seasonal staffing and facility productivity patterns
**Mechanism**: None—documenting patterns without theoretical mechanism

Early exploration of PPH (packages per hour) data revealed heterogeneous patterns across 20 facilities. No theoretical framing yet—just documenting what the data show.

*Data*: 8,698 daily observations, 20 facilities, 2019-2021.

---

## 2025-11-27: Frame #2 — "Turnover Contagion"

**Framing**: Turnover contagion in warehouse operations

Attempted to frame around turnover spreading across facilities through network effects. Abandoned: this was one finding, not the full story of what's happening in the data.

---

## 2025-11-29: Frame #3 — "The Seasonal Paradox"

**Framing**: Productivity patterns don't match staffing patterns

Abandoned: Staffing isn't the main story—automation is.

---

## 2025-12-01: Frame #4 — "Automation Architectures"

**Framing**: Documenting heterogeneity in automation outcomes
**Evidence**: Same tech → different outcomes across facilities

Documented that identical technologies produce systematically different outcomes: big productivity gains at some sites, capacity expansion with falling PPH at others, little or even negative change at still others. Still descriptive—no theoretical mechanism explaining why.

---

## 2025-12-03: Thompson Buffering Hypothesis KILLED

**Category Changed**: Mechanism, Claims

Tested Thompson (1967) buffering theory: do facilities differentiate by buffering against environmental volatility?

**REJECTED BY DATA**: Volume variance test showed expansion and efficiency nodes have identical coefficient of variation (~0.59). Facilities don't differentiate by buffering volatility.

*Needed different theoretical frame.*

---

## 2025-12-04: Qualitative Mining Reveals Intentional Differentiation

**Category Changed**: Mechanism, Evidence

Searched 69 interviews for evidence of intentional facility differentiation.

**Key quote found**: "Gallatin develops, Fresno perfects."

Managers explicitly talk about pilot sites vs execution sites, different scorecards and expectations, deliberate knowledge transfer practices. This is intentional role assignment, not emergent differentiation.

---

## 2025-12-05: Size Moderation Discovered

**Category Changed**: Evidence, Boundaries

Tested facility size as moderator of automation effects.

**Significant interaction** (p=0.001): Larger facilities show less favorable productivity responses. Adds "coordination costs of scale" as boundary condition.

---

## 2025-12-06: Frame #5 — "Learning to Automate: Spatial Ambidexterity" (MAJOR)

**Framing**: Spatial ambidexterity: firms solve exploration-exploitation dilemma across geography
**Mechanism**: Multi-site firms deliberately assign learning roles (pilot/optimization/scale/shrink) to different facilities. Pooling heterogeneous roles produces null aggregate effects.

**Core insight**: The "null effect of automation" that prior research finds is an artifact of pooling heterogeneous roles. When you separate by role:
- Optimization nodes: +50% PPH
- Scale nodes: Volume growth, PPH decline
- Shrink nodes: Decline on all metrics

**Theory positioning**: Spatial separation as fourth mode of ambidexterity (alongside structural, temporal, contextual).

*Evidence*: Only 1 optimization facility (ATL3), 2 scale, 4 shrink. N is small but qualitatively grounded.

---

## 2025-12-08: Zip Critique — External Model Review

**Category Changed**: Validation (Zip Critique)

Packaged paper + data + code into `learning_to_automate_FULL_PACKAGE_20251126.zip` and sent to powerful external AI model for rigorous adversarial review.

**Package contents**:
- manuscript.tex (full paper)
- PPH data files
- run_all_robustness_checks.py
- Project Listing.xlsx (automation dates)
- DATA_DESCRIPTOR.md
- REVIEW_PROMPT.md with specific verification requests

---

## 2025-12-09: Zuckerman Evaluation + Friendly Review

**Category Changed**: Claims, Validation

Ran Zuckerman criteria evaluation: 9/10 criteria met (after revisions).

**Key changes**:
1. Consolidated 5 propositions to 3 for memorability
2. Built up null hypothesis: "Uniform effects are not naive—they reflect sensible reasoning. Automation technologies are engineered to specification..."

**Friendly review identified central vulnerability**: Ex-post role classification. Roles defined by realized outcomes (PPH/volume/hours changes), then heterogeneity in those same outcomes shown by role. Risk of tautology.

**Recommendation**: "Make 'spatial ambidexterity' the memorable term."

---

## 2025-12-09: QUANTITATIVE HALLUCINATION DISCOVERED — Placebo Test Bug

**Category Changed**: Validation (Hallucination/Error Discovery), Robustness

External zip critique revealed a critical code bug: **the placebo test was broken and produced meaningless results.**

**What the code claimed to do**:
- Run 1,000 permutation iterations shuffling treatment dates
- Compare actual effect to null distribution
- Report p-value for significance

**What the code actually did**:
```python
mapping = dict(zip(dates.index, shuffled))
```
- Bug: Merge operation returned the same dates every iteration
- All 1,000 iterations produced **identical effects** (variance = 0)
- The "p-value" was meaningless—not a real permutation test

**The lesson**: External model review ran the actual code and detected the bug by examining output variance. Internal review had accepted the reported p-value without verifying computational correctness.

---

## 2025-12-09: Adversarial Review Identifies Critical Issues

**Category Changed**: Robustness, Validation

Comprehensive external review identified 5 major issues:

1. **Placebo test is BROKEN**: (See above) All 1,000 iterations produce identical effect (variance = 0).

2. **Only 1 optimization facility**: Most theoretically important role has N=1.

3. **Pre-trends tests are low-power**: Optimization has only 4 months pre-period data.

4. **Size moderation under-documented**: No replication code in package.

5. **Role classification is outcome-based**: Central vulnerability remains.

**Verdict**: "Publishable for OrgSci/ASQ with tightening; pessimistic for ManSci unless you upgrade identification or radically tone down causal language."

---

## 2025-12-10: Critique Verification

**Category Changed**: Validation

Independent verification of reviewer claims against actual code/data.

**Confirmed**:
- Placebo test bug is real
- Only 1 optimization facility is correct
- Pre-trends insufficient for optimization

**Partially confirmed**: Size interaction code exists separately but not integrated into main robustness script.

---

## 2025-12-13: Claims Audit and Living Paper Integration

**Category Changed**: Validation, Replication

Ran comprehensive audit: 3,949 evidence items linked to 9 claims across 189 interviews.

**Audit findings**:
- Core narrative well-supported
- 3 claims need revision (CLM-006, CLM-007, CLM-009 have weak/challenging evidence)
- Key finding: Site selection driven by proximity to vendor more than strategic role assignment

**Claim revised**: "Deliberately selected, pragmatically located"—acknowledges pragmatic factors alongside deliberate selection.

---

## 2026-01-06: Validation Package Created

**Category Changed**: Replication

Created learning-to-automate-validation.zip (1.4 MB) for external sharing. Includes robustness scripts, threshold analysis, pre-trend tests.

---

## 2026-01-09: Theory-Building Language Scrub

**Category Changed**: Register, Claims

Systematic replacement of hypothesis-testing language:

- "validated this framework by testing" → "checked whether...aligned"
- "validate that the empirical clusters" → "check whether...clusters"

---

## 2026-01-09: Post-Adversarial Review Refinements

**Category Changed**: Boundaries, Robustness

Addressed reviewer feedback:
- N=1 optimization facility now explicitly acknowledged
- Role terminology footnote distinguishes "pilot" from "optimization"
- Pre-trend narrative acknowledges low power
- Seasonality controls added to analysis
- Outlier sign flip made explicit
- Winsorizing added to event study

---

## 2026-01-13: Final Manuscript Prepared

**Length**: 80 KB main.tex

Ready for submission to Management Science.

---

## Summary: The Arc

| # | Frame | Fate |
|---|-------|------|
| 1 | "Seasonal staffing and facility productivity" | Purely descriptive—no theoretical mechanism |
| 2 | "Turnover contagion in warehouse operations" | One finding, not full story |
| 3 | "The Seasonal Paradox" | Staffing isn't the main story; automation is |
| 4 | "Automation Architectures" | Documents heterogeneity but still descriptive |
| 5 | Thompson (1967) buffering | **REJECTED BY DATA**: Volume variance identical across roles |
| 6 | Qualitative search for role differentiation | **EVIDENCE FOUND**: "Gallatin develops, Fresno perfects" |
| 7 | Facility size × automation interaction | **Statistically significant** (p=0.001) |
| 8 | "Learning to Automate" | **FINAL FRAME**: Spatial ambidexterity |
| 9 | Post-adversarial refinements | Minor: n=1 acknowledged, terminology footnote, seasonality controls |
| 10 | Theory-building language scrub | Register aligned with inductive genre |

**Key insight**: The paper's core contribution—that "null effects of automation" are artifacts of pooling heterogeneous learning roles—only emerged after (1) a theoretical hypothesis was killed by data (Thompson buffering), (2) qualitative evidence revealed intentional role differentiation, and (3) adversarial review forced honesty about N=1 and ex-post classification.

**Critical lesson about AI-assisted research**: The placebo test bug would have been published without external verification. AI had written the code and reported "significant" p-values—but only external model review running the actual code detected that variance = 0 across all iterations. This shows why zip critiques (sending full packages to external models) catch errors that internal review misses.

**Central vulnerability that remains**: Ex-post role classification. The paper handles this by (1) owning it explicitly, (2) showing 9-threshold robustness, (3) grounding in qualitative evidence of intentional differentiation.

**Automation built during this journey**:
- `/eval-zuckerman`: 10-criteria evaluation
- Living Paper claims audit
- Threshold robustness framework
