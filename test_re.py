import pytest
from pytest_benchmark.fixture import BenchmarkFixture
from typing import List, Tuple

from find_re import find_re

'''
    =======================================================
    |   Searching substring Python Regular Expressions    |
    =======================================================
    Runtime: ~ 0:01:50 [s]
    To runtest type: pytest ./test_re.py
    To run tests and save data to json type: pytest ./test_re.py --benchmark-save test_re
'''

@pytest.fixture(scope="session")
def pan_tadeusz():
    with open("files/pan-tadeusz.txt", mode="r", encoding="utf-8") as f:
        txt = f.read()

    words = txt.split(maxsplit=max(BENCHMARK_SIZES))[:-1]
    return txt, words

BENCHMARK_ROUNDS = 2
BENCHMARK_SIZES = list(range(100, 1001, 100))

@pytest.mark.parametrize("size", BENCHMARK_SIZES)
def test_re(size: int, benchmark: BenchmarkFixture, pan_tadeusz: Tuple[str, List[str]]):

    benchmark.extra_info["size"] = size

    list_of_words = pan_tadeusz[1][:size]
    text = pan_tadeusz[0]

    def f():
        results = {}
        for word in list_of_words:
            indecies = find_re(word, text)
            results[word] = indecies

    result = benchmark.pedantic(f, rounds=BENCHMARK_ROUNDS)