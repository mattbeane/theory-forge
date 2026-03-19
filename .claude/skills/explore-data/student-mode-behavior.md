## Student Mode Behavior

If `state.json.student_mode.enabled === true`, add these steps:

### Before Running Analysis

Prompt the user:

```
📚 STUDENT MODE: Before I explore your data, document your expectations.

Please write in STUDENT_WORK.md (or tell me now):

1. **What data sources do you have?** (List what you think is there)
2. **What do you expect to find?** (Patterns, anomalies, key variables)
3. **What would surprise you?** (What would challenge your assumptions)

This creates a record of your pre-AI thinking. Take 5-10 minutes on this.

[When ready, say "continue" and I'll run the exploration]
```

Wait for user response before proceeding.

### After Running Analysis

Add a **"Why I Did This"** section to your output:

```markdown
