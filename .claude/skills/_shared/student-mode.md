# Student Mode

When `state.json.student_mode.enabled === true`, skills add pedagogical scaffolding that helps researchers learn the analytical process.

## Before Running Analysis

Prompt the user to document their expectations BEFORE seeing AI output:

```
📚 STUDENT MODE: Before I [run analysis], document your predictions.

Please write in STUDENT_WORK.md (or tell me now):

1. **What do you expect to find?** (List specific hypotheses or expectations)
2. **What would surprise you?** (What would challenge your assumptions?)
3. **What are you most uncertain about?** (Where is your intuition weakest?)

This builds your analytical intuition. Take 10-15 minutes on this.

[When ready, say "continue" and I'll proceed]
```

Wait for user response before proceeding.

### Skill-Specific Expectations

Each skill customizes the prediction prompts:
- **hunt-patterns**: "What patterns do you expect? Which will be strongest?"
- **mine-qual**: "Read 3-5 interviews first. What mechanisms do you see?"
- **explore-data**: "What do you expect the data to look like?"
- **find-theory**: "Which theories might your finding violate?"

## After Running Analysis

### Explanation Layer

Add a section explaining the AI's reasoning:

```markdown
## Why I Did This (Explanation Layer)

**What I searched for**: [Explanation of approach]
**Key judgment calls**: [Where interpretation mattered]
**Alternatives I considered**: [Other approaches and why I chose this one]
```

### Comparison Section

Compare student predictions against AI findings:

```markdown
## Your Predictions vs. My Findings

| You Expected | I Found | Match? |
|-------------|---------|--------|
| [their prediction] | [actual finding] | ✓/✗ |

**Biggest surprise**: [What diverged most from expectations]
**Your best intuition**: [Where they were most accurate]

**Questions to consider**:
1. Why did [surprising finding] surprise you?
2. What does the mismatch on [item] tell you about your assumptions?
3. How would you update your mental model based on these results?
```

## Logging

Append a session record to `STUDENT_WORK.md`:
```markdown
## Session: [Date/Time] — [Skill Name]

### Predictions (before AI)
[Student's pre-analysis writing]

### AI Findings Summary
[Key results]

### Comparison
[Match table]

### Reflection
[Student's post-analysis notes, if provided]
```

## Toggling

Use `/student-mode` to enable/disable or configure student mode settings.
