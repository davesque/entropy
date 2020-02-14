from typing import (
    Any,
    Generic,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

K = TypeVar("K")
V = TypeVar("V")


class Node(Generic[K, V]):
    __slots__ = ["key", "val"]

    def __init__(self, key: K, val: V):
        self.key = key
        self.val = val

    def __lt__(self, other: Any) -> bool:
        assert isinstance(other, (type(self), Infinity))
        return self.key < other.key  # type: ignore

    def __repr__(self) -> str:
        return f"<Node ({self.key}, {self.val})>"


class Infinity:
    @property
    def key(self):
        return self

    def __lt__(self, _other: Any) -> bool:
        return False

    def __gt__(self, _other: Any) -> bool:
        return True


infinity = Infinity()


class MinHeap(Generic[K, V]):
    __slots__ = ["lst"]

    def __init__(self):
        self.lst: List[Node[K, V]] = []

    def insert(self, key: K, val: V) -> None:
        self.lst.append(Node(key, val))

        i: Optional[int] = len(self.lst) - 1
        while i is not None:
            i = self.bubble_up(i)

    def remove(self) -> Tuple[K, V]:
        last = self.lst.pop()
        if len(self.lst) == 0:
            return last.key, last.val

        root = self.lst[0]
        self.lst[0] = last

        i: Optional[int] = 0
        while i is not None:
            i = self.trickle_down(i)

        return root.key, root.val

    def bubble_up(self, i: int) -> Optional[int]:
        if i == 0:
            return None

        parent_i = (i - 1) // 2

        curr, parent = self.lst[i], self.lst[parent_i]
        if curr < parent:
            self.lst[parent_i], self.lst[i] = curr, parent
            return parent_i

        return None

    def trickle_down(self, i: int) -> Optional[int]:
        left_i = 2 * i + 1
        right_i = left_i + 1

        curr = self.lst[i]
        left: Union[Node[K, V], Infinity]
        right: Union[Node[K, V], Infinity]
        try:
            left = self.lst[left_i]
        except IndexError:
            left = infinity
        try:
            right = self.lst[right_i]
        except IndexError:
            right = infinity

        if left < right:
            el_to_compare = left
            el_to_compare_i = left_i
        else:
            el_to_compare = right
            el_to_compare_i = right_i

        if el_to_compare < curr:
            assert isinstance(el_to_compare, Node)
            self.lst[el_to_compare_i], self.lst[i] = curr, el_to_compare
            return el_to_compare_i

        return None

    def __len__(self) -> int:
        return len(self.lst)
