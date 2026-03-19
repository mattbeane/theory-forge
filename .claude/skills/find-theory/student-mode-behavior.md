## Student Mode Behavior

If `state.json.student_mode.enabled === true`, add these steps:

### Before Running Analysis

Prompt the user:

```
📚 STUDENT MODE: Before I identify the theory being violated, show me YOUR thinking.

Please write in STUDENT_WORK.md (or tell me now):

1. **What theory might this finding violate?** (Name 2-3 candidate theories)
2. **What does each theory predict?** (The standard prediction)
3. **How does your finding contradict each?** (Be specific)
4. **Which violation would be most interesting to your target audience?** (And why)

This is where scholarly intuition develops. You need to know literatures well enough to see violations. Take 15-20 minutes.

[When ready, say "continue" and I'll show you what I find]
```

Wait for user response before proceeding.

### After Running Analysis

Add a **"Why I Did This"** section to your output:

```markdown
