from __future__ import annotations

from typing import (
    Generic,
    List,
    Tuple,
    TypeVar,
)

from entropy.min_heap import MinHeap

K = TypeVar("K")
V = TypeVar("V")

Distribution = List[Tuple[K, V]]


def indent(inp: str, indent: str) -> str:
    return "\n".join([indent + l for l in inp.splitlines()])


class Node(Generic[V]):
    __slots__ = ["val", "left", "right"]

    def __init__(self, val: V, left: Node[V] = None, right: Node[V] = None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        if self.left is None and self.right is None:
            return f"Node({self.val})"

        left_repr = indent(repr(self.left), "   |")
        right_repr = indent(repr(self.right), "   |")

        return f"""
Node({self.val}):
{left_repr}
{right_repr}
"""[
            1:-1
        ]


def get_code_book(dist: Distribution[K, V]) -> Node[V]:
    assert len(dist) > 0
    assert sum(p for p, _ in dist) == 1

    heap = MinHeap()
    for p, i in dist:
        heap.insert(p, Node(i))

    while True:
        if len(heap) == 1:
            return heap.remove()[1]

        p1, left = heap.remove()
        p2, right = heap.remove()

        heap.insert(p1 + p2, Node(None, left, right))
