import numpy as np
from typing import Set, List, Tuple, Dict, Union
import pandas as pd
from dataclasses import dataclass, field
from itertools import product
from functools import lru_cache


@dataclass
class Constellation:
    filepath: str = field(repr=False)

    state: np.ndarray = field(init=False)

    def __post_init__(self):
        self.state = self._get_initial_state(self.filepath)
        self.iteration = 0

    def _get_initial_state(self, fp: str):
        with open(fp, 'r') as f:
            raw = f.readlines()
        initial_state = np.array([[1 if c == '#' else 0 for c in l.strip()] for l in raw], ndmin=3,
                                 dtype=int)
        return initial_state

    def extend_dims(self):
        self.state = np.pad(self.state, pad_width=1)

    def cube_active(self, x, y, z):
        blob_coords = get_blob_coords(x, y, z)
        s = 0
        for coord in blob_coords:
            try:
                if np.all(coord >= 0):
                    s += self.state[tuple(coord)]
            except IndexError:
                pass  # Same as add 0

        print(f'x, y, z: {(x, y, z)}, current_state: {self.state[z, y, x]} sum: {s}')
        cs = self.state[z, y, x]
        if cs == 1 and (s == 2 or s == 3):
            return True
        elif cs == 0 and s == 3:
            return True
        return False

    def iterate(self):
        self.iteration += 1
        coords = np.ndindex(self.state.shape)
        new_array = np.zeros(self.state.shape).astype(int)
        for coord in coords:
            new_array[tuple(coord)] = self.cube_active(x=coord[-1], y=coord[-2], z=coord[-3])
        self.state = new_array
        self.extend_dims()

    def run_iterations(self, iterations):
        for i in range(iterations):
            self.iterate()
        return self.state

    def print(self):
        p_arr = np.array([[['#' if v == 1 else '.' for v in row] for row in plane] for plane in self.state])
        print(p_arr)


@lru_cache(maxsize=1000)
def get_blob_coords(x, y, z):
    return (np.array(coord)+(z, y, x) for coord in set(product(*[[-1, 0, 1]] * 3)) - {(0, 0, 0)})


if __name__ == '__main__':
    filepath = 'Day17_Input.txt'
    test_fp = 'Day17_Input_test.txt'

    fp = test_fp

    constellation = Constellation(fp)
    constellation.run_iterations(6)
    print(np.sum(constellation.state))



