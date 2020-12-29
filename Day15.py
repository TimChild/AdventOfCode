import numpy as np
import pandas as pd
from collections import OrderedDict


EXAMPLES = {
    (0,3,6): 436,
    (1,3,2): 1,
    (2,1,3): 10,
    (1,2,3): 27,
    (2,3,1): 78,
    (3,2,1): 438,
    (3,1,2): 1836
}

INPUT = (6,4,12,1,20,0,16)

class Elf:
    def __init__(self, start_nums):
        self.memory = OrderedDict()
        self.pos = 0
        self.new = False
        self.answer = None
        for n in start_nums:
            self.set_num(n)

    @property
    def last(self):
        last_key = next(reversed(self.memory))
        return last_key, self.memory[last_key]

    def set_num(self, num):
        past = None
        if num not in self.memory:
            self.new = True
        else:
            self.new = False
            past = self.get_diff(num)
            del self.memory[num]
        self.memory[num] = (self.pos, past)
        self.pos += 1

    def get_diff(self, num):
        return self.pos - self.memory[num][0]

    # def check_exists(self, num):
    #     if num in self.memory:
    #         return True
    #     return False

    def take_turn(self):
        if self.new:
            self.set_num(0)
        else:
            self.set_num(self.last[1][1])

    def play_game(self):
        while self.pos < 2020:
            self.take_turn()
        self.answer = self.last[0]


if __name__ == '__main__':
    elf = Elf([0, 3, 6])
    for i in range(4, 11):
        elf.take_turn()
        print(f'Turn {i}: {elf.last}, Pos: {elf.pos}')

    for ex in EXAMPLES:
        elf = Elf(ex)
        elf.play_game()
        print(f'Expected ans: {EXAMPLES[ex]}, Elf ans: {elf.answer}, Elf pos: {elf.pos}')

    elf = Elf(INPUT)
    elf.play_game()
    print(f'Part1 Answer: {elf.answer}')

    elf = Elf(INPUT)
    while elf.pos < 3e7:
        elf.take_turn()
        if not elf.pos % 5e6:
            print(f'Pos: {elf.pos}, last: {elf.last}')
    print(f'\nPart2 Answer: {elf.last[0]}, pos = {elf.pos}')