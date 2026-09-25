"""Historical reads of the frozen POST-TUE-UPP-001 queue checkpoint.

The UPP workstream checkers were written while the queue was live and asserted its tip
(`next_action`, `ordered_followups`). After the terminal migration the legacy fields stay
frozen at the last workstream and `terminal_*` fields are authoritative once
`status == "complete"` (see the checkpoint's `compatibility_note`). These helpers let each
historical checker verify its own workstream against the queue *history* instead of the tip.
"""
from __future__ import annotations

FIRST_PR = 281


def completed_by_pr(queue: dict) -> dict[int, dict]:
    return {item.get("target_pr"): item for item in queue.get("completed_workstreams", [])}


def history_contiguous(queue: dict) -> bool:
    """Completed PRs run without gaps from the registration PR, and pending followups come after them."""
    prs = [item.get("target_pr") for item in queue.get("completed_workstreams", [])]
    if not prs or prs != list(range(FIRST_PR, FIRST_PR + len(prs))):
        return False
    return all(isinstance(pr, int) and pr > prs[-1] for pr in queue.get("ordered_followups", []))


def successor_recorded(queue: dict, target_pr: int, workstream: str) -> bool:
    """The queue advanced to `workstream` at `target_pr`: it is completed there or is the live next action."""
    completed = completed_by_pr(queue)
    if target_pr in completed:
        return completed[target_pr].get("workstream") == workstream
    return queue.get("next_action") == {"target_pr": target_pr, "workstream": workstream}


def _terminal(queue: dict, field: str):
    terminal_field = f"terminal_{field}"
    if queue.get("status") == "complete" and terminal_field in queue:
        return queue[terminal_field]
    return queue.get(field)


def terminally_closed(queue: dict) -> bool:
    return (
        queue.get("status") == "complete"
        and _terminal(queue, "next_action") is None
        and _terminal(queue, "ordered_followups") == []
    )


def public_evaluation_authorized(queue: dict):
    return _terminal(queue, "public_evaluation_authorized")
