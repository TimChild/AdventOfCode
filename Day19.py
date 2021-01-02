import numpy as np
import copy
from typing import List, Union, Iterable, Callable
import re
from functools import partial
from itertools import product



class Receiver:

    def __init__(self, fp):
        self.fp = fp
        self.input_str = get_input_lines(fp)
        self.rules = get_rules(self.input_str)
        self.messages = get_messages(self.input_str)

        self._rule_0 = None

    @property
    def rule_0(self):
        if not self._rule_0:
            self._rule_0 = get_single_rule(self.rules, 0)
        return self._rule_0

    def messages_passed(self, check_long):
        return sum_messages(self.messages, self.rule_0, self.rules, check_long=check_long)



def get_input_lines(fp):
    with open(fp) as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def get_rules(inp_str):
    rules = {}
    for l in inp_str:
            num = re.match('\d+', l)
            if num:
                num = int(num[0])
                r = re.search('(?<=: ).+', l)[0]
                if r.startswith('"'):
                    r = r.strip('"')
                else:
                    r = [[int(n) for n in ns.split(' ')] for ns in r.split(' | ')]
                rules[num] = r
            else:
                break
    return rules


def get_messages(inp_str):
    messages = []
    for l in inp_str:
        if re.match('[a-z]', l):
            messages.append(l)
    return messages


def get_single_rule(all_rules: dict, rule: int) -> List[str]:
    value = all_rules[rule]
    if isinstance(value, str):
        return [value]
    elif isinstance(value, list):
        temp_list = []
        for sublist in value:
            sub_list = []
            for n in sublist:
                sub_list.append(get_single_rule(all_rules, n))
            temp_list.extend(list(product(*sub_list)))
        ret_list = [''.join(v) for v in temp_list]
        return ret_list
    else:
        print(value)
        raise NotImplementedError


def sum_messages(messages: List[str], rule: List[str], all_rules, check_long=False):
    length = len(rule[0])
    rule_hashes = [hash(r) for r in rule]
    checks = map(lambda m: check_message_fast(m, length, rule_hashes), [m for m in messages if len(m) == length])
    if check_long:
        pre_rule = get_single_rule(all_rules, 42)
        post_rule = get_single_rule(all_rules, 31)
        # remain_rule = get_single_rule(all_rules, 42)
        long_checks = [check_long_messages(pre_rule, post_rule, None, m, rule) for m in messages if len(m) > length]
        # long_checks = map(lambda m: check_long_messages(pre_rule, post_rule, None, m, rule), [m for m in messages if len(m) > length])
        checks = list(checks)
        checks.extend(list(long_checks))
    return sum(checks)



def check_message_fast(message: str, length: int, rule_hashes: List[int]):
    if len(message) != length:
        return False
    elif hash(message) in rule_hashes:
        return True
    else:
        return False


def check_message(message: str, rule: List[str]):
    return check_message_fast(message, length=len(rule[0]), rule_hashes=[hash(r) for r in rule])


def check_long_messages(pre_rule, post_rule, remain_rule, m, rule0):
    # NOTE: Rule 0 = [8, 11] and it is all 42s at beginning and then 31s at end
    normal_len = len(rule0[0])
    assert len(m) > normal_len
    # m, num_pre = remove_pre(m, pre_rule, min_length=len(post_rule[0])+len(remain_rule[0]))
    m, num_pre = remove_pre(m, pre_rule, min_length=0)
    if num_pre < 2:
        return False  # Did not find anything to match the beginning (or the first part of Rule11)
    # m, num_post = remove_post(m, post_rule, min_length=len(remain_rule[0]))
    m, num_post = remove_post(m, post_rule, min_length=0)
    if num_pre >= 1 + num_post and num_post >= 1 and len(m) == 0:  # Note: Only need to find one at end, but two at beginning because middle is same as beginning
        return True
    # if len(m) == len(remain_rule[0]):
    #     return check_message(m, remain_rule)
    return False


def remove_pre(message, rule, min_length):
    check_len = len(rule[0])
    m = message
    num = 0
    while m[:check_len] in rule and len(m) >= min_length+check_len:
        m = m[check_len:]
        num += 1
    return m, num


def remove_post(message, rule, min_length):
    check_len = len(rule[0])
    m = message
    num = 0
    while m[-check_len:] in rule and len(m) >= min_length+check_len:
        m = m[:-check_len]
        num += 1
    return m, num





if __name__ == '__main__':
    # fp = 'Day19_Input_test.txt'
    fp = 'Day19_Input.txt'


    rec = Receiver(fp)
    print(f'Rules: {rec.rules}')
    print(f'Messages: {rec.messages}')

    # print(f'5 = {get_single_rule(rec.rules, 5)}')
    # print(f'4 = {get_single_rule(rec.rules, 4)}')
    # print(f'3 = {get_single_rule(rec.rules, 3)}')
    # print(f'2 = {get_single_rule(rec.rules, 2)}')
    # print(f'1 = {get_single_rule(rec.rules, 1)}')
    # print(f'0 = {get_single_rule(rec.rules, 0)[:-5]}')


    for message in rec.messages[0:5]:
        print(f'Message: {message}\nPassed: {check_message(message, rec.rule_0)}')

    print(f'\n\n Part1:\nSum Passed: {rec.messages_passed(check_long=False)}\n')

    # Part 2
    # Make required changes
    fp = 'Day19_Input_test2.txt'
    rec2 = Receiver(fp)
    print(f'Test Before change: {rec2.messages_passed(check_long = False)}')
    print(f'Test After change: {rec2.messages_passed(check_long=True)}')


    print(f'\nPart2:\nSum = {rec.messages_passed(check_long=True)}')







    # old_8, old_11, old_42, old_31 = [get_single_rule(rec2.rules, n) for n in [8, 11, 42, 31]]
    # max_msg_len = max([len(m) for m in rec2.messages])


    # def gen_new_8(current_8, max_len, o42):
    #     temp = [o42, [x for x in current_8 if len(x) <= max_len-len(o42[0])]]
    #     return [''.join(v) for v in product(*temp)]
    #
    # def gen_new_11(current_11, max_len, o42, o31):
    #     temp = [o42, [x for x in current_11 if len(x) <= max_len-(len(o42[0])+len(o31[0]))], o31]
    #     return [''.join(v) for v in product(*temp)]
    #
    #
    # def make_new(old_to_change: List, other_old_parts: List[list], gen_function: Callable, max_len):
    #     parts = [old_to_change, *other_old_parts]
    #
    #     add_length = sum([min([len(x) for x in chunk]) for chunk in parts])
    #     newest_len = 0
    #     new = []
    #     current = old_to_change
    #     while newest_len < (max_msg_len - add_length):
    #         current = gen_function(current, max_len, *other_old_parts)
    #         new.extend([c for c in current if len(c) <= max_len])
    #         newest_len = max([len(x) for x in new])
    #     return list(set(new))
    #

    # new_8 = make_new(old_8, [old_42], gen_new_8, max_msg_len)
    # new_11 = make_new(old_11, [old_42, old_31], gen_new_11, max_msg_len)






