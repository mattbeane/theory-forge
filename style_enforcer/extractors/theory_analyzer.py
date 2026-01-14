"""
Theory Analyzer - Analyze intro/theory sections for inductive structure.

This module uses LLM-based analysis to check whether the intro and theory
sections properly set up a puzzle → gap → question flow WITHOUT pre-announcing
the findings that should emerge later.
"""

import json
from dataclasses import dataclass, field
from typing import Any, Optional

from .contribution_extractor import ExtractedContribution


@dataclass
class PreannouncementEvidence:
    """Evidence that theory section pre-announces a finding."""
    finding_claim: str          # The claim from findings
    theory_text: str            # The text from theory that pre-announces it
    similarity_explanation: str  # Why these are considered similar
    severity: str = "high"      # "high", "medium", "low"


@dataclass
class TheoryAnalysis:
    """Analysis of intro/theory section structure."""
    prior_concepts: list[str] = field(default_factory=list)  # Concepts from prior lit
    gap_statement: Optional[str] = None  # The identified gap (if any)
    research_questions: list[str] = field(default_factory=list)  # The paper's RQs
    preannouncements: list[PreannouncementEvidence] = field(default_factory=list)
    overall_structure: str = "unknown"  # "inductive", "deductive", "mixed"
    structure_rating: int = 3  # 1-5, where 5 is pure inductive discovery

    @property
    def has_preannouncements(self) -> bool:
        return len(self.preannouncements) > 0

    @property
    def is_properly_inductive(self) -> bool:
        return (
            self.overall_structure == "inductive"
            and not self.has_preannouncements
            and self.structure_rating >= 4
        )


PREANNOUNCEMENT_PROMPT = """You are analyzing whether a theory section pre-announces findings (a violation for inductive papers).

CONTEXT: In inductive qualitative papers, the theory section should:
- Review PRIOR literature and concepts (what others have found/theorized)
- Identify a GAP (what's unknown/unexplained by prior work)
- Pose a QUESTION that the findings will answer
- NOT describe the mechanism or framework that findings will reveal

The key test: Does the theory section describe what THIS PAPER discovers, or only what PRIOR WORK has established?

FINDINGS/CONTRIBUTIONS (extracted from the paper's findings/discussion):
{contributions_text}

---

THEORY SECTION TEXT:
{theory_text}

---

For each finding/contribution listed above, check if the theory section ALREADY describes it.
A pre-announcement occurs when the theory section:
- Describes the same mechanism/dynamic the findings reveal
- Names the same concept that findings introduce
- Explains WHY something happens before findings provide the evidence
- States as fact what findings should discover

Return your analysis as valid JSON with this exact structure:
{{
  "preannouncements": [
    {{
      "finding_claim": "The contribution/finding being pre-announced",
      "theory_text_that_preannounces": "The exact text from theory section",
      "similarity_explanation": "Why this counts as pre-announcing the finding",
      "severity": "high" | "medium" | "low"
    }}
  ],
  "gap_statement_if_present": "The gap statement if one exists, or null",
  "research_questions": ["Each research question posed in the theory section"],
  "overall_structure": "inductive" | "deductive" | "mixed",
  "prior_concepts": ["Key concepts from prior literature (not from this paper)"]
}}

Be strict: If the theory section describes what managers DO, what facilities ARE, how mechanisms WORK - and these match the findings - that's a pre-announcement."""


STRUCTURE_PROMPT = """You are checking whether a paper has proper inductive structure.

PROPER INDUCTIVE STRUCTURE (discovery):
1. PUZZLE: "Here's a phenomenon that existing theory doesn't explain well"
2. GAP: "Prior work has focused on X, but we don't know Y"
3. QUESTION: "So we ask: [question that findings will answer]"
4. ANSWER: Findings reveal Y (reader experiences DISCOVERY)

PROBLEMATIC HYPO-DEDUCTIVE STRUCTURE (confirmation):
1. PREVIEW: "We propose a theory of X with these mechanisms..."
2. DERIVATION: "This suggests we would see patterns A, B, C..."
3. CONFIRMATION: Findings show A, B, C (reader experiences CONFIRMATION)

Key diagnostic: When you reach the findings, do they feel SURPRISING (discovery) or EXPECTED (confirmation)?
If the theory section told you what you'd find, it's confirmation disguised as discovery.

---

INTRODUCTION:
{intro_text}

---

THEORY SECTION:
{theory_text}

---

FINDINGS SUMMARY (what the paper claims to discover):
{findings_summary}

---

Analyze this paper and rate its structure from 1-5:
- 5: Pure inductive discovery - theory sets up puzzle, findings are surprising
- 4: Mostly inductive - minor preview but mainly discovery
- 3: Mixed - some substantial preview, some discovery
- 2: Mostly deductive - theory telegraphs findings
- 1: Pure deductive - theory describes exactly what findings show

Return your analysis as valid JSON:
{{
  "structure_rating": <1-5>,
  "puzzle_statement": "The puzzle if one is clearly articulated, or null",
  "gap_statement": "The gap in literature if clearly stated, or null",
  "preview_evidence": ["Any text that previews/pre-announces findings"],
  "diagnosis": "Your assessment of why this structure is inductive or deductive"
}}"""


class TheoryAnalyzer:
    """
    Analyzes intro/theory sections for proper inductive structure.

    Usage:
        analyzer = TheoryAnalyzer(llm_client)
        analysis = analyzer.analyze(intro, theory, contributions)
    """

    def __init__(self, llm_client: Any):
        """
        Initialize with an LLM client.

        Args:
            llm_client: Any LLM client with a chat() or generate() method.
        """
        self.llm = llm_client

    def analyze(
        self,
        intro: str,
        theory: str,
        contributions: list[ExtractedContribution],
    ) -> TheoryAnalysis:
        """
        Analyze intro/theory sections for inductive structure.

        Args:
            intro: Introduction section text
            theory: Theory/background section text
            contributions: Extracted contributions from findings/discussion

        Returns:
            TheoryAnalysis with structure assessment and pre-announcement detection
        """
        # First, check for pre-announcements
        preannouncement_result = self._check_preannouncements(
            theory,
            contributions,
        )

        # Then, check overall structure
        structure_result = self._check_structure(
            intro,
            theory,
            contributions,
        )

        # Combine results
        return TheoryAnalysis(
            prior_concepts=preannouncement_result.get("prior_concepts", []),
            gap_statement=preannouncement_result.get("gap_statement_if_present")
                         or structure_result.get("gap_statement"),
            research_questions=preannouncement_result.get("research_questions", []),
            preannouncements=[
                PreannouncementEvidence(
                    finding_claim=p.get("finding_claim", ""),
                    theory_text=p.get("theory_text_that_preannounces", ""),
                    similarity_explanation=p.get("similarity_explanation", ""),
                    severity=p.get("severity", "medium"),
                )
                for p in preannouncement_result.get("preannouncements", [])
            ],
            overall_structure=preannouncement_result.get("overall_structure", "unknown"),
            structure_rating=structure_result.get("structure_rating", 3),
        )

    def _check_preannouncements(
        self,
        theory: str,
        contributions: list[ExtractedContribution],
    ) -> dict:
        """Check for pre-announcements in theory section."""
        if not theory:
            return {}

        # Format contributions for prompt
        contrib_lines = []
        for i, c in enumerate(contributions, 1):
            line = f"{i}. {c.claim}"
            if c.mechanism_if_any:
                line += f"\n   Mechanism: {c.mechanism_if_any}"
            if c.named_concept_if_any:
                line += f"\n   Named concept: '{c.named_concept_if_any}'"
            contrib_lines.append(line)

        contributions_text = "\n".join(contrib_lines) if contrib_lines else "(No contributions)"

        prompt = PREANNOUNCEMENT_PROMPT.format(
            contributions_text=contributions_text,
            theory_text=theory,
        )

        response = self._call_llm(prompt)
        return self._parse_json_response(response)

    def _check_structure(
        self,
        intro: str,
        theory: str,
        contributions: list[ExtractedContribution],
    ) -> dict:
        """Check overall puzzle → gap → question → answer structure."""
        # Create findings summary
        findings_summary = "\n".join(
            f"- {c.claim}" for c in contributions
        ) if contributions else "(No findings extracted)"

        prompt = STRUCTURE_PROMPT.format(
            intro_text=intro or "(No introduction provided)",
            theory_text=theory or "(No theory section provided)",
            findings_summary=findings_summary,
        )

        response = self._call_llm(prompt)
        return self._parse_json_response(response)

    def _call_llm(self, prompt: str) -> str:
        """Call the LLM with the prompt."""
        if hasattr(self.llm, 'chat'):
            return self.llm.chat(prompt)
        elif hasattr(self.llm, 'generate'):
            return self.llm.generate(prompt)
        elif hasattr(self.llm, 'complete'):
            return self.llm.complete(prompt)
        elif callable(self.llm):
            return self.llm(prompt)
        else:
            raise ValueError(
                "LLM client must have chat(), generate(), complete() method, "
                "or be callable"
            )

    def _parse_json_response(self, response: str) -> dict:
        """Parse JSON from LLM response."""
        try:
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]

            return json.loads(json_str.strip())

        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"Warning: Failed to parse LLM response: {e}")
            return {}
