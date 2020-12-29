import numpy as np
import pandas as pd
from functools import reduce
import time

def part1(raw):
    start = int(raw[0].strip())
    services = [int(s) for s in raw[1].split(',') if s != 'x']
    print('\n\nPart 1:\n')
    print(f'Start: {start}, Services: {services}')

    times = dict()
    for service in services:
        ts = np.ceil(start / service) * service
        times[service] = ts

    print(f'Times: {times}')
    fastest_bus = reduce(lambda a, b: b if times[b] < times[a] else a, times)
    print(
        f'Fastest bus: {fastest_bus}, time: {times[fastest_bus]:.0f}, id = {fastest_bus * (times[fastest_bus] - start):.0f}')


def check_service(order, service, compare_order, check_val):
    """
    Checks whether service appears in the right place relative to compare_order

    Args:
        order (int): Where service was in original list
        service (int): Service number
        compare_order (int): Where service of comparison was in original list
        check_val (int): Value to see if service is near (i.e. 1000000, so check if service appears compare_order-order away from it)

    Returns:
        (bool): Whether it fits
    """
    diff = compare_order-order
    if (check_val-diff) % service == 0:
        return True
    return False


def find_earliest_consecutive(services_string, start_val=1, show_prints=True):
    services = [[i, int(s)] for i, s in enumerate(services_string.split(',')) if s != 'x']
    print(f'Services: {services}')

    services.sort(key=lambda x: x[1], reverse=True)
    print(f'Sorted Services: {services}')

    services = tuple(services)
    largest_order, largest_val = services[0]
    i = np.floor(start_val/largest_val)
    i = i if i > 0 else 1
    val = largest_val*i
    start_time = time.time()
    while True:
        bad = False
        add_next_val = largest_val
        for serv in services[1:]:
            if not check_service(*serv, largest_order, val):
                bad = True
                break
            else:
                add_next_val *= serv[1]
        if not bad:
            print(f'Start at {val - largest_order}')
            break
        elif show_prints:
            print(f'val = {val:4g}, add_next_val = {add_next_val:4g}, time_elapsed = {time.time()-start_time:.2f}s')
        val += add_next_val
    return val-largest_order


if __name__ == '__main__':
    # fp = 'Day13_Input_test.txt'
    fp = 'Day13_Input.txt'
    with open(fp, 'r') as f:
        raw = f.readlines()

    # Part 1
    part1(raw)

    # Part 2
    print('\n\nPart 2:\n')
    find_earliest_consecutive('17,x,13,19', show_prints=False)
    find_earliest_consecutive('67,7,59,61', show_prints=False)
    find_earliest_consecutive('67,x,7,59,61', show_prints=False)
    find_earliest_consecutive('67,7,x,59,61', show_prints=False)
    find_earliest_consecutive('1789,37,47,1889', show_prints=False)
    find_earliest_consecutive(raw[1], start_val=100000000000000, show_prints=False)




