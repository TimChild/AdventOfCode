import numpy as np
import pandas as pd
from itertools import product, chain
from functools import lru_cache
from multiprocessing import Pool


@lru_cache
def gen_data():
    with open('Day11_input.txt') as f:
    # with open('Day11_input_test.txt') as f:
        raw = f.readlines()
    data = np.array([[char for char in row.strip()] for row in raw])
    indexs = np.where(data)
    return data, indexs


# @lru_cache
def coords_to_check(y, x, data):
    check_coords = [(y - 1, x), (y + 1, x), (y, x + 1), (y, x - 1), (y + 1, x + 1), (y + 1, x - 1), (y - 1, x + 1),
                    (y - 1, x - 1)]
    check_coords = [(y, x) for y, x in check_coords if
                    (0 <= y <= data.shape[0] - 1) and (0 <= x <= data.shape[1] - 1)]
    check_coords = np.array(check_coords)
    return check_coords


def empty(y, x, data):
    if data[y, x] in ['.', '#']:
        return False
    surrounding_coords = coords_to_check(y, x, data)
    if all([p in ['.', 'L'] for p, coords in zip(data[tuple(surrounding_coords.T)], surrounding_coords)]):
        return True
    return False


def full(y, x, data):
    if data[y, x] in ['.', 'L']:
        return False
    surrounding_coords = coords_to_check(y, x, data)
    if np.sum(data[tuple(surrounding_coords.T)] == '#') >= 4:
        return True
    return False


def iter_seats(data, indexs, async_mode=False):
    if async_mode:
        empties, fulls = _async_iter_seats(data, indexs)
    else:
        empties, fulls = _iter_seats(data, indexs)
    changed = False
    if np.any(empties) or np.any(fulls):
        changed = True
        data[np.where(empties)] = '#'
        data[np.where(fulls)] = 'L'
    return data, changed


def _iter_seats(data, indexs):
    args = (indexs[0], indexs[1], [data]*len(indexs[0]))
    empties = np.array(list(map(empty, *args))).reshape(data.shape)
    fulls = np.array(list(map(full, *args))).reshape(data.shape)
    return empties, fulls


CS = 1


def _async_iter_seats(data, indexs):
    with Pool(processes=6) as pool:
        indexs = np.array(indexs).T
        args = [(*coords, data) for coords in indexs]
        empties_future = pool.starmap_async(empty, args, chunksize=CS)
        fulls_future = pool.starmap_async(full, args, chunksize=CS)
        empties_future.wait()
        fulls_future.wait()
    empties = np.array(empties_future.get()).reshape(data.shape)
    fulls = np.array(fulls_future.get()).reshape(data.shape)
    return empties, fulls


def iter_till_finished(data, indexs):
    while True:
        data, changed = iter_seats(data, indexs, async_mode=False)
        if changed is False:
            break
    return data


def test(a, b):
    print(a*2, b)
    return a*3*b


if __name__ == '__main__':
    data, indexs = gen_data()
    print(_iter_seats(data, indexs))
    print(_async_iter_seats(data, indexs))
