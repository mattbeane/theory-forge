# Advisor Guide: Supervising Students Using Theory-Forge

**Theory-forge accelerates skilled researchers. It doesn't replace skill development.**

This guide helps advisors supervise students who want to use theory-forge while ensuring they develop the capabilities needed for independent scholarship.

---

## The Core Tension

Students face competing pressures:
- **Speed**: Publish to stay competitive
- **Skill**: Develop capabilities for long-term career
- **Temptation**: Let AI do the hard parts

Your job as advisor: ensure the student builds skills while benefiting from AI assistance.

---

## Recommended Approach

### Phase 1: Manual First (No Theory-Forge)

Before a student uses theory-forge, they should complete **at least one project** using traditional methods:

1. Code a dataset by hand (not just "assisted by AI")
2. Develop themes iteratively, experiencing the struggle
3. Write a methods section describing what they actually did
4. Receive peer feedback on their analytical choices

This builds the foundation needed to evaluate AI outputs.

### Phase 2: Guided Introduction

When the student starts using theory-forge:

1. **Work through it together** the first time
   - Sit with them as they run commands
   - Discuss what the AI produces
   - Ask: "Does this match what you see in the data?"

2. **Enable student mode** (`/student-mode on`)
   - Requires predictions before AI runs
   - Shows AI reasoning
   - Creates audit trail you can review

3. **Review their `STUDENT_WORK.md`**
   - What did they predict vs. what AI found?
   - Where did they agree/disagree with AI suggestions?
   - Did they go back to the data to check AI claims?

### Phase 3: Supervised Independence

As the student gains experience:

1. **Spot-check outputs** rather than reviewing everything
2. **Focus on decision points**:
   - Why did they choose this framing over alternatives?
   - How did they handle disconfirming evidence?
   - Can they explain the mechanism in their own words?

3. **Ask "show me in the data"**
   - If they can't point to specific passages, they're over-relying on AI

---

## Warning Signs

### Student May Be Over-Relying on AI

| Sign | What It Suggests |
|------|------------------|
| Can't explain framing choices | Accepted AI suggestion without evaluation |
| No disconfirming evidence discussed | Didn't engage with adversarial outputs |
| Methods section is vague | Didn't track what they actually did |
| Surprised by your questions | Didn't think deeply about the analysis |
| Identical language to AI outputs | Copy-pasted without digesting |

### Student Is Using AI Well

| Sign | What It Suggests |
|------|------------------|
| Can trace claims to specific data | Verified AI suggestions against raw data |
| Discusses alternatives they rejected | Engaged with multiple framings |
| Acknowledges limitations AI surfaced | Read adversarial evidence seriously |
| Methods section is detailed | Tracked their process |
| Uses own language to explain | Internalized the argument |

---

## Gate Checkpoints

Theory-forge has quality gates. These are natural checkpoints for advisor review:

### Gate A: After `/hunt-patterns`

**Ask**: Is this pattern interesting? Does it violate theory?

**Red flags**:
- Pattern is obvious (no theoretical tension)
- Student can't explain why it matters
- Student didn't look at "killed findings"

### Gate C: After `/smith-frames`

**Ask**: Why this framing over alternatives?

**Red flags**:
- Student chose first suggestion without comparing
- Can't explain adversarial concerns
- Framing doesn't match the data student described to you

### Gate D: After evaluations (`/eval-zuckerman`, `/eval-becker`, `/eval-genre`)

**Ask**: What did the evaluations flag?

**Red flags**:
- Student doesn't know what failed
- Student skipped evaluations to proceed faster
- Student can't explain how they addressed concerns

### Gate F: After `/verify-claims`

**Ask**: What claims are weakest?

**Red flags**:
- Student says "all claims verified"
- No discussion of alternative interpretations
- Student didn't send package to external reviewer

---

## Advisor Notifications (Optional)

If student mode is configured with your email:

```
/student-mode advisor your-email@university.edu
```

You'll receive notifications when the student passes major gates. The notification includes:
- What command was run
- Student's prediction (if any)
- Key AI outputs
- Student's decision

This lets you monitor progress without requiring synchronous meetings.

---

## Conversation Starters

### After `/explore-data`
- "What surprised you in the data inventory?"
- "Did the AI find anything you hadn't noticed?"

### After `/hunt-patterns`
- "Which patterns did you expect? Which surprised you?"
- "What patterns did the AI test that died? Why?"

### After `/find-theory`
- "Why does this finding violate [theory]?"
- "Could you have predicted this finding from [theory]?"

### After `/mine-qual`
- "Show me a quote that challenges your interpretation"
- "What did informants say that you didn't expect?"

### After `/smith-frames`
- "What's the alternative framing you rejected? Why?"
- "What's the weakest part of your chosen framing?"

### After `/verify-claims`
- "What did the external reviewer flag?"
- "Which claim would you drop if you had to?"

---

## When to Intervene

**Stop the student and discuss if:**
- They're running commands without reading outputs
- They can't explain decisions in their own words
- They haven't touched the raw data in weeks
- They're dismissing AI-surfaced concerns without explanation
- Their writing sounds like AI output rather than their voice

**Encourage them if:**
- They're spending too long double-checking everything
- They're afraid to trust any AI suggestion
- They're not using the tool at all out of fear

---

## A Note on Methods Sections

Students will need to describe their process. Theory-forge creates `DECISION_LOG.md` which helps, but the student should write the methods section themselves, in their own words.

**Good methods section**: Explains analytical choices, acknowledges AI assistance, describes how they verified AI outputs

**Bad methods section**: Vague about process, doesn't mention AI, or attributes all analysis to AI without explaining human judgment

The goal is transparency. Reviewers should understand what the human did vs. what the AI did.

---

## Resources

- [PREREQUISITES.md](PREREQUISITES.md) — What students need before using theory-forge
- [STUDENT_MODE_FEATURE_OPTIONS.md](STUDENT_MODE_FEATURE_OPTIONS.md) — Design rationale for student mode
- [ADVERSARIAL_EVIDENCE.md](ADVERSARIAL_EVIDENCE.md) — How theory-forge prevents cherry-picking
