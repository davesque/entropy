from contextlib import contextmanager
from decimal import Decimal
from fractions import Fraction
from math import log2
from typing import (
    Iterator,
    List,
    Tuple,
    TypeVar,
    Union,
)
import functools
import operator
import time

from entropy.huffman import get_code_book, Node


def H(P):
    return -sum(p * log2(p) for p in P)


T = TypeVar("T")


@contextmanager
def timeit(display):
    start = time.time()
    yield
    end = time.time()
    display(end - start)


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


def force_float(x: Union[Fraction, int, float, Decimal]) -> float:
    if isinstance(x, Fraction):
        return x.numerator / x.denominator
    else:
        return float(x)


letter_freqs = {
    "a": 2 / 3,
    "b": 1 / 3,
}


for n in range(2, 25):
    print(f"~~~~~~~~~~~~~~~~ word length: {n}")
    with timeit(lambda t: print(f"~~~~~~~~~~~~~~~~ elapsed time: {t} seconds\n")):
        words = sequences(list(letter_freqs.keys()), n)

        word_freqs = {"".join(w): prod(letter_freqs[l] for l in w) for w in words}
        word_distribution = [(f, w) for w, f in word_freqs.items()]

        code_book = get_code_book(word_distribution)
        path_lengths = list(get_path_lengths(code_book))

        avg_path_len = (
            force_float(sum([word_freqs[word] * path_len for word, path_len in path_lengths])) / n
        )

        print(" Avg. path length:            ", avg_path_len)
        print(" Derivative alphabet entropy: ", H(word_freqs.values()) / n)
        print(" Base alphabet entropy:       ", H(letter_freqs.values()))
