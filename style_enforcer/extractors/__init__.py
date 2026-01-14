"""
Extractors for cross-section coherence validation.

This module contains LLM-based extractors that analyze paper sections
to extract semantic content for cross-section validation.
"""

from .contribution_extractor import ContributionExtractor, ExtractedContribution
from .theory_analyzer import TheoryAnalyzer, TheoryAnalysis, PreannouncementEvidence

__all__ = [
    "ContributionExtractor",
    "ExtractedContribution",
    "TheoryAnalyzer",
    "TheoryAnalysis",
    "PreannouncementEvidence",
]
