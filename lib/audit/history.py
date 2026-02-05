"""
Claude Code history integration.

Links audit trail decisions to Claude Code conversation history
for full traceability.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def get_history_path() -> Path:
    """Get the path to Claude Code history."""
    return Path.home() / ".claude" / "history.jsonl"


def get_recent_conversations(
    limit: int = 10,
    project_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Get recent Claude Code conversations.

    Args:
        limit: Maximum number of conversations to return
        project_filter: Optional project name to filter by

    Returns:
        List of conversation summaries
    """
    history_path = get_history_path()
    if not history_path.exists():
        return []

    conversations = []

    with open(history_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if project_filter:
                    # Filter by project if specified
                    project = entry.get("project", "")
                    if project_filter.lower() not in project.lower():
                        continue

                conversations.append({
                    "id": entry.get("id"),
                    "timestamp": entry.get("timestamp"),
                    "project": entry.get("project"),
                    "summary": entry.get("summary", "")[:100],
                    "messages_count": len(entry.get("messages", [])),
                })
            except json.JSONDecodeError:
                continue

    # Sort by timestamp descending, take most recent
    conversations.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return conversations[:limit]


def find_claude_conversation(
    decision_timestamp: str,
    window_minutes: int = 5,
) -> Optional[str]:
    """
    Find the Claude Code conversation that was active when a decision was made.

    Args:
        decision_timestamp: ISO timestamp of the decision
        window_minutes: Time window to search (±minutes)

    Returns:
        Conversation ID if found, None otherwise
    """
    history_path = get_history_path()
    if not history_path.exists():
        return None

    try:
        decision_time = datetime.fromisoformat(decision_timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None

    window = timedelta(minutes=window_minutes)
    best_match = None
    best_delta = timedelta.max

    with open(history_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                entry_time_str = entry.get("timestamp")
                if not entry_time_str:
                    continue

                entry_time = datetime.fromisoformat(
                    entry_time_str.replace("Z", "+00:00")
                )
                delta = abs(entry_time - decision_time)

                if delta <= window and delta < best_delta:
                    best_match = entry.get("id")
                    best_delta = delta

            except (json.JSONDecodeError, ValueError):
                continue

    return best_match


def link_to_conversation(
    state_path: Path,
    decision_id: str,
    conversation_id: str,
) -> bool:
    """
    Link a decision to a Claude Code conversation.

    Args:
        state_path: Path to state.json
        decision_id: ID of the decision to link
        conversation_id: Claude Code conversation ID

    Returns:
        True if linked successfully
    """
    if not state_path.exists():
        return False

    with open(state_path, "r") as f:
        state = json.load(f)

    decisions = state.get("decisions", [])
    for d in decisions:
        if d.get("id") == decision_id:
            d["claude_conversation_id"] = conversation_id
            break
    else:
        return False

    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

    return True


def auto_link_decisions(
    state_path: Path,
    window_minutes: int = 5,
) -> int:
    """
    Automatically link all unlinked decisions to conversations.

    Args:
        state_path: Path to state.json
        window_minutes: Time window for matching

    Returns:
        Number of decisions linked
    """
    if not state_path.exists():
        return 0

    with open(state_path, "r") as f:
        state = json.load(f)

    linked_count = 0
    decisions = state.get("decisions", [])

    for d in decisions:
        if d.get("claude_conversation_id"):
            continue  # Already linked

        timestamp = d.get("timestamp")
        if not timestamp:
            continue

        conversation_id = find_claude_conversation(timestamp, window_minutes)
        if conversation_id:
            d["claude_conversation_id"] = conversation_id
            linked_count += 1

    if linked_count > 0:
        state["updated_at"] = datetime.now().isoformat()
        with open(state_path, "w") as f:
            json.dump(state, f, indent=2)

    return linked_count


def get_conversation_context(
    conversation_id: str,
    max_messages: int = 10,
) -> List[Dict[str, str]]:
    """
    Get message context from a Claude Code conversation.

    Args:
        conversation_id: The conversation ID to retrieve
        max_messages: Maximum messages to return

    Returns:
        List of message dicts with 'role' and 'content'
    """
    history_path = get_history_path()
    if not history_path.exists():
        return []

    with open(history_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if entry.get("id") == conversation_id:
                    messages = entry.get("messages", [])
                    # Return last N messages
                    return [
                        {"role": m.get("role"), "content": m.get("content", "")[:500]}
                        for m in messages[-max_messages:]
                    ]
            except json.JSONDecodeError:
                continue

    return []
