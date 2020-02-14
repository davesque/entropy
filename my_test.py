from decimal import Decimal as D
from fractions import Fraction as F
from math import log2
from typing import (
    Iterator,
    List,
    Tuple,
    TypeVar,
)
import functools
import operator

from entropy.huffman import get_code_book, Node


def H(P):
    return -sum(p * log2(p) for p in P)


T = TypeVar("T")


def sequences(alphabet: List[T], n: int) -> List[List[T]]:
    c: List[List[T]] = [[]]
    for _ in range(n):
        c = [[x] + y for x in alphabet for y in c]
    return c


def prod(X):
    return functools.reduce(operator.mul, X, 1)


def get_path_lengths(node: Node[str], depth: int = 0) -> Iterator[Tuple[str, int]]:
    if node.left is None and node.right is None:
        yield (node.val, depth)

    if node.left is not None:
        yield from get_path_lengths(node.left, depth + 1)
    if node.right is not None:
        yield from get_path_lengths(node.right, depth + 1)


def f_to_d(x: F) -> D:
    return D(x.numerator) / D(x.denominator)


letter_freqs = {
    "a": F(2, 3),
    "b": F(1, 3),
}
n = 12
words = sequences(list(letter_freqs.keys()), n)
word_freqs = {"".join(w): prod(letter_freqs[l] for l in w) for w in words}
word_distribution = [(f, w) for w, f in word_freqs.items()]

code_book = get_code_book(word_distribution)
path_lengths = list(get_path_lengths(code_book))

actual_entropy = f_to_d(sum([word_freqs[word] * path_len for word, path_len in path_lengths])) / n
expected_entropy = H(word_freqs[word] for word, _ in path_lengths) / n

print("\n", repr(actual_entropy))
print("\n", repr(expected_entropy))
print("\n", H([F(2, 3), F(1, 3)]))
