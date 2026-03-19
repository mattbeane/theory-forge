## Student Mode Behavior

If `state.json.student_mode.enabled === true`, add these steps:

### Before Running Analysis

Prompt the user:

```
📚 STUDENT MODE: Before I hunt for patterns, document your predictions.

Please write in STUDENT_WORK.md (or tell me now):

1. **What patterns do you expect to find?** (List 3-5 specific hypotheses)
2. **Which pattern do you think will be strongest?** (And why)
3. **What would surprise you?** (What finding would challenge your priors)
4. **What patterns would be most theoretically interesting?** (And for what literature)

This forces you to form expectations before seeing AI output. Take 10-15 minutes.

[When ready, say "continue" and I'll run the pattern search]
```

Wait for user response before proceeding.

### After Running Analysis

Add a **"Why I Did This"** section to your output:

```markdown
