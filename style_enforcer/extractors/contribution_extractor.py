"""
Contribution Extractor - Extract paper contributions from findings/discussion.

This module uses LLM-based analysis to extract the core claims and contributions
from a paper's findings and discussion sections. These extracted contributions
are then used to check whether the theory section pre-announces them.
"""

import json
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ExtractedContribution:
    """A contribution/claim extracted from findings or discussion."""
    claim: str                    # The substantive claim
    evidence_type: str            # "qual_finding", "quant_result", "theoretical_extension"
    section_source: str           # "findings" or "discussion"
    mechanism_if_any: Optional[str] = None  # If the paper explains WHY/HOW
    named_concept_if_any: Optional[str] = None  # If the paper coins a term

    def to_dict(self) -> dict:
        return {
            "claim": self.claim,
            "evidence_type": self.evidence_type,
            "section_source": self.section_source,
            "mechanism_if_any": self.mechanism_if_any,
            "named_concept_if_any": self.named_concept_if_any,
        }

    @classmethod
    def from_dict(cls, data: dict, section: str = "unknown") -> "ExtractedContribution":
        return cls(
            claim=data.get("claim", ""),
            evidence_type=data.get("evidence_type", "unknown"),
            section_source=section,
            mechanism_if_any=data.get("mechanism_if_any"),
            named_concept_if_any=data.get("named_concept_if_any"),
        )


EXTRACTION_PROMPT = """You are analyzing a qualitative/inductive research paper. Extract the paper's core contributions from its Findings and Discussion sections.

For each contribution, identify:
1. The substantive claim (what the paper argues it discovered)
2. Whether it involves a mechanism explanation (HOW/WHY something happens)
3. Whether the paper coins a new term or concept
4. The specific evidence type (qualitative finding, quantitative pattern, theoretical extension)

Be thorough - capture ALL claims the paper makes about what it found.
Focus on SUBSTANTIVE claims, not methodological notes or literature reviews.

FINDINGS SECTION:
{findings_text}

---

DISCUSSION SECTION:
{discussion_text}

---

Return your analysis as valid JSON with this exact structure:
{{
  "contributions": [
    {{
      "claim": "The substantive claim in a single sentence",
      "mechanism_if_any": "The causal mechanism if the paper explains WHY/HOW, or null",
      "named_concept_if_any": "Any coined term like 'shadow learning' or 'developmental uncertainty', or null",
      "evidence_type": "qual_finding" | "quant_result" | "theoretical_extension"
    }}
  ]
}}

Extract 3-8 core contributions. Prioritize the most important claims."""


class ContributionExtractor:
    """
    Extracts contributions from paper findings and discussion using LLM.

    Usage:
        extractor = ContributionExtractor(llm_client)
        contributions = extractor.extract(findings_text, discussion_text)
    """

    def __init__(self, llm_client: Any):
        """
        Initialize with an LLM client.

        Args:
            llm_client: Any LLM client with a chat() or generate() method.
                       Expected interface: client.chat(prompt) -> str
        """
        self.llm = llm_client

    def extract(
        self,
        findings: str,
        discussion: str,
    ) -> list[ExtractedContribution]:
        """
        Extract contributions from findings and discussion sections.

        Args:
            findings: The findings section text
            discussion: The discussion section text

        Returns:
            List of extracted contributions
        """
        if not findings and not discussion:
            return []

        # Build the prompt
        prompt = EXTRACTION_PROMPT.format(
            findings_text=findings or "(No findings section provided)",
            discussion_text=discussion or "(No discussion section provided)",
        )

        # Call the LLM
        response = self._call_llm(prompt)

        # Parse the response
        return self._parse_response(response)

    def _call_llm(self, prompt: str) -> str:
        """Call the LLM with the prompt."""
        # Support different LLM client interfaces
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

    def _parse_response(self, response: str) -> list[ExtractedContribution]:
        """Parse LLM response into ExtractedContribution objects."""
        try:
            # Try to extract JSON from response
            # Handle case where LLM wraps JSON in markdown code blocks
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]

            data = json.loads(json_str.strip())
            contributions = []

            for item in data.get("contributions", []):
                contrib = ExtractedContribution.from_dict(item, section="findings")
                contributions.append(contrib)

            return contributions

        except (json.JSONDecodeError, KeyError, IndexError) as e:
            # If parsing fails, return empty list
            # In production, would log this error
            print(f"Warning: Failed to parse LLM response: {e}")
            return []

    def extract_summary(
        self,
        contributions: list[ExtractedContribution],
    ) -> str:
        """
        Generate a summary of contributions for use in other prompts.

        Args:
            contributions: List of extracted contributions

        Returns:
            Formatted summary string
        """
        if not contributions:
            return "(No contributions extracted)"

        lines = []
        for i, c in enumerate(contributions, 1):
            line = f"{i}. {c.claim}"
            if c.named_concept_if_any:
                line += f" [concept: '{c.named_concept_if_any}']"
            if c.mechanism_if_any:
                line += f" [mechanism: {c.mechanism_if_any}]"
            lines.append(line)

        return "\n".join(lines)
