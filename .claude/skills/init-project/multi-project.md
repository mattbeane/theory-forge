## Multi-Project Mode

If the user is setting up multiple papers in one workspace, create:

```
workspace/
├── .claude/
│   └── skills/
├── projects/
│   ├── paper-1/
│   │   ├── data/
│   │   ├── analysis/
│   │   ├── literature/
│   │   ├── output/
│   │   ├── PROJECT_CONTEXT.md
│   │   ├── DECISION_LOG.md
│   │   └── state.json
│   └── paper-2/
│       └── [same structure]
├── shared/
│   └── literature/          # Shared reference library
└── workspace.json           # Tracks all projects
```

The `workspace.json` file:

```json
{
  "version": "1.0.0",
  "created_at": "[ISO timestamp]",
  "active_project": "paper-1",
  "projects": {
    "paper-1": {
      "path": "projects/paper-1",
      "created_at": "[ISO timestamp]",
      "status": "active"
    }
  }
}
```

Use `/switch-project` to change active project in multi-project mode.

---

For guided mode walkthrough, see [guided-mode.md](guided-mode.md)
