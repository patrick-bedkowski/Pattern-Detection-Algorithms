import pytest
from pytest_benchmark.fixture import BenchmarkFixture
from typing import Callable, Iterator, List, Sequence, Tuple

from find_n import find_n
from file_management import read_txt_file, list_2_str

# https://gitlab-stud.elka.pw.edu.pl/mkuranow/aisdi-wysocka-kuranowski/-/blob/master/05-substring/substring.py

'''
    ====================================================
    |       Searching substring Naive algorithm        |
    ====================================================

    Runtime: ~ 0:15:00 [s]
    To runtest type: pytest ./test_n.py
    To run tests and save data to json type: pytest ./test_n.py --benchmark-save benchmarks\test_n
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
def test_n(size: int, benchmark: BenchmarkFixture, pan_tadeusz: Tuple[str, List[str]]):

    benchmark.extra_info["size"] = size

    list_of_words = pan_tadeusz[1][:size]
    text = pan_tadeusz[0]

    def f():
        results = {}
        for word in list_of_words:
            indecies = find_n(word, text)
            results[word] = indecies

    result = benchmark.pedantic(f, rounds=BENCHMARK_ROUNDS, iterations=1)