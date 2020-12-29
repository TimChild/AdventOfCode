import numpy as np
from itertools import product
import re

class Program:
    def __init__(self):
        self.mask = ''
        self.memory = {}

    def update_mask(self, new_mask):
        assert(len(new_mask) == 36)
        self.mask = new_mask

    def update_memory(self, mem_num, input):
        mem_num, input = int(mem_num), int(input)
        converted = self._apply_mask(input)
        self.memory[mem_num] = converted

    def _apply_mask(self, num: int):
        bin_num = bin(num)[2:].zfill(36)
        new_bin = ''.join([a if b == 'X' else b for a, b in zip(bin_num, self.mask)])
        new_num = int(new_bin, 2)
        return new_num

    def do_operation(self, line_string):
        if line_string[0:4] == 'mask':
            self.update_mask(line_string[-36:])
        elif line_string[0:3] == 'mem':
            self.update_memory(re.search('(?<=\[)\d+(?=])', line_string)[0], re.search('\d+$', line_string)[0])
        else:
            raise ValueError


class Program2(Program):

    def update_memory(self, mem_num, input):
        mem_num, input = [int(num) for num in (mem_num, input)]
        mem_nums = self._apply_mask(mem_num)
        for num in mem_nums:
            self.memory[num] = input

    def _apply_mask(self, num: int):
        bin_num = bin(num)[2:].zfill(36)
        masked_num = [a if b == '0' else b for a, b in zip(bin_num, self.mask)]
        floaters = [i for i, a in enumerate(masked_num) if a == 'X']
        combs = np.array(list(product(*[[(p, x) for x in (0, 1)] for p in floaters])))
        ret_nums = []
        for c in combs:
            new_bin = list(masked_num)
            for p in c:
                pos, val = p
                new_bin[pos] = str(val)
            ret_nums.append(int(''.join(new_bin), 2))
        return ret_nums



if __name__ == '__main__':
    # fp = "Day14_Input_test.txt"
    fp = 'Day14_Input.txt'
    with open(fp, 'r') as f:
        raw = f.readlines()
    data = [r.strip() for r in raw]

    part1 = Program()
    for line in data:
        part1.do_operation(line)

    print(f'Part1 answer: {sum(part1.memory.values()):.0f}')


    part2 = Program2()
    for line in data:
        part2.do_operation(line)

    print(f'Part2 answer: {sum(part2.memory.values()):.0f}')