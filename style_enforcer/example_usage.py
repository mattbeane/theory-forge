#!/usr/bin/env python3
"""
Example usage of the style enforcer.

This demonstrates how to use the style enforcer with different LLM backends.
"""

import os
from typing import Optional

# Import the style enforcer components
from validator import StyleValidator, validate_paragraph
from config import ManuscriptConfig, PaperType, QUANT_FORWARD_ORGSCI
from exemplars import ExemplarDB, get_section_prompt_with_exemplar
from orchestrator import ManuscriptOrchestrator


# =============================================================================
# Example 1: Validate existing text
# =============================================================================

def example_validate_text():
    """Demonstrate validation of existing text."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Validating existing text")
    print("="*60 + "\n")

    validator = StyleValidator()

    # Bad text with violations
    bad_text = """
    This paper makes three contributions. First, we extend the literature on
    worker responses to automation. Second, we show that anticipatory sensemaking
    mediates the relationship. Third, we document heterogeneity in response patterns.

    Our key findings include:
    - Voluntary turnover decreases as automation approaches
    - Workers engage in signaling behaviors
    - Seasonal workers show stronger effects

    The coefficient was significant (β = 0.21, p < 0.001).
    """

    result = validator.validate(bad_text)

    print(f"Is clean: {result.is_clean}")
    print(f"Hard violations: {result.hard_violation_count}")
    print(f"Soft violations: {result.soft_violation_count}")
    print()

    for v in result.violations:
        print(f"[{v.severity.value.upper()}] {v.type.value}")
        print(f"  Message: {v.message}")
        if v.location:
            print(f"  Location: {v.location}")
        if v.suggestion:
            print(f"  Suggestion: {v.suggestion}")
        print()


# =============================================================================
# Example 2: Get exemplars for a section
# =============================================================================

def example_get_exemplars():
    """Demonstrate getting exemplars for section writing."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Getting exemplars for sections")
    print("="*60 + "\n")

    db = ExemplarDB()

    # Get introduction exemplar
    intro_exemplar = db.get("introduction")
    print("INTRODUCTION EXEMPLAR:")
    print(f"Source: {intro_exemplar.source}")
    print(f"\nText preview:\n{intro_exemplar.text[:500]}...")
    print(f"\nNotes:\n{intro_exemplar.notes}")

    # Get contribution exemplar (critical for avoiding lists)
    print("\n" + "-"*40)
    contrib_exemplar = db.get("contribution")
    print("\nCONTRIBUTION EXEMPLAR (critical!):")
    print(f"\nNotes:\n{contrib_exemplar.notes}")


# =============================================================================
# Example 3: Build prompts with exemplars
# =============================================================================

def example_build_prompts():
    """Demonstrate building prompts with exemplars."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Building prompts with exemplars")
    print("="*60 + "\n")

    prompt_addition = get_section_prompt_with_exemplar("findings")
    print("PROMPT ADDITION FOR FINDINGS SECTION:")
    print(prompt_addition[:1000] + "...")


# =============================================================================
# Example 4: Full orchestration (requires LLM)
# =============================================================================

def example_full_orchestration(llm_call=None):
    """
    Demonstrate full manuscript orchestration.

    Args:
        llm_call: Function(system_prompt, user_prompt) -> response
                  If None, uses a mock for demonstration.
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Full orchestration")
    print("="*60 + "\n")

    if llm_call is None:
        print("No LLM provided. Using mock for demonstration.")
        print("In production, pass your LLM calling function.")
        print()

        def mock_llm(system: str, user: str) -> str:
            return """This research extends person-environment fit theory by identifying
work orientation as a moderator of the misfit-response relationship. Standard P-E fit
theory predicts that misfit leads to withdrawal: reduced effort, lower commitment, and
exit. This prediction has strong empirical support and captures an important dynamic.
But it is incomplete.

We show that when advancement pathways exist, career-oriented workers respond to misfit
by intensifying effort rather than withdrawing. Misfit creates motivation to change
one's situation; effort creates opportunities to change it. The standard P-E fit
prediction holds for job-oriented workers—they don't intensify effort because they
aren't seeking advancement. But for career-oriented workers, misfit can motivate.

The quantitative evidence supports this argument. Seasonal workers respond nearly twice
as strongly to incentive pay as full-time workers (β = 0.21 vs. β = 0.12, both p < 0.001).
This gap reveals that workers experiencing status misfit—stuck in contingent roles when
they desire permanent employment—intensify effort rather than withdraw. The qualitative
evidence illuminates why: managers described career-oriented workers as "the ones who
really care," visibly engaged from their first day."""

        llm_call = mock_llm

    # Create orchestrator
    orchestrator = ManuscriptOrchestrator(
        config=QUANT_FORWARD_ORGSCI,
        llm_call=llm_call,
        verbose=True,
    )

    # Generate a section
    result = orchestrator.generate_section(
        section_name="discussion",
        paper_plan={
            "main_contribution": "Work orientation moderates misfit-response relationship",
            "theoretical_extension": "Extends P-E fit theory",
            "practical_implications": "Recognize orientation heterogeneity in workforce",
        },
        evidence={
            "key_stats": "β = 0.21 vs 0.12, p < 0.001",
            "key_quote": "I can tell the people who really care. But then there's just like 85% of them that are just like, heh, okay.",
        },
    )

    print("\nGENERATED SECTION:")
    print("-"*40)
    print(result.content)
    print("-"*40)
    print(f"\nSuccess: {result.success}")
    print(f"Was fixed: {result.was_fixed}")

    # Get status
    print("\nORCHESTRATOR STATUS:")
    import json
    print(json.dumps(orchestrator.get_status(), indent=2))


# =============================================================================
# Example 5: Using with Claude API
# =============================================================================

def example_with_claude():
    """Example of using with the Anthropic Claude API."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Using with Claude API")
    print("="*60 + "\n")

    code = '''
import anthropic
from style_enforcer import ManuscriptOrchestrator, QUANT_FORWARD_ORGSCI

# Initialize Claude client
client = anthropic.Anthropic()

def claude_call(system_prompt: str, user_prompt: str) -> str:
    """Call Claude with system and user prompts."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return response.content[0].text

# Create orchestrator with Claude
orchestrator = ManuscriptOrchestrator(
    config=QUANT_FORWARD_ORGSCI,
    llm_call=claude_call,
)

# Generate manuscript
results = orchestrator.generate_manuscript(
    paper_plan=my_paper_plan,
    evidence=my_evidence,
)

# Assemble final manuscript
manuscript = "\\n\\n".join(
    results[section].content
    for section in ["abstract", "introduction", "theory", "methods", "findings", "discussion"]
)
'''
    print("Example code for using with Claude API:")
    print(code)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    # Run examples
    example_validate_text()
    example_get_exemplars()
    example_build_prompts()
    example_full_orchestration()
    example_with_claude()

    print("\n" + "="*60)
    print("Examples complete!")
    print("="*60)
