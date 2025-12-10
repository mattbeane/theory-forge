"""
Style Enforcer for Qualitative Management Papers

A system for enforcing stylistic standards on academic manuscripts targeting
top management journals (ASQ, Organization Science, Management Science).

This module implements a hybrid architecture:
- Section-controlled generation with exemplars
- Streaming paragraph-level validation
- Automatic fixing of style violations
- Data inventory for statistics verification
- Section-level sanity checks

Key components:
- StyleValidator: Deterministic rule checking (fast, no LLM)
- ExemplarDB: Reference paper excerpts for style guidance
- SectionConfig: Per-section rules and constraints
- ManuscriptOrchestrator: Controls section-by-section generation
- DataInventory: Scans available data files to prevent hallucination
- StatisticsValidator: Flags unverified statistical claims
- SectionSanityChecker: Section-level validation beyond style rules
"""

from .validator import StyleValidator, ValidationResult, ViolationType, Severity
from .exemplars import ExemplarDB
from .config import SectionConfig, ManuscriptConfig, PaperType, QUANT_FORWARD_ORGSCI
from .orchestrator import ManuscriptOrchestrator, GenerationResult
from .data_inventory import DataInventory, InventoryResult, scan_paper_data
from .statistics_validator import StatisticsValidator, StatisticalClaim
from .section_sanity import SectionSanityChecker, SanityReport

__all__ = [
    # Core
    'StyleValidator',
    'ValidationResult',
    'ViolationType',
    'Severity',
    'ExemplarDB',
    'SectionConfig',
    'ManuscriptConfig',
    'ManuscriptOrchestrator',
    'GenerationResult',
    # Config presets
    'PaperType',
    'QUANT_FORWARD_ORGSCI',
    # Data validation (new in v2)
    'DataInventory',
    'InventoryResult',
    'scan_paper_data',
    'StatisticsValidator',
    'StatisticalClaim',
    'SectionSanityChecker',
    'SanityReport',
]
