"""
Audit Trail for Theory-Forge

Provides structured decision logging and Claude Code conversation linkage
for transparent, reviewable research methodology.
"""

from .tracker import (
    Decision,
    DecisionType,
    log_decision,
    get_decisions,
    get_decisions_by_stage,
    generate_decision_id,
)
from .reporter import (
    format_audit_trail,
    format_methods_appendix,
    format_decision_summary,
)
from .history import (
    find_claude_conversation,
    link_to_conversation,
    get_recent_conversations,
)

__all__ = [
    # Tracker
    "Decision",
    "DecisionType",
    "log_decision",
    "get_decisions",
    "get_decisions_by_stage",
    "generate_decision_id",
    # Reporter
    "format_audit_trail",
    "format_methods_appendix",
    "format_decision_summary",
    # History linkage
    "find_claude_conversation",
    "link_to_conversation",
    "get_recent_conversations",
]
