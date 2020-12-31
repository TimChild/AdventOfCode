import numpy as np
from typing import Set, List, Tuple, Dict, Union
import pandas as pd
from functools import reduce
from dataclasses import dataclass, field
from itertools import product
import timeit

@dataclass
class Constellation:
    filepath: str = field(repr=False)
    ndim: int = 3

    state: np.ndarray = field(init=False)

    def __post_init__(self):
        self.state = self._get_initial_state(self.filepath)
        self.iteration = 0
        self._slices = None

    def _get_initial_state(self, fp: str):
        with open(fp, 'r') as f:
            raw = f.readlines()
        initial_state = np.array([[1 if c == '#' else 0 for c in l.strip()] for l in raw], ndmin=self.ndim,
                                 dtype=int)
        return initial_state

    def extend_dims(self):
        self.state = np.pad(self.state, pad_width=1)

    @property
    def slices(self):
        if not self._slices:
            self._slices = get_slices(ndim=self.ndim)
        return self._slices

    def iterate(self):
        self.extend_dims()
        temp = np.pad(self.state, pad_width=1)
        arr_gen = (temp[s] for s in self.slices)

        if self.ndim <= 5:  # Faster, but uses too much memory for dim = 6 (took 1.4s d=5, d=6 wasn't finishing)
            sums = np.sum(np.array([temp[s] for s in self.slices]), axis=0)
        else:  # using reduce so that higher dimensions can be done for fun of it (slower for low dim)
            # (took 1m45s d=6, 2.7s d=5)
            sums = reduce(lambda a, b: np.sum(np.array([a, b]), axis=0), arr_gen)

        actives = np.where(
            np.logical_or(
                np.logical_and(
                    self.state == 1,
                    np.logical_or(sums == 2, sums == 3)),
                np.logical_and(
                    self.state == 0,
                    sums == 3
                )
            )
        )
        self.state = np.zeros(self.state.shape)
        self.state[actives] = 1

    def run_iterations(self, iterations):
        for i in range(iterations):
            self.iterate()
        return self.state


def get_slices(ndim=3):
    return tuple(
        s for s in product(*[[np.s_[:-2], np.s_[1:-1], np.s_[2:]]] * ndim) if
        s != tuple([np.s_[1:-1]]*ndim))


# @lru_cache(maxsize=1000)
# def get_blob_coords(x, y, z):
#     return (np.array(coord)+(z, y, x) for coord in set(product(*[[-1, 0, 1]] * 3)) - {(0, 0, 0)})


if __name__ == '__main__':
    filepath = 'Day17_Input.txt'
    test_fp = 'Day17_Input_test.txt'

    fp = filepath

    # Part 1
    constellation = Constellation(fp, ndim=3)
    constellation.run_iterations(6)
    print(f'\n\nPart1: Sum = {np.sum(constellation.state)}\n\n')

    # Part2
    constellation = Constellation(fp, ndim=4)
    constellation.run_iterations(6)
    print(f'\n\nPart2: Sum = {np.sum(constellation.state)}\n\n')

    # Speed testing
    test_const = Constellation(fp, ndim=6)
    init_state = test_const.state

    def timeit_test(constel, start_state):
        constel.state = start_state
        constel.run_iterations(6)

    print(f'Ready to run speed test. Just run: \n%timeit timeit_test(test_const, init_state)\n')

