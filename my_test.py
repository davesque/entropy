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
import shutil
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


ALIGN_SPECIFIERS = {
    "left": "<",
    "right": ">",
    "center": "^",
}


def get_term_width() -> int:
    return shutil.get_terminal_size((80, 20)).columns


def align_str(inp: str, filler_char: str = " ", align: str = "right") -> str:
    term_width = get_term_width()

    align_specifier = ALIGN_SPECIFIERS[align]
    format_str = "{:" + filler_char + align_specifier + str(term_width) + "}"

    return format_str.format(inp)


def print_header(inp: str, filler_char: str = " ", align: str = "right") -> None:
    print(align_str(inp, filler_char=filler_char, align=align))


def print_stat(name: str, value: str) -> None:
    term_width = get_term_width()

    if term_width % 2 == 1:
        val_width = term_width // 2 + 1
    else:
        val_width = term_width // 2
    name_width = term_width // 2

    format_str = "{:.<" + str(name_width) + "}{:.>" + str(val_width) + "}"

    print(format_str.format(name, value))


letter_freqs = {
    "a": 2 / 3,
    "b": 1 / 3,
}


for n in range(12, 15):
    print("")
    print_header(f"=== WORD LENGTH: {n} ===", align="left", filler_char="=")
    with timeit(
        lambda t: print_header(f"=== elapsed time: {t} seconds ===", align="right", filler_char="=")
    ):
        with timeit(lambda t: print_stat("words time ", f" {t} seconds")):
            words = sequences(list(letter_freqs.keys()), n)

        with timeit(lambda t: print_stat("lookups time ", f" {t} seconds")):
            word_freqs = {"".join(w): prod(letter_freqs[l] for l in w) for w in words}
            word_distribution = [(f, w) for w, f in word_freqs.items()]

        with timeit(lambda t: print_stat("code book time ", f" {t} seconds")):
            code_book = get_code_book(word_distribution)

        with timeit(lambda t: print_stat("avg. path length time ", f" {t} seconds")):
            avg_path_len = (
                force_float(
                    sum(
                        word_freqs[word] * path_len
                        for word, path_len in get_path_lengths(code_book)
                    )
                )
                / n  # noqa
            )

        derivative_entropy = H(word_freqs.values()) / n
        base_entropy = H(letter_freqs.values())

        print_header("-- totals: --", align="center", filler_char="-")

        print_stat("avg. path length ", f" {avg_path_len}")
        print_stat("derivative alphabet entropy ", f" {derivative_entropy}")
        print_stat("base alphabet entropy ", f" {base_entropy}")
