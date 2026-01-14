#!/usr/bin/env python3
"""
Test script for coherence validator using mock LLM responses.

This demonstrates what the coherence validator would catch with
example text from a problematic paper structure.
"""

import json

from .extractors import ContributionExtractor, TheoryAnalyzer, ExtractedContribution
from .coherence_validator import CoherenceValidator, CoherenceReport


class MockLLMClient:
    """
    Mock LLM client that returns predetermined responses for testing.

    In production, this would be replaced with an actual LLM client.
    """

    def __init__(self, extraction_response: dict, preannouncement_response: dict, structure_response: dict):
        self.extraction_response = extraction_response
        self.preannouncement_response = preannouncement_response
        self.structure_response = structure_response
        self._call_count = 0

    def chat(self, prompt: str) -> str:
        """Return mock response based on prompt content."""
        self._call_count += 1

        # Determine which response to return based on prompt keywords
        # Order matters - more specific checks first
        if "Extract the paper's core contributions" in prompt:
            return json.dumps(self.extraction_response)
        elif "PROPER INDUCTIVE STRUCTURE" in prompt:  # Structure prompt uses caps header
            return json.dumps(self.structure_response)
        elif "pre-announces findings" in prompt:
            return json.dumps(self.preannouncement_response)
        else:
            return "{}"


def test_problematic_paper():
    """
    Test with a paper that has confirmatory structure.

    This simulates what we'd detect in the Learning to Automate paper
    BEFORE the manual fixes.
    """
    print("=" * 70)
    print("TEST: Problematic Paper (Confirmatory Structure)")
    print("=" * 70)

    # Simulate what the paper looked like before fixes
    theory_text = """
    We propose that multi-site firms distributing automation spatially across facilities
    will assign different learning roles to different sites. Exploration-focused facilities
    absorb learning costs and function as sites for experimentation. Exploitation-focused
    facilities capture the benefits of proven technology. Managers expect exploration nodes
    to show higher variability and lower productivity initially, while exploitation nodes
    show stable, optimized performance.

    This suggests we would attend to: (1) whether facilities differ in their assigned roles,
    (2) how role assignment affects operational outcomes, and (3) whether pooling across
    roles obscures systematic patterns.
    """

    findings_text = """
    We find that firms indeed assign different learning roles to facilities. Some serve as
    exploration sites that absorb uncertainty, while others function as exploitation sites
    that capture proven technology's benefits. This role assignment produces systematically
    different operational outcomes: exploration sites show higher variability and learning
    curves, while exploitation sites show stable, optimized performance. Pooling across
    roles obscures these systematic patterns.
    """

    discussion_text = """
    Our findings contribute to automation research by showing that firms distribute
    automation spatially with differentiated learning roles. The concept of "learning roles"
    extends organizational learning theory to multi-site automation contexts.
    """

    # Mock LLM responses
    extraction_response = {
        "contributions": [
            {
                "claim": "Firms assign different learning roles to facilities (exploration vs exploitation)",
                "mechanism_if_any": "Role assignment affects operational outcomes because exploration sites absorb learning costs while exploitation sites capture benefits",
                "named_concept_if_any": "learning roles",
                "evidence_type": "qual_finding"
            },
            {
                "claim": "Role assignment produces systematically different operational outcomes",
                "mechanism_if_any": "Exploration sites show higher variability, exploitation sites show stable performance",
                "named_concept_if_any": None,
                "evidence_type": "quant_result"
            },
            {
                "claim": "Pooling across roles obscures systematic patterns",
                "mechanism_if_any": None,
                "named_concept_if_any": None,
                "evidence_type": "theoretical_extension"
            }
        ]
    }

    preannouncement_response = {
        "preannouncements": [
            {
                "finding_claim": "Firms assign different learning roles to facilities (exploration vs exploitation)",
                "theory_text_that_preannounces": "We propose that multi-site firms distributing automation spatially across facilities will assign different learning roles to different sites. Exploration-focused facilities absorb learning costs...",
                "similarity_explanation": "Theory section describes the exact finding: firms assign learning roles (exploration vs exploitation) and what each role entails",
                "severity": "high"
            },
            {
                "finding_claim": "Role assignment produces systematically different operational outcomes",
                "theory_text_that_preannounces": "Managers expect exploration nodes to show higher variability and lower productivity initially, while exploitation nodes show stable, optimized performance",
                "similarity_explanation": "Theory section describes the mechanism (how roles produce different outcomes) before findings reveal it",
                "severity": "high"
            }
        ],
        "gap_statement_if_present": None,
        "research_questions": ["whether facilities differ in their assigned roles", "how role assignment affects operational outcomes"],
        "overall_structure": "deductive",
        "prior_concepts": ["organizational learning", "ambidexterity"]
    }

    structure_response = {
        "structure_rating": 2,
        "puzzle_statement": None,
        "gap_statement": None,
        "preview_evidence": [
            "We propose that multi-site firms distributing automation spatially across facilities will assign different learning roles",
            "Managers expect exploration nodes to show higher variability"
        ],
        "diagnosis": "Theory section reads as a preview of findings. It describes the learning roles framework and what we'd expect to see, making findings feel like confirmation rather than discovery."
    }

    # Create mock client and run validation
    mock_client = MockLLMClient(
        extraction_response=extraction_response,
        preannouncement_response=preannouncement_response,
        structure_response=structure_response,
    )

    validator = CoherenceValidator(mock_client)

    paper_sections = {
        "introduction": "We study how firms implement automation across multiple sites...",
        "theory": theory_text,
        "findings": findings_text,
        "discussion": discussion_text,
    }

    report = validator.validate(paper_sections)

    print(report.format_report())

    # Assertions for testing
    assert report.has_violations, "Should detect violations"
    assert report.critical_count >= 2, f"Should have at least 2 critical violations, got {report.critical_count}"
    assert report.structure_rating <= 3, f"Structure rating should be low, got {report.structure_rating}"
    assert not report.is_properly_inductive, "Should NOT be properly inductive"

    print("\n✅ Test passed: Detected confirmatory structure as expected\n")


def test_properly_inductive_paper():
    """
    Test with a paper that has proper inductive structure.

    This simulates what Shadow Learning looks like (the exemplar).
    """
    print("=" * 70)
    print("TEST: Properly Inductive Paper (Discovery Structure)")
    print("=" * 70)

    theory_text = """
    Communities of practice cannot persist without training new members. Much consequential
    learning occurs through legitimate peripheral participation in experts' work. However,
    economic and efficiency pressures, coupled with technologies that allow experts to work
    without assistance, often mean trainees get less meaningful exposure to experts in action.

    Studies of learning in communities of practice have not focused on this problem; they
    have treated legitimate peripheral participation as a given. So what do trainees do
    to learn when approved practices are insufficient? This remains unexplored.
    """

    findings_text = """
    I found that learning in robotic surgery required what I call "shadow learning": an
    interconnected set of norm- and policy-challenging practices enacted extensively,
    opportunistically, and in relative isolation. Successful trainees engaged in unauthorized
    practice on simulators, sought out clandestine mentorship, and created informal
    learning networks outside official channels.
    """

    discussion_text = """
    This study expands our conceptions of learning in communities of practice by showing
    that when technological change allows experts to work with less help, successful
    trainees may learn through shadow learning. The concept of "shadow learning" captures
    how trainees navigate barriers to legitimate peripheral participation.
    """

    extraction_response = {
        "contributions": [
            {
                "claim": "When approved learning practices are insufficient, trainees engage in shadow learning",
                "mechanism_if_any": "Shadow learning involves unauthorized practice, clandestine mentorship, and informal networks",
                "named_concept_if_any": "shadow learning",
                "evidence_type": "qual_finding"
            },
            {
                "claim": "Technological change that reduces need for trainee help creates barriers to legitimate peripheral participation",
                "mechanism_if_any": None,
                "named_concept_if_any": None,
                "evidence_type": "qual_finding"
            }
        ]
    }

    preannouncement_response = {
        "preannouncements": [],  # No pre-announcements!
        "gap_statement_if_present": "Studies of learning in communities of practice have not focused on this problem; they have treated legitimate peripheral participation as a given",
        "research_questions": ["what do trainees do to learn when approved practices are insufficient?"],
        "overall_structure": "inductive",
        "prior_concepts": ["legitimate peripheral participation", "communities of practice", "technological change"]
    }

    structure_response = {
        "structure_rating": 5,
        "puzzle_statement": "economic and efficiency pressures mean trainees get less meaningful exposure",
        "gap_statement": "Studies have not focused on this problem; they have treated legitimate peripheral participation as a given",
        "preview_evidence": [],
        "diagnosis": "Theory sets up a genuine puzzle (trainees excluded from legitimate participation) and asks what they do about it. The answer (shadow learning) is a discovery, not a confirmation."
    }

    mock_client = MockLLMClient(
        extraction_response=extraction_response,
        preannouncement_response=preannouncement_response,
        structure_response=structure_response,
    )

    validator = CoherenceValidator(mock_client)

    paper_sections = {
        "introduction": "We have known for decades that the world of work is changing...",
        "theory": theory_text,
        "findings": findings_text,
        "discussion": discussion_text,
    }

    report = validator.validate(paper_sections)

    print(report.format_report())

    # Assertions
    assert report.critical_count == 0, f"Should have no critical violations, got {report.critical_count}"
    assert report.structure_rating >= 4, f"Structure rating should be high, got {report.structure_rating}"
    assert report.is_properly_inductive, "Should be properly inductive"

    print("\n✅ Test passed: Recognized proper inductive structure\n")


if __name__ == "__main__":
    test_problematic_paper()
    print("\n" + "=" * 70 + "\n")
    test_properly_inductive_paper()
    print("\n✅ All tests passed!")
