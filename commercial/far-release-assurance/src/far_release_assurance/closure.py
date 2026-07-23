"""Deterministic finite machinery-closure traversal."""

from __future__ import annotations

from collections import Counter, deque

from .model import ClosureResult, ClosureStatus, MachineryItem


def assess_closure(items: tuple[MachineryItem, ...], roots: tuple[str, ...]) -> ClosureResult:
    """Assess transitively required machinery from canonical roots.

    Duplicate identities are defects and are never silently merged. The first item
    is used only to allow deterministic traversal while the duplicate remains an
    explicit opening defect.
    """

    counts = Counter(item.machinery_id for item in items)
    duplicates = tuple(sorted(key for key, count in counts.items() if count > 1))

    index: dict[str, MachineryItem] = {}
    for item in items:
        index.setdefault(item.machinery_id, item)

    queue = deque(sorted(set(roots)))
    visited: set[str] = set()
    unresolved: set[str] = set()
    defects: set[str] = set(duplicates)
    undeclared_roots: set[str] = set()

    root_set = set(roots)
    while queue:
        machinery_id = queue.popleft()
        if machinery_id in visited:
            continue
        visited.add(machinery_id)

        item = index.get(machinery_id)
        if item is None:
            defects.add(machinery_id)
            if machinery_id in root_set:
                undeclared_roots.add(machinery_id)
            continue

        if item.opening_defect():
            defects.add(machinery_id)
        elif item.unresolved():
            unresolved.add(machinery_id)

        for dependency in sorted(set(item.required_dependencies)):
            if dependency not in visited:
                queue.append(dependency)

    if defects:
        status = ClosureStatus.OPEN
    elif unresolved:
        status = ClosureStatus.UNKNOWN
    else:
        status = ClosureStatus.CLOSED

    return ClosureResult(
        status=status,
        reached=tuple(sorted(visited)),
        unresolved=tuple(sorted(unresolved)),
        defects=tuple(sorted(defects)),
        duplicates=duplicates,
        undeclared_roots=tuple(sorted(undeclared_roots)),
    )
