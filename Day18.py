import numpy as np
import re



class Calculator:

    def __init__(self, question: str, part = 1):
        self.question = question
        self.part = part
        self.state = sanitize_chars(list(self.question.replace(' ', '')))

    def calc_step(self):
        self.state = iter_calc(self.state, self.part)
        return self.state

    def do_all(self):
        while len(self.state) > 1:
            self.calc_step()
        return self.state[0]


def do_op(a, op, b):
    if op == '*':
        return a*b
    elif op == '+':
        return a+b
    elif op == '-':
        return a-b
    else:
        raise ValueError


def sanitize_chars(chars):
    for i, c in enumerate(chars):
        try:
            chars[i] = int(c)
        except ValueError:
            pass
    return chars


def iter_calc(chars, part = 1):
    new_chars = []
    i = 0
    temp_val = None
    if part == 2 and '+' in chars:
        allowed_ops = ['+']
    else:
        allowed_ops = ['+', '*']
    while True:

        if i > len(chars) - 3:
            if temp_val is not None:
                new_chars.append(temp_val)
                if i + 1 < len(chars):
                    new_chars.extend(chars[i+1:])
            else:
                new_chars.extend(chars[i:])
            break
        c0, c1, c2 = chars[i:i+3]
        if isinstance(c0, int):
            if c1 == ')':
                if temp_val:
                    new_chars.append(temp_val)
                    new_chars.extend(chars[i+1:])
                else:
                    new_chars.extend(chars[i:])
                break  # Gotta be careful of closing brackets
            elif c1 not in allowed_ops:
                if temp_val:
                    new_chars.extend([temp_val, c1, c2])
                    temp_val = None
                else:
                    new_chars.extend([c0, c1, c2])
                i += 3
            elif c2 not in ['(', ')']:
                if temp_val is None:
                    temp_val = c0
                temp_val = do_op(temp_val, c1, c2)
                i += 2
            else:
                if temp_val is not None:
                    new_chars.extend([temp_val, c1, c2])
                    temp_val = None
                else:
                    new_chars.extend([c0, c1, c2])
                i += 3

        else:
            new_chars.append(c0)
            i += 1
    new_chars = remove_redundant_parens(new_chars)
    return new_chars



def remove_redundant_parens(chars):
    if len(chars) == 1:
        return chars

    new_chars = []
    i = 0
    while i < len(chars):
        if i + 3 > len(chars):
            new_chars.extend(chars[i:])
            break
        c0, c1, c2 = chars[i:i+3]
        if c0 == '(' and c2 == ')':
            new_chars.append(c1)
            i += 3
        else:
            new_chars.append(c0)
            i += 1
    return new_chars

    # string = ''.join((str(c) for c in chars))
    # string = re.sub(r'\((\d+)\)', r'\1', string)
    # chars = sanitize_chars(list(string.split())
    # return chars



if __name__ == '__main__':
    fp = 'Day18_Input_test.txt'

    TEST_ANSWERS = [26, 437, 122240, 13632]

    with open(fp, 'r') as f:
        test_qs = [l.strip() for l in f.readlines()]

    for q in test_qs:
        c = Calculator(q)
        print(f'Test Question: {c.question}\nAnswer: {c.do_all()}')


    fp = 'Day18_Input.txt'
    with open(fp, 'r') as f:
        qs = [l.strip() for l in f.readlines()]

    answers = []
    for q in qs:
        c = Calculator(q)
        ans = c.do_all()
        print(f'Question: {c.question}\nAnswer: {ans}')
        answers.append(ans)

    print(f'\n\nPart1:\nSum = {sum(answers)}\n\n')


    for q in test_qs:
        c = Calculator(q, part=2)
        print(f'Test Question: {c.question}\nAnswer: {c.do_all()}')



