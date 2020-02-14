from hypothesis import (
    given,
    settings,
    strategies as st,
)

from entropy.min_heap import MinHeap


@settings(max_examples=500)
@given(st.lists(st.tuples(st.integers(), st.integers())))
def test_min_heap(lst):
    heap = MinHeap()

    for k, v in lst:
        heap.insert(k, v)
    actual = []
    while True:
        try:
            actual.append(heap.remove())
        except IndexError:
            break

    expected = sorted(lst, key=lambda i: i[0])
    if len(actual) == 0 and len(expected) == 0:
        return

    actual_keys, actual_vals = zip(*actual)
    expected_keys, expected_vals = zip(*expected)

    assert actual_keys == expected_keys
    assert set(actual_vals) == set(expected_vals)
