# Living Paper Implementation Prompt

Use this prompt with a frontier model (Claude Opus, o1, etc.) alongside the LIVING_PAPER_SPEC.md document.

---

## Prompt

I'm a professor of Technology Management at UC Santa Barbara. I study how people develop expertise—particularly in contexts where AI/robotics are changing work. My research is primarily qualitative: ethnographic fieldwork, interviews, observation. I publish in management journals (ASQ, Org Science, Management Science).

I've built a system called "paper-mining-agents" that uses Claude Code to accelerate qualitative research—turning dormant datasets into papers through AI-assisted pattern-finding, evidence extraction, and manuscript generation. The key insight: the human stays the theorist and interpreter; the AI accelerates search and enforces structure.

Now I want to build infrastructure for "living papers"—research artifacts that maintain bidirectional links between claims and evidence throughout their lifecycle. The attached spec (LIVING_PAPER_SPEC.md) lays out the concept.

### My Context

**Why I care about this:**
1. I have 15+ years of qualitative data under various IRB protocols—interviews, field notes, observations. Much of it contains PII or information that could enable attribution even with pseudonyms. I can't share it, but I want claims derived from it to be verifiable.

2. I'm training PhD students who will be faculty in 10 years. I want them to build habits around claim-evidence traceability now, before they accumulate datasets with broken provenance chains.

3. The replication crisis critique of qualitative research ("your findings are unfalsifiable") has merit. Living papers could provide verification infrastructure that doesn't currently exist—without requiring us to violate IRB commitments.

4. I already have the paper-mining-agents workflow producing structured output (claims, evidence links, frame iterations). Building living paper infrastructure on top of this is a natural extension.

**Constraints:**
- IRB protocols govern my existing data. Some prohibit sharing; some require destruction after N years. Any system must respect these constraints absolutely.
- I work primarily in Claude Code on my local machine. I'm comfortable with Python, markdown, SQLite, and command-line tools. I'm not going to spin up Kubernetes clusters.
- I need something I can actually use, not a beautiful architecture I'll never build. Minimum viable versions that provide value immediately are better than complete systems that take a year.
- My PhD students are potential early users/contributors. The system should be learnable by smart people who aren't software engineers.

**What I already have:**
- Paper-mining-agents repo with slash commands for the full data-to-paper pipeline
- Extraction schema that structures how claims and evidence are captured
- Style enforcer module that validates manuscript output
- Multiple datasets in various states (some analyzed, some dormant)
- Relationships with field sites I could return to for additional data collection

### What I Want From You

1. **Critique the spec**: What's overengineered? What's missing? What assumptions am I making that might be wrong?

2. **Propose a build sequence**: Given my constraints, what's the smartest order to build this? What provides value earliest? What should I defer or cut entirely?

3. **Design the data model**: Propose concrete schemas for claims, evidence links, and protected data references that would work with my existing paper-mining-agents workflow. Show me what the actual files/database would look like.

4. **Solve the hard problems**:
   - How do I handle evidence that's scheduled for IRB-mandated destruction?
   - How do I verify claims against protected data without exposing it?
   - How do I version a living paper when claims change?

5. **Sketch the implementation**: What would V0.1 actually look like as code? Give me enough to start building—file structures, key functions, integration points with existing slash commands.

Be direct. Tell me what's feasible and what's fantasy. I'd rather have a working V0.1 than a beautiful spec for V2.0.

---

## Attachments

Include with this prompt:
- LIVING_PAPER_SPEC.md (full spec document)
- README.md from paper-mining-agents (for context on existing system)
- templates/extraction-schema.md (if it exists, for data model context)
