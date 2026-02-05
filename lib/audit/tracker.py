"""
Decision tracking for audit trail.

Logs structured decisions to state.json for transparent methodology.
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class DecisionType(Enum):
    """Types of decisions that can be logged."""

    # Pattern hunting
    PATTERN_SELECTED = "pattern_selected"
    PATTERN_REJECTED = "pattern_rejected"
    ROBUSTNESS_CHECK = "robustness_check"

    # Theory selection
    THEORY_SELECTED = "theory_selected"
    LENS_SELECTED = "lens_selected"

    # Qualitative
    MECHANISM_IDENTIFIED = "mechanism_identified"
    QUOTE_SELECTED = "quote_selected"
    DISCONFIRMING_NOTED = "disconfirming_noted"

    # Framing
    FRAME_GENERATED = "frame_generated"
    FRAME_SELECTED = "frame_selected"
    FRAME_REJECTED = "frame_rejected"

    # Claims
    CLAIM_VERIFIED = "claim_verified"
    CLAIM_FLAGGED = "claim_flagged"

    # General
    GATE_PASSED = "gate_passed"
    GATE_FAILED = "gate_failed"
    USER_OVERRIDE = "user_override"
    PARAMETER_SET = "parameter_set"


@dataclass
class Decision:
    """A structured decision record."""

    id: str
    timestamp: str
    stage: str  # e.g., "hunt_patterns", "mine_qual", "smith_frames"
    decision_type: DecisionType
    action: str  # "accepted", "rejected", "flagged", "selected"

    # What was decided about
    entity_type: str  # "pattern", "quote", "frame", "claim", "theory"
    entity_id: str  # Identifier for the entity
    entity_label: str  # Human-readable name

    # Reasoning
    description: str
    reasoning: str

    # Alternatives
    alternatives_considered: List[str] = field(default_factory=list)

    # Evidence
    supporting_evidence: List[str] = field(default_factory=list)
    challenging_evidence: List[str] = field(default_factory=list)

    # Confidence
    confidence: str = "medium"  # high, medium, low

    # Claude Code linkage
    claude_turn_id: Optional[str] = None
    claude_conversation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSON storage."""
        d = asdict(self)
        d["decision_type"] = self.decision_type.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Decision":
        """Deserialize from JSON."""
        data = data.copy()
        data["decision_type"] = DecisionType(data["decision_type"])
        return cls(**data)


def generate_decision_id() -> str:
    """Generate a unique decision ID."""
    return f"DEC-{uuid.uuid4().hex[:8].upper()}"


def log_decision(
    state_path: Path,
    stage: str,
    decision_type: DecisionType,
    action: str,
    entity_type: str,
    entity_id: str,
    entity_label: str,
    description: str,
    reasoning: str,
    alternatives: List[str] = None,
    supporting: List[str] = None,
    challenging: List[str] = None,
    confidence: str = "medium",
    claude_turn_id: str = None,
) -> Decision:
    """
    Log a decision to state.json.

    Args:
        state_path: Path to state.json
        stage: Pipeline stage (e.g., "hunt_patterns")
        decision_type: Type of decision
        action: What was done ("accepted", "rejected", etc.)
        entity_type: Type of entity ("pattern", "quote", etc.)
        entity_id: Unique identifier
        entity_label: Human-readable name
        description: What was decided
        reasoning: Why it was decided
        alternatives: Other options considered
        supporting: Evidence supporting the decision
        challenging: Evidence against the decision
        confidence: Confidence level
        claude_turn_id: Optional link to CC conversation turn

    Returns:
        The logged Decision object
    """
    # Load current state
    if state_path.exists():
        with open(state_path) as f:
            state = json.load(f)
    else:
        state = {}

    # Ensure decisions array exists
    if "decisions" not in state:
        state["decisions"] = []

    # Create decision
    decision = Decision(
        id=generate_decision_id(),
        timestamp=datetime.now().isoformat(),
        stage=stage,
        decision_type=decision_type,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        entity_label=entity_label,
        description=description,
        reasoning=reasoning,
        alternatives_considered=alternatives or [],
        supporting_evidence=supporting or [],
        challenging_evidence=challenging or [],
        confidence=confidence,
        claude_turn_id=claude_turn_id,
    )

    # Append to state
    state["decisions"].append(decision.to_dict())
    state["updated_at"] = datetime.now().isoformat()

    # Write back
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

    return decision


def get_decisions(state_path: Path) -> List[Decision]:
    """Get all decisions from state.json."""
    if not state_path.exists():
        return []

    with open(state_path) as f:
        state = json.load(f)

    decisions_data = state.get("decisions", [])
    return [Decision.from_dict(d) for d in decisions_data]


def get_decisions_by_stage(state_path: Path, stage: str) -> List[Decision]:
    """Get decisions filtered by pipeline stage."""
    all_decisions = get_decisions(state_path)
    return [d for d in all_decisions if d.stage == stage]


def get_decisions_by_type(state_path: Path, decision_type: DecisionType) -> List[Decision]:
    """Get decisions filtered by type."""
    all_decisions = get_decisions(state_path)
    return [d for d in all_decisions if d.decision_type == decision_type]
