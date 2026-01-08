# Knowledge Backlog Processor: Formal Specification

**Version:** 0.1.0
**Status:** Draft
**Author:** Matt Beane
**Date:** 2025-01-08

---

## Abstract

This document specifies a generalized architecture for converting dormant professional backlogs into validated outputs according to community standards. The pattern emerged from paper-mining-agents (academic research) but applies to any knowledge work domain where professionals must produce defensible outputs from accumulated artifacts.

The core insight: **the blocker isn't AI capability—it's defensibility**. Professionals won't use outputs they can't stake their reputation on. This architecture makes variance visible, constraints explicit, and quality gates mandatory, enabling professional communities to trust AI-assisted outputs.

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Core Concepts](#2-core-concepts)
3. [Architecture Overview](#3-architecture-overview)
4. [Layer Specifications](#4-layer-specifications)
   - 4.1 [Backlog Layer](#41-backlog-layer)
   - 4.2 [Triage Layer](#42-triage-layer) *(NEW)*
   - 4.3 [Community Standards Layer](#43-community-standards-layer)
   - 4.4 [Constraint Templates Layer](#44-constraint-templates-layer)
   - 4.5 [Execution Engine Layer](#45-execution-engine-layer)
   - 4.6 [Output Validation Layer](#46-output-validation-layer)
5. [Domain Configurations](#5-domain-configurations)
6. [Implementation Architecture](#6-implementation-architecture)
7. [Progression Model](#7-progression-model)
8. [Quality Assurance](#8-quality-assurance)
9. [Future Directions](#9-future-directions)

---

## 1. Problem Statement

### 1.1 The Dormant Potential Problem

Knowledge workers accumulate backlogs of potential value:
- Researchers sit on datasets that could become papers
- Consultants have client artifacts that could yield insights
- Clinicians have patient histories that could surface patterns
- Lawyers have case files that could inform strategy
- Educators have student work that could reveal learning gaps

These backlogs remain dormant not because processing them is impossible, but because:

1. **Time constraints**: Manual processing doesn't scale
2. **Expertise bottlenecks**: Domain experts are scarce
3. **Quality uncertainty**: AI-assisted outputs lack defensibility
4. **Community standards**: Each profession has specific validation requirements

### 1.2 The Defensibility Gap

Current AI tools produce outputs that professionals cannot trust because:

- **Variance is hidden**: Single-run outputs mask inconsistency
- **Constraints are implicit**: LLMs produce plausible but unvalidated content
- **Quality gates are missing**: No systematic verification before use
- **Community standards are ignored**: Generic outputs don't meet professional norms

### 1.3 The Backlog Graveyard Problem

**Most backlog items should stay dead.**

Knowledge workers accumulate backlogs not just because they lack time, but because:

1. **Sunk cost accumulation**: Items feel valuable because effort was invested
2. **Optionality preservation**: "Maybe someday" thinking keeps items alive
3. **Selection bias blindness**: The reasons an item was *never* prioritized are often valid
4. **Context decay**: The conditions that made an item promising may have changed

A naive processing system that treats every backlog item as worthy of full processing will:
- Waste compute on items that should have died
- Produce outputs for opportunities that no longer exist
- Give professional credibility to ideas that the community would reject
- Train users to distrust the system's judgment

**The system must be a filter, not just a processor.** Most items should be killed early and cheaply. Only a promising minority should receive full treatment.

### 1.4 The Solution Pattern

A system that:
1. **Triages backlogs iteratively**, killing most items early with minimal investment
2. Processes survivors through constrained, multi-run execution
3. Exposes variance through statistical aggregation
4. Validates outputs against community-specific standards
5. Provides confidence bounds that professionals can stake reputations on

---

## 2. Core Concepts

### 2.1 Definitions

**Backlog**: A collection of discrete work units (artifacts, data, opportunities) with natural temporal or logical boundaries, awaiting processing.

**Professional Community**: A group with shared standards for what constitutes valid evidence, defensible claims, and acceptable output formats.

**Constraint Template**: A structured prompt with explicit output requirements that reduce LLM variance to measurable levels.

**Defensibility**: The property of an output that allows a professional to stake their reputation on it, typically achieved through statistical confidence bounds, traceability, and community-standard compliance.

**Stability Score**: A measure of output consistency across multiple runs, typically expressed as Coefficient of Variation (CV).

### 2.2 Core Principles

1. **Kill Early, Kill Cheap**: Most backlog items should die in triage, not after expensive processing
2. **Variance Exposure Over Variance Hiding**: Always show users how confident they should be
3. **Community Accountability First**: Design for the people who will judge the output
4. **Explicit Quality Gates**: Make it impossible to skip validation steps
5. **Progressive Trust Building**: Start manual, graduate to automated as confidence grows
6. **Human-in-Loop by Design**: Not because AI can't, but because accountability requires it

---

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      KNOWLEDGE BACKLOG PROCESSOR                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐                                                        │
│  │  BACKLOG LAYER  │  What are we processing?                               │
│  │  (pluggable)    │  - Discrete work units with boundaries                 │
│  └────────┬────────┘  - Domain-specific artifact types                      │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐                                                        │
│  │  TRIAGE LAYER   │  Should this item live or die?        ──────┐         │
│  │  (iterative     │  - Multi-stage funnel                       │         │
│  │   funnel)       │  - Increasing investment per stage    ┌─────▼─────┐   │
│  └────────┬────────┘  - Kill criteria at each gate         │ GRAVEYARD │   │
│           │                                                │  (killed  │   │
│           │ survivors only (~10-20%)                       │   items)  │   │
│           ▼                                                └───────────┘   │
│  ┌─────────────────┐                                                        │
│  │   COMMUNITY     │  Who judges the output?                                │
│  │   STANDARDS     │  - Evidence requirements                               │
│  │   (pluggable)   │  - Format constraints                                  │
│  └────────┬────────┘  - Defensibility thresholds                            │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐                                                        │
│  │   CONSTRAINT    │  How do we reduce variance?                            │
│  │   TEMPLATES     │  - Output format specifications                        │
│  │   (pluggable)   │  - Forbidden patterns                                  │
│  └────────┬────────┘  - Verification checklists                             │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐                                                        │
│  │   EXECUTION     │  How do we process?                                    │
│  │   ENGINE        │  - Single/multi-run modes                              │
│  │   (core)        │  - Statistical aggregation                             │
│  └────────┬────────┘  - Failure handling                                    │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────┐                                                        │
│  │   OUTPUT        │  How do we ensure defensibility?                       │
│  │   VALIDATION    │  - Format compliance                                   │
│  │   (pluggable)   │  - Consistency checks                                  │
│  └─────────────────┘  - Review workflows                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Layer Specifications

### 4.1 Backlog Layer

The Backlog Layer defines what the system processes.

#### 4.1.1 Interface Definition

```typescript
interface BacklogSource {
  /** Unique identifier for this backlog source */
  id: string;

  /** Human-readable name */
  name: string;

  /** Type of backlog content */
  type: BacklogType;

  /** The discrete work units to process */
  items: BacklogItem[];

  /** How to determine unit boundaries */
  boundaries: BoundaryDefinition;

  /** Connection to source system */
  adapter: BacklogAdapter;
}

type BacklogType =
  | "artifacts"      // Documents, files, records
  | "data"           // Structured datasets
  | "opportunities"  // Potential actions to take
  | "obligations";   // Required deliverables

interface BacklogItem {
  /** Unique identifier within this backlog */
  id: string;

  /** When this item entered the backlog */
  ingestedAt: DateTime;

  /** Temporal boundaries of the work unit */
  temporalBounds: {
    start: DateTime;
    end: DateTime;
  };

  /** The actual content/artifacts */
  content: BacklogContent;

  /** Processing status */
  status: "pending" | "processing" | "completed" | "failed" | "flagged";

  /** Metadata for filtering/routing */
  metadata: Record<string, unknown>;
}

interface BoundaryDefinition {
  /** How to identify where one unit ends and another begins */
  type: "temporal" | "logical" | "explicit";

  /** For temporal: duration-based boundaries */
  temporalConfig?: {
    unit: "hour" | "day" | "week" | "project" | "custom";
    customDuration?: Duration;
  };

  /** For logical: content-based boundaries */
  logicalConfig?: {
    boundaryMarkers: string[];  // e.g., "CASE CLOSED", project IDs
    groupingField: string;      // field to group by
  };
}
```

#### 4.1.2 Domain Examples

| Domain | BacklogType | Item Example | Boundary Type |
|--------|-------------|--------------|---------------|
| Academic Research | data | One dataset + field notes | explicit (study) |
| Management Consulting | artifacts | One client engagement's emails/docs | logical (project ID) |
| Clinical Medicine | artifacts | One patient encounter | temporal (visit) |
| Legal Research | artifacts | One case file | explicit (case number) |
| Student Grading | obligations | One assignment submission | explicit (submission ID) |
| Grant Writing | opportunities | One preliminary dataset | explicit (aim) |

#### 4.1.3 Adapter Interface

```typescript
interface BacklogAdapter {
  /** Connect to source system */
  connect(): Promise<void>;

  /** Fetch pending items */
  fetchPending(limit?: number): Promise<BacklogItem[]>;

  /** Update item status */
  updateStatus(itemId: string, status: BacklogItem["status"]): Promise<void>;

  /** Store processing results */
  storeResult(itemId: string, result: ProcessingResult): Promise<void>;
}
```

Built-in adapters:
- `FileSystemAdapter`: Local directories with file-based items
- `NotionAdapter`: Notion databases as backlog sources
- `SlackAdapter`: Slack channels/threads as artifacts
- `GoogleDriveAdapter`: Drive folders as document sources
- `APIAdapter`: Generic REST/GraphQL endpoint

---

### 4.2 Triage Layer

The Triage Layer implements an iterative funnel that kills most backlog items early, investing progressively more resources only in items that survive each stage.

#### 4.2.1 Design Philosophy

**The Funnel Principle**: Processing cost should be proportional to survival probability. Items that will obviously fail should be killed with a single cheap check. Items that might succeed deserve progressively deeper analysis.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        TRIAGE FUNNEL                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  STAGE 0: STALENESS CHECK                        Cost: ~0               │
│  ───────────────────────                                                │
│  • Is the opportunity window still open?                                │
│  • Has context decayed beyond recovery?                                 │
│  • Kill rate: ~30-50%                                                   │
│                                                                         │
│           │ survivors                                                   │
│           ▼                                                             │
│                                                                         │
│  STAGE 1: QUICK VIABILITY SCAN                   Cost: 1 cheap LLM call │
│  ──────────────────────────                                             │
│  • Can this plausibly produce a valid output?                           │
│  • Does it have minimum required components?                            │
│  • Kill rate: ~40-60%                                                   │
│                                                                         │
│           │ survivors                                                   │
│           ▼                                                             │
│                                                                         │
│  STAGE 2: COMMUNITY FIT CHECK                    Cost: 1-2 LLM calls    │
│  ────────────────────────────                                           │
│  • Would the target community care about this?                          │
│  • Does it address a recognized gap/need?                               │
│  • Is the contribution potentially significant?                         │
│  • Kill rate: ~30-50%                                                   │
│                                                                         │
│           │ survivors                                                   │
│           ▼                                                             │
│                                                                         │
│  STAGE 3: FEASIBILITY PROBE                      Cost: 3-5 LLM calls    │
│  ──────────────────────────                                             │
│  • Can we actually produce what's needed?                               │
│  • Are there fatal gaps in the source material?                         │
│  • Does initial analysis show promise?                                  │
│  • Kill rate: ~20-40%                                                   │
│                                                                         │
│           │ survivors (~10-20% of original)                             │
│           ▼                                                             │
│                                                                         │
│  ══════════════════════════════════════════════                         │
│  PROCEED TO FULL PROCESSING                                             │
│  ══════════════════════════════════════════════                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 4.2.2 Interface Definition

```typescript
interface TriagePipeline {
  /** The stages in order */
  stages: TriageStage[];

  /** Overall survival target (for calibration) */
  targetSurvivalRate: number;  // e.g., 0.15 = 15% survive to full processing

  /** What to do with killed items */
  graveyardPolicy: GraveyardPolicy;
}

interface TriageStage {
  /** Stage identifier */
  id: string;

  /** Human-readable name */
  name: string;

  /** Order in the pipeline (0 = first) */
  order: number;

  /** What this stage evaluates */
  evaluates: string;

  /** Cost profile */
  cost: {
    llmCalls: number;      // expected LLM calls
    tokens: number;        // expected tokens
    humanMinutes: number;  // expected human review time
  };

  /** The checks to run */
  checks: TriageCheck[];

  /** Decision logic */
  decision: TriageDecision;

  /** Expected kill rate at this stage */
  expectedKillRate: {
    min: number;
    max: number;
  };
}

interface TriageCheck {
  /** Check identifier */
  id: string;

  /** What this check evaluates */
  description: string;

  /** Check type */
  type: "rule_based" | "llm_judgment" | "metadata_lookup" | "human_required";

  /** For rule-based checks */
  rule?: {
    field: string;
    operator: "gt" | "lt" | "eq" | "contains" | "exists" | "age_gt" | "age_lt";
    value: unknown;
  };

  /** For LLM judgment checks */
  llmConfig?: {
    prompt: string;
    expectedOutput: "binary" | "score" | "category";
    threshold?: number;  // for scores
    passingCategories?: string[];  // for categories
  };

  /** Weight in decision (if multiple checks) */
  weight: number;
}

interface TriageDecision {
  /** How to combine check results */
  logic: "all_pass" | "any_pass" | "weighted_score" | "custom";

  /** For weighted_score: minimum to survive */
  threshold?: number;

  /** For custom: decision function name */
  customFunction?: string;

  /** Override: always send to human if uncertain */
  humanReviewOnUncertain: boolean;

  /** Uncertainty threshold (for scores) */
  uncertaintyRange?: {
    low: number;   // below this = kill
    high: number;  // above this = survive
    // between = uncertain, may go to human
  };
}

interface GraveyardPolicy {
  /** What to store for killed items */
  retention: {
    storeKillReason: boolean;
    storeTriageScores: boolean;
    storePartialAnalysis: boolean;
  };

  /** Can killed items be resurrected? */
  resurrection: {
    allowed: boolean;
    cooldownDays: number;       // minimum time before retry
    maxResurrections: number;   // prevent infinite loops
    requiresChange: boolean;    // must something change to retry?
  };

  /** Reporting */
  reporting: {
    aggregateKillReasons: boolean;  // for pattern analysis
    notifyOnMassKill: boolean;      // alert if kill rate spikes
    massKillThreshold: number;      // what counts as "mass kill"
  };
}
```

#### 4.2.3 Stage Specifications

**Stage 0: Staleness Check (Rule-Based)**

Zero LLM cost. Pure metadata inspection.

```yaml
id: staleness-check
name: Staleness Check
order: 0
evaluates: "Is this item still timely and relevant?"

cost:
  llmCalls: 0
  tokens: 0
  humanMinutes: 0

checks:
  - id: age_check
    description: Item is not too old
    type: rule_based
    rule:
      field: ingestedAt
      operator: age_lt
      value: 180  # days
    weight: 1.0

  - id: context_exists
    description: Referenced context still exists
    type: metadata_lookup
    rule:
      field: contextReferences
      operator: exists
      value: true
    weight: 0.8

  - id: not_superseded
    description: No newer item covers same ground
    type: rule_based
    rule:
      field: supersededBy
      operator: eq
      value: null
    weight: 1.0

decision:
  logic: all_pass
  humanReviewOnUncertain: false

expectedKillRate:
  min: 0.30
  max: 0.50
```

**Stage 1: Quick Viability Scan (Single LLM Call)**

One cheap LLM call to assess basic viability.

```yaml
id: viability-scan
name: Quick Viability Scan
order: 1
evaluates: "Does this item have the minimum components for success?"

cost:
  llmCalls: 1
  tokens: 500
  humanMinutes: 0

checks:
  - id: completeness_check
    description: Has minimum required elements
    type: llm_judgment
    llmConfig:
      prompt: |
        Assess whether this backlog item has the minimum components needed
        to potentially produce a valid {{output_type}}.

        ITEM:
        {{item_summary}}

        Required components for {{domain}}:
        {{required_components}}

        Score from 0-100:
        - 0-30: Missing critical components, cannot proceed
        - 31-60: Missing some components, may be recoverable
        - 61-100: Has necessary components

        Output only the score as an integer.
      expectedOutput: score
      threshold: 40
    weight: 1.0

decision:
  logic: weighted_score
  threshold: 40
  humanReviewOnUncertain: false
  uncertaintyRange:
    low: 30
    high: 50

expectedKillRate:
  min: 0.40
  max: 0.60
```

**Stage 2: Community Fit Check (1-2 LLM Calls)**

Does the professional community actually want this?

```yaml
id: community-fit
name: Community Fit Check
order: 2
evaluates: "Would the target community value this contribution?"

cost:
  llmCalls: 2
  tokens: 1500
  humanMinutes: 0

checks:
  - id: relevance_check
    description: Addresses recognized community need
    type: llm_judgment
    llmConfig:
      prompt: |
        You are an expert in {{community_name}}.

        Evaluate whether this potential contribution addresses a recognized
        need, gap, or interest in the community.

        CONTRIBUTION SUMMARY:
        {{item_summary}}

        CURRENT COMMUNITY PRIORITIES:
        {{community_priorities}}

        Score from 0-100:
        - 0-30: No apparent community interest
        - 31-60: Tangential interest, niche audience
        - 61-100: Clear community relevance

        Output: Score (integer) | Brief reason (one sentence)
      expectedOutput: score
      threshold: 45
    weight: 0.6

  - id: novelty_check
    description: Offers something not already available
    type: llm_judgment
    llmConfig:
      prompt: |
        Assess whether this contribution would offer something new to
        {{community_name}}, or if similar work already exists.

        CONTRIBUTION SUMMARY:
        {{item_summary}}

        Score from 0-100:
        - 0-30: Already well-covered, nothing new
        - 31-60: Incremental addition to existing work
        - 61-100: Novel contribution or fresh angle

        Output: Score (integer) | Brief reason (one sentence)
      expectedOutput: score
      threshold: 35
    weight: 0.4

decision:
  logic: weighted_score
  threshold: 42
  humanReviewOnUncertain: true
  uncertaintyRange:
    low: 35
    high: 55

expectedKillRate:
  min: 0.30
  max: 0.50
```

**Stage 3: Feasibility Probe (3-5 LLM Calls)**

Can we actually do this? Light exploration of the source material.

```yaml
id: feasibility-probe
name: Feasibility Probe
order: 3
evaluates: "Can we actually produce a valid output from this material?"

cost:
  llmCalls: 5
  tokens: 5000
  humanMinutes: 2  # quick human sanity check on results

checks:
  - id: data_quality
    description: Source material is sufficient quality
    type: llm_judgment
    llmConfig:
      prompt: |
        Examine the source material for this backlog item.
        Assess whether it's sufficient to produce a {{output_type}}.

        SOURCE MATERIAL SAMPLE:
        {{material_sample}}

        Evaluate:
        1. Data completeness (are there obvious gaps?)
        2. Data quality (noise, inconsistency, ambiguity)
        3. Analyzability (can meaningful analysis be performed?)

        Score from 0-100 with brief justification.
      expectedOutput: score
      threshold: 50
    weight: 0.4

  - id: initial_analysis
    description: Initial analysis shows promise
    type: llm_judgment
    llmConfig:
      prompt: |
        Perform a quick preliminary analysis of this material.
        Identify 2-3 potential findings or themes.

        MATERIAL:
        {{material_sample}}

        TARGET OUTPUT TYPE: {{output_type}}

        Assessment:
        - Did you find anything worth developing? (yes/partial/no)
        - Confidence that full analysis would yield value (0-100)
        - Key finding preview (one sentence)
      expectedOutput: score
      threshold: 45
    weight: 0.4

  - id: fatal_flaw_check
    description: No obvious fatal flaws
    type: llm_judgment
    llmConfig:
      prompt: |
        Look for fatal flaws that would make this backlog item unworkable.

        ITEM SUMMARY:
        {{item_summary}}

        MATERIAL SAMPLE:
        {{material_sample}}

        Fatal flaws to check:
        - Ethical issues (privacy, consent, harm)
        - Legal issues (copyright, confidentiality)
        - Technical impossibility
        - Fundamental data problems

        Output: CLEAR (no fatal flaws) | FATAL: [reason] | UNCERTAIN: [concern]
      expectedOutput: category
      passingCategories: ["CLEAR"]
    weight: 0.2

decision:
  logic: weighted_score
  threshold: 48
  humanReviewOnUncertain: true
  uncertaintyRange:
    low: 40
    high: 60

expectedKillRate:
  min: 0.20
  max: 0.40
```

#### 4.2.4 Triage Output

```typescript
interface TriageResult {
  /** The item that was triaged */
  itemId: string;

  /** Final verdict */
  verdict: "proceed" | "kill" | "human_review";

  /** Which stage made the final decision */
  decidingStage: string;

  /** Results from each stage */
  stageResults: StageResult[];

  /** Total cost incurred */
  totalCost: {
    llmCalls: number;
    tokens: number;
    humanMinutes: number;
    estimatedDollars: number;
  };

  /** For killed items */
  killReason?: {
    stage: string;
    check: string;
    explanation: string;
    score?: number;
    threshold?: number;
  };

  /** For proceed items */
  proceedConfidence?: {
    score: number;           // 0-100
    strengthAreas: string[]; // what looks promising
    riskAreas: string[];     // what to watch for
  };

  /** For human_review items */
  humanReviewContext?: {
    uncertaintyReason: string;
    suggestedQuestions: string[];
    relevantScores: Record<string, number>;
  };
}

interface StageResult {
  stageId: string;
  passed: boolean;
  scores: Record<string, number>;  // check_id -> score
  aggregateScore?: number;
  notes: string[];
  cost: { llmCalls: number; tokens: number };
}
```

#### 4.2.5 Graveyard Management

Killed items aren't deleted—they're stored with context for:
1. **Pattern analysis**: Why do items die? What backlog sources produce mostly dead items?
2. **Resurrection eligibility**: If conditions change, can items be reconsidered?
3. **User learning**: Show users why their items died to calibrate expectations

```typescript
interface GraveyardEntry {
  /** Original item */
  item: BacklogItem;

  /** When killed */
  killedAt: DateTime;

  /** Full triage result */
  triageResult: TriageResult;

  /** Resurrection tracking */
  resurrection: {
    attempts: number;
    lastAttempt?: DateTime;
    eligible: boolean;
    eligibleAfter?: DateTime;
    requiredChanges?: string[];  // what would need to change
  };

  /** For analytics */
  analytics: {
    backlogSource: string;
    itemAge: number;  // days from ingestion to kill
    costToKill: number;  // dollars spent on triage
  };
}
```

#### 4.2.6 Domain-Specific Triage Examples

| Domain | Stage 0 Kill | Stage 1 Kill | Stage 2 Kill | Stage 3 Kill |
|--------|--------------|--------------|--------------|--------------|
| **Academic Research** | Dataset > 2 years old | No clear DV/IV structure | Topic already saturated | Data too noisy for claims |
| **Consulting** | Client no longer active | Missing business context | Problem already solved | Insufficient evidence for recs |
| **Legal** | Case closed/settled | Missing key documents | No novel legal question | Precedent analysis inconclusive |
| **Grading** | Assignment past due | Submission empty/corrupt | Wrong assignment type | Cannot apply rubric reliably |
| **Grant Writing** | Deadline passed | No preliminary data | Topic out of scope for funder | Pilot results too weak |

#### 4.2.7 Calibration and Tuning

The triage funnel should be calibrated based on:

1. **Downstream success rate**: What percentage of items that survive triage actually produce valid outputs?
   - If too low (<60%): Triage is too permissive, tighten thresholds
   - If too high (>90%): Triage may be killing viable items, loosen thresholds

2. **False positive rate**: What percentage of killed items would have succeeded?
   - Requires occasional "ghost runs" where killed items are processed anyway
   - Target: <15% of kills would have succeeded

3. **Cost efficiency**: Is triage actually saving money?
   - Track: (cost of full processing × items killed) vs. (cost of triage × all items)
   - Triage should save at least 3x its cost

```typescript
interface TriageCalibrationMetrics {
  /** Of items that survive triage, how many produce valid outputs? */
  survivorSuccessRate: number;

  /** Estimated false kill rate (from ghost runs) */
  falseKillRate: number;

  /** Cost savings from triage */
  costEfficiency: {
    triageCost: number;
    savedProcessingCost: number;
    netSavings: number;
    savingsMultiple: number;  // savedProcessingCost / triageCost
  };

  /** Kill rate by stage */
  killRateByStage: Record<string, number>;

  /** Kill rate by backlog source */
  killRateBySource: Record<string, number>;

  /** Items in human review queue */
  humanReviewBacklog: number;
}
```

---

### 4.3 Community Standards Layer

The Community Standards Layer defines who judges the output and what they require.

#### 4.3.1 Interface Definition

```typescript
interface ProfessionalCommunity {
  /** Unique identifier */
  id: string;

  /** Human-readable name */
  name: string;

  /** Description of the community and its norms */
  description: string;

  /** What counts as valid evidence? */
  evidenceStandards: EvidenceStandards;

  /** What counts as defensible? */
  defensibilityThreshold: DefensibilityThreshold;

  /** What are the quality gates? */
  qualityGates: QualityGate[];

  /** Output format requirements */
  outputFormats: OutputFormat[];
}

interface EvidenceStandards {
  /** Elements that MUST be present */
  requiredElements: RequiredElement[];

  /** Elements that MUST NOT be present */
  forbiddenElements: ForbiddenElement[];

  /** Traceability requirements */
  traceability: {
    claimToEvidence: boolean;      // Must link claims to source data
    methodTransparency: boolean;   // Must explain how conclusions reached
    uncertaintyDisclosure: boolean; // Must flag uncertain conclusions
  };
}

interface RequiredElement {
  name: string;
  description: string;
  validationRule: ValidationRule;

  // Examples:
  // { name: "citations", validationRule: { type: "regex", pattern: "\\([A-Z][a-z]+,? \\d{4}\\)" } }
  // { name: "IRB_approval", validationRule: { type: "presence", field: "irb_number" } }
  // { name: "sample_size", validationRule: { type: "numeric_present", field: "n" } }
}

interface ForbiddenElement {
  name: string;
  description: string;
  detectionRule: ValidationRule;
  severity: "error" | "warning";

  // Examples:
  // { name: "advocacy_language", detectionRule: { type: "regex", pattern: "\\b(should|must|need to)\\b" } }
  // { name: "unattributed_claims", detectionRule: { type: "custom", validator: "checkCitationCoverage" } }
}

interface DefensibilityThreshold {
  /** Statistical rigor required */
  statisticalRigor: "point_estimate" | "confidence_interval" | "full_distribution" | "bayesian";

  /** How to handle variance across runs */
  variancePolicy: {
    action: "hide" | "flag" | "reject_if_high";
    threshold?: number;  // CV threshold for "high"
  };

  /** Stability requirements */
  stabilityRequirements: {
    minStability: "low" | "medium" | "high";
    cvThresholds: {
      high: number;    // CV below this = HIGH stability (default: 0.10)
      medium: number;  // CV below this = MEDIUM stability (default: 0.25)
      // CV above medium threshold = LOW stability
    };
  };

  /** Human review requirements */
  reviewRequirements: {
    selfReview: boolean;        // Creator must review before submission
    peerReview: boolean;        // Domain expert must review
    stakeholderReview: boolean; // End consumer must approve
  };
}

interface QualityGate {
  /** Gate identifier */
  id: string;

  /** Human-readable name */
  name: string;

  /** When this gate is evaluated */
  stage: "pre_processing" | "post_processing" | "pre_output" | "pre_submission";

  /** What must pass */
  checks: QualityCheck[];

  /** What happens on failure */
  onFailure: "block" | "warn" | "flag_for_review";
}
```

#### 4.3.2 Configuration Examples

**Academic Sociology:**
```yaml
id: academic-sociology
name: Academic Sociology (Qualitative Management Journals)

evidenceStandards:
  requiredElements:
    - name: theoretical_grounding
      description: Claims must connect to established theory
      validationRule:
        type: citation_density
        minCitationsPerClaim: 1
    - name: methods_transparency
      description: Must explain data collection and analysis
      validationRule:
        type: section_present
        sections: [data_collection, analysis_approach]

  forbiddenElements:
    - name: advocacy_language
      description: Academic writing should not advocate
      detectionRule:
        type: regex
        pattern: "\\b(companies should|managers must|organizations need to)\\b"
      severity: warning
    - name: overclaiming
      description: Avoid claims beyond what data supports
      detectionRule:
        type: hedge_absence
        requiredHedges: [suggests, indicates, appears, may]
      severity: error

  traceability:
    claimToEvidence: true
    methodTransparency: true
    uncertaintyDisclosure: true

defensibilityThreshold:
  statisticalRigor: confidence_interval
  variancePolicy:
    action: flag
    threshold: 0.25
  stabilityRequirements:
    minStability: medium
    cvThresholds:
      high: 0.10
      medium: 0.25
  reviewRequirements:
    selfReview: true
    peerReview: true
    stakeholderReview: false  # No client approval needed

qualityGates:
  - id: pre_submission_review
    name: Pre-Submission Quality Check
    stage: pre_submission
    checks:
      - type: no_contested_claims
        description: All claims must have resolved evidence status
      - type: citation_completeness
        description: All claims must have citations
      - type: format_compliance
        description: Must match target journal format
    onFailure: block
```

**Management Consulting:**
```yaml
id: management-consulting
name: Management Consulting (Partner + Client Defensibility)

evidenceStandards:
  requiredElements:
    - name: executive_summary
      validationRule:
        type: section_present
        maxLength: 500
    - name: quantified_impact
      validationRule:
        type: numeric_present
        fields: [revenue_impact, cost_savings, time_reduction]

  forbiddenElements:
    - name: uncertain_recommendations
      detectionRule:
        type: regex
        pattern: "\\b(might|perhaps|possibly)\\b"
      severity: warning

  traceability:
    claimToEvidence: true
    methodTransparency: false  # Clients don't need to see the sausage
    uncertaintyDisclosure: false  # Confidence, not caveats

defensibilityThreshold:
  statisticalRigor: point_estimate  # Clients want clear numbers
  variancePolicy:
    action: hide  # Don't show uncertainty to clients
    threshold: null
  stabilityRequirements:
    minStability: high  # But internally, we need high confidence
    cvThresholds:
      high: 0.10
      medium: 0.20
  reviewRequirements:
    selfReview: true
    peerReview: true   # Partner review
    stakeholderReview: true  # Client approval

qualityGates:
  - id: partner_review
    name: Partner Review Gate
    stage: pre_output
    checks:
      - type: internal_stability
        description: All metrics must have HIGH stability internally
      - type: pyramid_structure
        description: Recommendations must follow pyramid principle
    onFailure: block
```

---

### 4.4 Constraint Templates Layer

The Constraint Templates Layer defines how to reduce LLM variance to measurable levels.

#### 4.4.1 Interface Definition

```typescript
interface ConstraintTemplate {
  /** Unique identifier */
  id: string;

  /** Human-readable name */
  name: string;

  /** Domain this template applies to */
  domain: string;

  /** Type of analysis */
  analysisType: "process" | "skill" | "synthesis" | "validation" | "extraction";

  /** The prompt template with placeholders */
  promptTemplate: string;

  /** Output constraints that reduce variance */
  outputConstraints: OutputConstraints;

  /** Execution constraints for consistency */
  executionConstraints: ExecutionConstraints;

  /** Post-processing verification */
  verificationChecklist: VerificationItem[];
}

interface OutputConstraints {
  /** Require exact numbers (no "approximately") */
  exactNumbers: boolean;

  /** Require explicit calculations shown */
  showCalculations: boolean;

  /** Required output structure */
  requiredFormat: FormatSpec;

  /** Patterns that indicate bad output */
  forbiddenPatterns: ForbiddenPattern[];

  /** Required fields in output */
  requiredFields: RequiredField[];

  /** Numeric constraints */
  numericConstraints: NumericConstraint[];
}

interface FormatSpec {
  /** Output format type */
  type: "json" | "markdown" | "structured_text" | "table";

  /** Schema for JSON outputs */
  jsonSchema?: JSONSchema;

  /** Template for markdown/text outputs */
  template?: string;

  /** Example of valid output */
  example: string;
}

interface ForbiddenPattern {
  /** Pattern name */
  name: string;

  /** Regex or keyword to detect */
  pattern: string;

  /** Why this is forbidden */
  reason: string;

  // Examples:
  // { name: "hedging", pattern: "\\b(approximately|around|about|roughly)\\b", reason: "Reduces precision" }
  // { name: "ranges", pattern: "\\d+-\\d+", reason: "Need exact numbers, not ranges" }
}

interface ExecutionConstraints {
  /** Start each run with fresh context */
  freshContext: boolean;

  /** Required system message */
  systemMessage?: string;

  /** Required step ordering */
  stepOrdering: ExecutionStep[];

  /** Pre-execution setup */
  setup: SetupStep[];
}

interface ExecutionStep {
  /** Step identifier */
  id: string;

  /** What this step does */
  description: string;

  /** The prompt for this step */
  prompt: string;

  /** Expected output format */
  expectedOutput: FormatSpec;

  /** Dependencies on previous steps */
  dependsOn: string[];
}

interface VerificationItem {
  /** Check identifier */
  id: string;

  /** Human-readable description */
  description: string;

  /** How to verify */
  verificationType: "regex" | "json_schema" | "numeric_check" | "custom";

  /** Verification configuration */
  config: VerificationConfig;

  /** What to do on failure */
  onFailure: "reprompt" | "flag" | "reject";

  /** Reprompt template if applicable */
  repromptTemplate?: string;
}
```

#### 4.4.2 Template Example

**Workflow Cycle Time Analysis:**
```yaml
id: workflow-cycle-time
name: Workflow Cycle Time Analysis
domain: workflow_analysis
analysisType: process

promptTemplate: |
  Analyze the following workflow artifacts to calculate cycle time metrics.

  ARTIFACTS:
  {{artifacts}}

  INSTRUCTIONS:
  1. Identify the workflow start date (first substantive action)
  2. Identify the workflow end date (final deliverable or approval)
  3. Calculate total elapsed time in calendar days
  4. Break down time into: active work, waiting, review/approval

  OUTPUT FORMAT (use exactly):
  ```
  CYCLE TIME ANALYSIS
  ==================
  Start Date: YYYY-MM-DD (source: [artifact name])
  End Date: YYYY-MM-DD (source: [artifact name])

  Total Elapsed: X days

  Breakdown:
  - Active Work: X days (XX%)
  - Waiting: X days (XX%)
  - Review/Approval: X days (XX%)

  Calculation:
  [Show date arithmetic explicitly]
  ```

  RULES:
  - Use exact dates, never "approximately" or "around"
  - Percentages must sum to 100%
  - Show your date calculations step by step
  - If dates are ambiguous, use the most conservative interpretation

outputConstraints:
  exactNumbers: true
  showCalculations: true
  requiredFormat:
    type: structured_text
    template: |
      CYCLE TIME ANALYSIS
      ==================
      Start Date: {{start_date}} (source: {{start_source}})
      End Date: {{end_date}} (source: {{end_source}})

      Total Elapsed: {{total_days}} days

      Breakdown:
      - Active Work: {{active_days}} days ({{active_pct}}%)
      - Waiting: {{waiting_days}} days ({{waiting_pct}}%)
      - Review/Approval: {{review_days}} days ({{review_pct}}%)

      Calculation:
      {{calculation_steps}}

  forbiddenPatterns:
    - name: hedging
      pattern: "\\b(approximately|around|about|roughly|estimated)\\b"
      reason: "Need exact numbers for statistical aggregation"
    - name: ranges
      pattern: "\\d+\\s*-\\s*\\d+\\s*(days|hours)"
      reason: "Need single values, not ranges"
    - name: ambiguity
      pattern: "\\b(unclear|uncertain|possibly|might be)\\b"
      reason: "Flag ambiguity explicitly, don't hedge"

  requiredFields:
    - name: start_date
      type: date
      format: "YYYY-MM-DD"
    - name: end_date
      type: date
      format: "YYYY-MM-DD"
    - name: total_days
      type: integer
      min: 0
    - name: breakdown_percentages
      type: percentage_set
      mustSumTo: 100

  numericConstraints:
    - field: breakdown_percentages
      constraint: sum_equals
      value: 100
      tolerance: 0.1

executionConstraints:
  freshContext: true
  systemMessage: |
    You are a workflow analyst. Your outputs will be aggregated across
    multiple runs for statistical analysis. Precision and consistency
    are critical. Never hedge or provide ranges.
  stepOrdering:
    - id: identify_boundaries
      description: Find workflow start and end
      prompt: "First, identify the workflow boundaries..."
      dependsOn: []
    - id: calculate_breakdown
      description: Break down time categories
      prompt: "Now break down the elapsed time..."
      dependsOn: [identify_boundaries]
  setup:
    - type: context_clear
      description: Start with fresh conversation context

verificationChecklist:
  - id: date_format
    description: Dates must be in YYYY-MM-DD format
    verificationType: regex
    config:
      pattern: "\\d{4}-\\d{2}-\\d{2}"
      fields: [start_date, end_date]
    onFailure: reprompt
    repromptTemplate: "Please provide {{field}} in YYYY-MM-DD format exactly."

  - id: percentage_sum
    description: Breakdown percentages must sum to 100%
    verificationType: numeric_check
    config:
      operation: sum
      fields: [active_pct, waiting_pct, review_pct]
      expected: 100
      tolerance: 0.5
    onFailure: reprompt
    repromptTemplate: "Your breakdown percentages sum to {{actual}}%. Please recalculate so they sum to exactly 100%."

  - id: calculation_shown
    description: Date arithmetic must be explicit
    verificationType: regex
    config:
      pattern: "\\d{4}-\\d{2}-\\d{2}.*(?:minus|to|-).*\\d{4}-\\d{2}-\\d{2}"
    onFailure: reprompt
    repromptTemplate: "Please show your date calculation explicitly (e.g., '2024-01-15 to 2024-01-22 = 7 days')."
```

---

### 4.5 Execution Engine Layer

The Execution Engine Layer defines how processing happens.

#### 4.5.1 Interface Definition

```typescript
interface ExecutionEngine {
  /** Execute a single item through a template */
  execute(
    item: BacklogItem,
    template: ConstraintTemplate,
    config: ExecutionConfig
  ): Promise<ExecutionResult>;

  /** Execute with multi-run aggregation */
  executeWithAggregation(
    item: BacklogItem,
    template: ConstraintTemplate,
    config: AggregationConfig
  ): Promise<AggregatedResult>;
}

interface ExecutionConfig {
  /** Execution mode */
  mode: "single" | "multi_run" | "production";

  /** LLM configuration */
  llm: {
    provider: "openai" | "anthropic" | "google" | "local";
    model: string;
    temperature: number;  // Recommend 0.0-0.3 for consistency
    maxTokens: number;
  };

  /** Timeout per run */
  timeoutMs: number;

  /** Retry configuration */
  retry: {
    maxAttempts: number;
    backoffMs: number;
  };
}

interface AggregationConfig extends ExecutionConfig {
  /** Number of runs for aggregation */
  iterations: number;  // Recommended: 3-5 for workshop, 50 for production

  /** Run in parallel or sequential */
  parallel: boolean;

  /** Maximum concurrent runs if parallel */
  maxConcurrency?: number;

  /** Aggregation method */
  aggregation: AggregationMethod;

  /** Outlier handling */
  outlierHandling: "include" | "flag" | "exclude";

  /** Outlier detection method if flagging/excluding */
  outlierDetection?: {
    method: "iqr" | "zscore" | "mad";
    threshold: number;
  };
}

interface AggregationMethod {
  /** How to combine numeric fields */
  numeric: "mean" | "median" | "mode";

  /** How to combine categorical fields */
  categorical: "majority" | "unanimous" | "distribution";

  /** Confidence interval calculation */
  confidenceInterval: {
    enabled: boolean;
    level: number;  // e.g., 0.95 for 95% CI
  };

  /** Stability scoring */
  stabilityScoring: {
    enabled: boolean;
    metric: "cv" | "iqr_ratio" | "custom";
    thresholds: {
      high: number;
      medium: number;
    };
  };
}

interface ExecutionResult {
  /** Unique run identifier */
  runId: string;

  /** Timestamp */
  executedAt: DateTime;

  /** Raw LLM output */
  rawOutput: string;

  /** Parsed structured output */
  parsedOutput: Record<string, unknown>;

  /** Verification results */
  verification: {
    passed: boolean;
    checks: VerificationCheckResult[];
  };

  /** Execution metadata */
  metadata: {
    durationMs: number;
    tokenCount: number;
    repromptCount: number;
  };
}

interface AggregatedResult {
  /** All individual run results */
  runs: ExecutionResult[];

  /** Aggregated values */
  aggregated: {
    [field: string]: AggregatedField;
  };

  /** Overall stability assessment */
  stability: {
    overall: "high" | "medium" | "low";
    byField: Record<string, "high" | "medium" | "low">;
  };

  /** Flags for human review */
  flags: ReviewFlag[];

  /** Recommended actions */
  recommendations: string[];
}

interface AggregatedField {
  /** Aggregated value */
  value: number | string;

  /** For numeric fields */
  numeric?: {
    mean: number;
    median: number;
    stdDev: number;
    cv: number;  // Coefficient of Variation
    confidenceInterval: {
      lower: number;
      upper: number;
      level: number;
    };
  };

  /** For categorical fields */
  categorical?: {
    distribution: Record<string, number>;  // value -> count
    majorityValue: string;
    agreement: number;  // 0-1, percentage agreeing with majority
  };

  /** Stability for this field */
  stability: "high" | "medium" | "low";
}

interface ReviewFlag {
  /** Flag type */
  type: "high_variance" | "outlier_detected" | "verification_failed" | "ambiguous_input";

  /** Affected fields */
  fields: string[];

  /** Human-readable description */
  description: string;

  /** Suggested action */
  suggestedAction: string;
}
```

#### 4.5.2 Stability Scoring Algorithm

```typescript
function calculateStability(
  values: number[],
  thresholds: { high: number; medium: number }
): "high" | "medium" | "low" {
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
  const stdDev = Math.sqrt(variance);
  const cv = stdDev / mean;  // Coefficient of Variation

  if (cv < thresholds.high) return "high";
  if (cv < thresholds.medium) return "medium";
  return "low";
}

// Default thresholds (from paper-mining-agents):
// high: 0.10 (CV < 10%)
// medium: 0.25 (CV < 25%)
// low: CV >= 25%
```

#### 4.5.3 Failure Handling

```typescript
interface FailureHandler {
  /** Handle parse failures */
  onParseFailure(
    rawOutput: string,
    template: ConstraintTemplate
  ): Promise<ParseRecoveryResult>;

  /** Handle verification failures */
  onVerificationFailure(
    result: ExecutionResult,
    failedChecks: VerificationCheckResult[]
  ): Promise<VerificationRecoveryResult>;

  /** Handle high variance */
  onHighVariance(
    aggregatedResult: AggregatedResult,
    highVarianceFields: string[]
  ): Promise<VarianceRecoveryResult>;
}

interface ParseRecoveryResult {
  /** Recovery method used */
  method: "regex_extraction" | "secondary_llm" | "human_review" | "failed";

  /** Recovered output if successful */
  recovered?: Record<string, unknown>;

  /** Error details if failed */
  error?: string;
}

// Recovery cascade:
// 1. Regex extraction (fast, deterministic)
// 2. Secondary LLM call with stricter prompt
// 3. Flag for human review
// 4. Mark as failed, exclude from aggregation
```

---

### 4.6 Output Validation Layer

The Output Validation Layer ensures outputs meet defensibility requirements.

#### 4.6.1 Interface Definition

```typescript
interface OutputValidator {
  /** Validate output against community standards */
  validate(
    output: AggregatedResult,
    community: ProfessionalCommunity
  ): Promise<ValidationResult>;

  /** Check all quality gates */
  checkQualityGates(
    output: AggregatedResult,
    gates: QualityGate[]
  ): Promise<QualityGateResult[]>;

  /** Generate review package for human reviewers */
  generateReviewPackage(
    output: AggregatedResult,
    community: ProfessionalCommunity
  ): Promise<ReviewPackage>;
}

interface ValidationResult {
  /** Overall pass/fail */
  passed: boolean;

  /** Evidence standards compliance */
  evidenceCompliance: {
    passed: boolean;
    missingRequired: RequiredElement[];
    forbiddenFound: ForbiddenElement[];
    traceabilityIssues: string[];
  };

  /** Defensibility compliance */
  defensibilityCompliance: {
    passed: boolean;
    stabilityMet: boolean;
    varianceFlags: string[];
    reviewsCompleted: Record<string, boolean>;
  };

  /** Detailed check results */
  checks: ValidationCheck[];

  /** Blocking issues */
  blockingIssues: string[];

  /** Warnings (non-blocking) */
  warnings: string[];
}

interface ReviewPackage {
  /** Summary for reviewers */
  summary: {
    itemId: string;
    templateUsed: string;
    iterationsRun: number;
    overallStability: "high" | "medium" | "low";
    flagCount: number;
  };

  /** Aggregated output with confidence bounds */
  output: AggregatedResult;

  /** Individual runs for inspection */
  runs: ExecutionResult[];

  /** Variance analysis */
  varianceAnalysis: {
    fieldStability: Record<string, "high" | "medium" | "low">;
    problematicFields: string[];
    varianceVisualization: string;  // ASCII or chart
  };

  /** Flags requiring attention */
  flags: ReviewFlag[];

  /** Reviewer checklist */
  reviewerChecklist: ReviewerChecklistItem[];

  /** Sign-off requirements */
  signOffRequirements: {
    selfReview: { required: boolean; completed: boolean; by?: string };
    peerReview: { required: boolean; completed: boolean; by?: string };
    stakeholderReview: { required: boolean; completed: boolean; by?: string };
  };
}

interface ReviewerChecklistItem {
  /** Check identifier */
  id: string;

  /** Description of what to verify */
  description: string;

  /** Whether this is auto-verified or requires human judgment */
  autoVerified: boolean;

  /** Auto-verification result if applicable */
  autoResult?: boolean;

  /** Guidance for human reviewers */
  humanGuidance?: string;
}
```

#### 4.6.2 Output Presentation

The system formats outputs differently based on community requirements:

**Academic (show uncertainty):**
```
Cycle Time: 14.7 days (±1.2 SD, 95% CI: 12.3-17.1)
Stability: HIGH (CV = 0.08)

Breakdown:
- Active Work: 8.2 days (56%) [MEDIUM stability, CV = 0.18]
- Waiting: 4.1 days (28%) [HIGH stability, CV = 0.09]
- Review: 2.4 days (16%) [LOW stability - flagged for review]
```

**Consulting (hide uncertainty, ensure internal confidence):**
```
Cycle Time: 15 days

Breakdown:
- Active Work: 8 days (55%)
- Waiting: 4 days (27%)
- Review: 3 days (18%)

[Internal note: All metrics achieved HIGH stability. Safe for client presentation.]
```

---

## 5. Domain Configurations

The same core engine instantiates differently per domain:

### 5.1 Configuration Matrix

| Domain | Backlog Type | Community | Constraint Focus | Execution | Output |
|--------|--------------|-----------|------------------|-----------|--------|
| **Academic Research** | Datasets, transcripts | Sociology journals | Exact calcs, no hedging | N=50, CV scoring | Paper sections + CI |
| **Management Consulting** | Client artifacts | Partner + Client | Pyramid structure, exec summary | N=10, internal CV | Deck slides |
| **Clinical Diagnosis** | Patient encounters | AMA + Patient | SOAP format, differential dx | Single + peer | Treatment plan |
| **Legal Research** | Case files | Bar + Court | Citation format, issue-spotting | Single + partner | Legal memo |
| **Student Grading** | Submissions | Course rubric | Rubric application | N=50, Monte Carlo | Grade + feedback |
| **Grant Writing** | Preliminary data | Funder + Field | Specific aims format | Iterative + mentor | Proposal |
| **Due Diligence** | Target company docs | Investment committee | Risk identification | N=5, consensus | Investment memo |
| **Journalism** | Source interviews | Editorial standards | Fact-checking, attribution | Single + editor | Article draft |

### 5.2 Community Configuration Files

Store as YAML in `communities/` directory:

```
communities/
├── academic-sociology.yaml
├── management-consulting.yaml
├── clinical-medicine.yaml
├── legal-research.yaml
├── k12-education.yaml
├── higher-ed-grading.yaml
├── grant-writing-nih.yaml
├── grant-writing-nsf.yaml
├── investigative-journalism.yaml
└── private-equity-dd.yaml
```

Each file contains the full `ProfessionalCommunity` configuration.

---

## 6. Implementation Architecture

### 6.1 Directory Structure

```
knowledge-backlog-processor/
├── packages/
│   ├── core/                      # Core engine (domain-agnostic)
│   │   ├── src/
│   │   │   ├── engine/
│   │   │   │   ├── executor.ts        # Single-run execution
│   │   │   │   ├── aggregator.ts      # Multi-run aggregation
│   │   │   │   ├── stability.ts       # CV calculation, stability scoring
│   │   │   │   └── failure-handler.ts # Recovery cascade
│   │   │   ├── validation/
│   │   │   │   ├── validator.ts       # Output validation
│   │   │   │   ├── quality-gates.ts   # Gate checking
│   │   │   │   └── review-package.ts  # Generate review materials
│   │   │   ├── types/
│   │   │   │   ├── backlog.ts
│   │   │   │   ├── community.ts
│   │   │   │   ├── template.ts
│   │   │   │   ├── execution.ts
│   │   │   │   └── output.ts
│   │   │   └── index.ts
│   │   └── package.json
│   │
│   ├── adapters/                  # Backlog source adapters
│   │   ├── filesystem/
│   │   ├── notion/
│   │   ├── slack/
│   │   ├── google-drive/
│   │   └── api/
│   │
│   └── cli/                       # Command-line interface
│       ├── src/
│       │   ├── commands/
│       │   │   ├── process.ts         # Process backlog items
│       │   │   ├── validate.ts        # Validate outputs
│       │   │   ├── review.ts          # Generate review packages
│       │   │   └── configure.ts       # Manage communities/templates
│       │   └── index.ts
│       └── package.json
│
├── communities/                   # Community configurations (YAML)
│   ├── academic-sociology.yaml
│   ├── management-consulting.yaml
│   └── ...
│
├── templates/                     # Constraint templates (YAML)
│   ├── workflow-analysis/
│   │   ├── cycle-time.yaml
│   │   ├── bottleneck.yaml
│   │   └── handoff.yaml
│   ├── literature-synthesis/
│   │   ├── systematic-review.yaml
│   │   └── gap-analysis.yaml
│   └── ...
│
├── docs/
│   ├── SPECIFICATION.md           # This document
│   ├── GETTING_STARTED.md
│   ├── COMMUNITY_GUIDE.md         # How to define new communities
│   ├── TEMPLATE_GUIDE.md          # How to create templates
│   └── API_REFERENCE.md
│
└── examples/
    ├── academic-research/
    ├── consulting/
    └── grading/
```

### 6.2 Core Engine Interface

```typescript
// Main entry point
import { KnowledgeBacklogProcessor } from '@kbp/core';
import { FileSystemAdapter } from '@kbp/adapters-filesystem';

const processor = new KnowledgeBacklogProcessor({
  community: 'academic-sociology',
  llm: {
    provider: 'anthropic',
    model: 'claude-3-sonnet',
    temperature: 0.1,
  },
});

// Process a single item
const result = await processor.process({
  backlog: new FileSystemAdapter('./data/transcripts'),
  template: 'literature-synthesis/gap-analysis',
  execution: {
    mode: 'production',
    iterations: 50,
    parallel: true,
  },
});

// Check quality gates
const gateResults = await processor.checkGates(result);

// Generate review package
const reviewPackage = await processor.generateReviewPackage(result);
```

---

## 7. Progression Model

Users progress through trust levels as they gain confidence in the system:

### 7.1 Progression Stages

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         TRUST PROGRESSION                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  STAGE 1: LEARNING                                                      │
│  ─────────────────                                                      │
│  • Manual execution (copy/paste prompts)                                │
│  • Single runs with manual verification                                 │
│  • User learns what variance means                                      │
│  • Goal: Build intuition for when to trust outputs                      │
│                                                                         │
│                          ↓                                              │
│                                                                         │
│  STAGE 2: MEASURING                                                     │
│  ──────────────────                                                     │
│  • Manual execution with 3-5 runs                                       │
│  • Comparison table shows variance                                      │
│  • User learns to recognize stable vs unstable outputs                  │
│  • Goal: Understand which outputs are defensible                        │
│                                                                         │
│                          ↓                                              │
│                                                                         │
│  STAGE 3: TRUSTING                                                      │
│  ─────────────────                                                      │
│  • Automated execution with N=50                                        │
│  • Statistical aggregation with CI                                      │
│  • Stability flags guide human review                                   │
│  • Goal: Efficient processing with appropriate oversight                │
│                                                                         │
│                          ↓                                              │
│                                                                         │
│  STAGE 4: INTEGRATING                                                   │
│  ────────────────────                                                   │
│  • Full pipeline automation                                             │
│  • Exception-based human review only                                    │
│  • Continuous monitoring of stability metrics                           │
│  • Goal: Production-scale backlog processing                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Stage Transitions

Transition criteria from Stage N to Stage N+1:

| Transition | Criteria |
|------------|----------|
| 1 → 2 | User has run 10+ single analyses, understands verification checklist |
| 2 → 3 | User has compared 5+ multi-run outputs, correctly predicted stability |
| 3 → 4 | 90%+ of flagged items were correctly triaged for human review |

---

## 8. Quality Assurance

### 8.1 System-Level Quality Metrics

```typescript
interface SystemQualityMetrics {
  /** What percentage of outputs achieve target stability? */
  stabilityRate: {
    high: number;    // % of outputs with HIGH stability
    medium: number;  // % with MEDIUM stability
    low: number;     // % with LOW stability (requiring review)
  };

  /** How often do quality gates block submission? */
  gateBlockRate: number;

  /** How often do flagged items actually need intervention? */
  flagPrecision: number;  // True positives / (True positives + False positives)

  /** How often do unflagged items later reveal problems? */
  flagRecall: number;     // True positives / (True positives + False negatives)

  /** Average time from backlog entry to validated output */
  processingLatency: {
    p50: number;
    p90: number;
    p99: number;
  };

  /** Cost per processed item */
  costPerItem: {
    llmTokens: number;
    humanReviewMinutes: number;
    totalDollars: number;
  };
}
```

### 8.2 Pilot Success Criteria

Before moving to production:

1. **Stability Target**: >80% of metrics achieve MEDIUM or HIGH stability
2. **Gate Accuracy**: <5% of blocked outputs were actually acceptable
3. **Flag Precision**: >70% of flagged items genuinely needed review
4. **Flag Recall**: <10% of unflagged items had issues discovered later
5. **User Trust**: Users report >7/10 confidence in high-stability outputs

### 8.3 Monitoring Dashboard

Track over time:
- Stability distribution by template
- Gate block rate by community
- Flag precision/recall trends
- User override patterns (when users proceed despite flags)
- Processing latency trends

---

## 9. Future Directions

### 9.1 Near-Term (v0.2-0.3)

- **Template Authoring UI**: Visual tool for creating constraint templates
- **Community Library**: Shareable community configurations
- **Adapter Marketplace**: Community-contributed backlog adapters
- **Multi-LLM Ensemble**: Run across multiple providers to detect model-specific variance

### 9.2 Medium-Term (v0.4-0.6)

- **Active Learning**: System learns which items need more runs based on content features
- **Adaptive Thresholds**: Stability thresholds adjust per template based on historical performance
- **Cross-Template Synthesis**: Combine outputs from multiple templates into coherent deliverables
- **Collaborative Review**: Multi-stakeholder review workflows with role-based gates

### 9.3 Long-Term (v1.0+)

- **Domain Transfer Learning**: Templates that work in one domain inform templates in related domains
- **Automated Template Generation**: System proposes templates based on backlog analysis
- **Continuous Calibration**: Real-world outcome feedback improves stability predictions
- **Professional Community Integration**: Direct integration with journal submission systems, clinical record systems, etc.

---

## Appendix A: Reference Implementation Status

This specification emerged from the following implemented systems:

| System | Status | Coverage |
|--------|--------|----------|
| paper-mining-agents | Active | Academic research, sociology journals |
| living-paper | Active | Claim-evidence traceability, pre-review workflow |
| teamraderie-workshop | Live | Manual/workshop execution mode |
| workflow-analysis-platform | Concept | Production execution (planned) |
| grading-experiment-2025 | Pilot | Student grading, Monte Carlo |

---

## Appendix B: Glossary

**Backlog**: Collection of discrete work units awaiting processing.

**Coefficient of Variation (CV)**: Standard deviation divided by mean; measures relative variability.

**Constraint Template**: Structured prompt with explicit output requirements that reduce LLM variance.

**Defensibility**: Property allowing professionals to stake reputation on an output.

**Ghost Run**: Processing a killed item anyway to measure false kill rate; used for calibration.

**Graveyard**: Storage for killed backlog items, preserving kill reasons and enabling potential resurrection.

**Kill Rate**: Percentage of items rejected at a given triage stage.

**Professional Community**: Group with shared standards for valid evidence and acceptable outputs.

**Quality Gate**: Checkpoint that must pass before output proceeds to next stage.

**Resurrection**: Re-evaluating a previously killed item after conditions change.

**Stability Score**: Assessment of output consistency across multiple runs (HIGH/MEDIUM/LOW).

**Triage Funnel**: Multi-stage filter that progressively eliminates backlog items, with increasing investment at each stage. Most items die early and cheap; survivors receive full processing.

---

## Appendix C: Changelog

| Version | Date | Changes |
|---------|------|---------|
| 0.2.0 | 2025-01-08 | Added Triage Layer (Section 4.2) with iterative funnel design, graveyard management, calibration metrics |
| 0.1.0 | 2025-01-08 | Initial specification |

---

*This specification is a living document. Updates will be tracked in the changelog.*
