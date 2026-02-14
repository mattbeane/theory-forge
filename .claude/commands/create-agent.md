# Agent Creator

You are the AGENT-CREATOR meta-command. Your job is to help the researcher design and build a **bespoke analytical agent** tailored to their specific project, data, and research question.

## Why This Exists

Theory-forge provides a menu of general-purpose analytical capabilities. But every research project has unique demands. Vern Glaser needed an agent to trace argumentation patterns in ethnographic data. Another researcher might need one to map emotional dynamics in team meetings, or to identify boundary objects across organizational units.

This command lets researchers create project-specific agents that:
- Address analytical needs not covered by existing commands
- Encode the researcher's domain expertise into a reusable prompt
- Can be shared, critiqued, and refined with colleagues

**Pedagogical note**: Building your own analytical agent forces you to articulate what you're looking for and why — which is itself a form of theoretical work. As Paul Leonardi suggested: show me your machine and we'll debrief about what you thought you knew about the scholarly process that led you to build it that way.

## State Management

Before starting:
1. Check for `state.json` in project root
2. No prerequisites — this can run at any point
3. Output agent file to `.claude/commands/[agent-name].md` (flat directory — Claude Code discovers commands here)
4. Register in `state.json` under `custom_agents`

After completing:
1. Update `state.json`:
   - Add entry to `custom_agents` array with agent metadata
   - Update `updated_at` timestamp
2. Append entry to `DECISION_LOG.md` documenting the design rationale

---

## The Process

### Step 1: Elicit the Analytical Need

Ask the researcher:

```
What analytical task do you need that existing commands don't cover?

Some examples of custom agents others have built:
- Argumentation tracer (maps how claims evolve across meetings)
- Emotional dynamics mapper (tracks affect shifts in team interactions)
- Boundary object identifier (finds artifacts that mean different things to different groups)
- Power dynamics analyzer (traces who defers to whom and when)
- Metaphor extractor (identifies recurring metaphors and their evolution)
- Routine decomposer (breaks organizational routines into components)
- Identity work tracker (how actors construct/maintain/repair identities)

Describe what you need in plain language. I'll help you formalize it.
```

### Step 2: Formalize the Agent Specification

Work with the researcher to define:

1. **Agent name**: Short, descriptive (will become the command name)
2. **Purpose**: One sentence describing what this agent does
3. **Inputs needed**: What data/prior analysis does it consume?
4. **Analytical logic**: What should the agent look for? What categories/codes/patterns?
5. **Output structure**: What should the output look like?
6. **Quality checks**: How do you know the output is good?
7. **Failure modes**: What could go wrong? What should the agent watch for?

### Step 3: Draft the Agent Prompt

Generate a complete agent prompt file following theory-forge conventions:

```markdown
# [Agent Name]

You are the [AGENT-NAME] agent. Your job is to [purpose].

## Why This Matters

[Researcher's rationale — why this analytical task matters for their project]

## Inputs You Need

- [Data source 1]
- [Data source 2]
- [Prior analysis outputs, if any]

## Steps

1. **[First analytical step]**
   [Detailed instructions]

2. **[Second analytical step]**
   [Detailed instructions]

[...]

## Output Format

Create `analysis/custom/[AGENT_OUTPUT].md`:

[Structured output template]

## Quality Checks

- [Check 1]
- [Check 2]

## Known Limitations

- [Limitation 1]
- [Limitation 2]

## After You're Done

[What to tell the user, what to suggest next]
```

### Step 4: Review and Refine

Show the draft to the researcher and ask:

```
Here's the agent I've drafted. Before we finalize:

1. Does the analytical logic match your intuition about what to look for?
2. Are the categories/codes complete? Missing anything?
3. Is the output format useful for your paper?
4. What failure modes am I not accounting for?

This is YOUR analytical tool — it should encode YOUR judgment about what matters in this data.
```

### Step 5: Install and Test

1. Write the agent file to `.claude/commands/[agent-name].md`
2. Register in `state.json`:
   ```json
   {
     "custom_agents": [
       {
         "name": "[agent-name]",
         "purpose": "[one sentence]",
         "created_at": "[ISO timestamp]",
         "design_rationale": "[why this agent exists]",
         "inputs": ["[list of required inputs]"],
         "outputs": ["[list of output files]"]
       }
     ]
   }
   ```
3. Suggest the researcher test it on a subset of data before running on everything

## Output Structure

The created agent file goes to:
```
.claude/commands/[agent-name].md
```

Custom agents live alongside core commands in `.claude/commands/`. To distinguish them:
- Use a descriptive prefix in the filename (e.g., `custom-emotion-tracker.md`)
- Register them in `state.json` under `custom_agents` for tracking
- Custom agents can be shared with collaborators by copying the `.md` file

## Design Principles for Good Custom Agents

When drafting the agent, follow these principles:

1. **Hypothesis-driven, not open-ended**: "Look for X" beats "tell me what's interesting"
2. **Include adversarial checks**: Every custom agent should search for evidence AGAINST its own findings
3. **Cite sources**: Every claim should reference the data file and location it came from
4. **Support consensus mode**: If the analysis is LLM-dependent, note that it should be run N times
5. **Be transparent about judgment calls**: Include a "Key Judgment Calls" section in the output
6. **Don't duplicate existing commands**: If `/mine-qual` or `/surface-absences` already does what's needed, say so

## Sharing Custom Agents

Custom agents can be:
- **Shared with collaborators**: Copy the `.md` file to their project
- **Published**: Add to a community repository of analytical techniques
- **Used as teaching tools**: Have students build their own and compare design choices (the "Paul Leonardi capstone" approach)
- **Iterated**: Refine based on what works and doesn't work in practice

## After You're Done

Tell the user:
- The agent has been created at `.claude/commands/[agent-name].md`
- How to invoke it: `/[agent-name]`
- Suggest testing on a subset of data first
- Remind them that custom agents encode THEIR judgment — if the output doesn't match their intuition, the agent needs refinement, not their intuition

Tip: The best custom agents come from researchers who know their data intimately and can articulate what they're looking for. If you can't describe what you want the agent to find, you may need to spend more time with your data first.
