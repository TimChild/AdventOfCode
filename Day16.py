import re
import numpy as np
import pandas as pd


def get_rules(fp):
    raw_rules = []
    with open(fp, 'r') as f:
        for line in f:
            if line.strip():
                raw_rules.append(line.strip())
            else:
                break
    rules = {name: val for name, val in [l.split(':') for l in raw_rules]}
    for k in rules:
        rules[k] = [range(int(s), int(f)+1) for s, f in [r.split('-') for r in re.findall('\d+-\d+', rules[k])]]
    return rules


def get_my_ticket(fp) -> list:
    with open(fp, 'r') as f:
        for line in f:
            if line.strip() == 'your ticket:':
                ticket = f.readline().strip().split(',')
                break
    return ticket


def get_nearby_tickets(fp) -> pd.DataFrame:
    with open(fp, 'r') as f:
        for i, line in enumerate(f):
            if line.strip() == 'nearby tickets:':
                break
    nearby = pd.read_csv(fp, sep=',', skiprows=i+1, header=None)
    return nearby


def part1(rules, nearby):
    invalid_values = []
    invalid_rows = set()
    all_rules = [r for sublist in rules.values() for r in sublist]
    for i, ticket in nearby.iterrows():
        for v in ticket:
            if not any([v in r for r in all_rules]):
                invalid_values.append(v)
                invalid_rows.add(i)
    return invalid_values, invalid_rows


def determine_possible_rules(rules, nearby: pd.DataFrame) -> dict:
    possibilities = {rule: [] for rule in rules}
    for rule in rules:
        ranges = rules[rule]
        for i, column in enumerate(nearby.columns):
            if all(nearby[column].map(lambda x: any([x in r for r in ranges]))):
                possibilities[rule].append(i)
    return possibilities


def figure_out_combination(possiblities):
    def remove_opt(opt):
        for k in possiblities:
            possiblities[k] = possiblities[k] - {opt}

    possiblities = {k: set(v) for k, v in possiblities.items()}

    final_rules = {}
    while True:
        change_made = False
        for rule in possiblities:
            opts = possiblities[rule]
            if len(opts) == 1:
                opt = list(opts)[0]
                final_rules[rule] = opt
                remove_opt(opt)
                change_made = True
                break
        if not change_made:
            break
    if any([len(v) > 0 for v in possiblities.values()]):
        print(f'Remaining possibilities: {[(k, v) for k, v in possiblities.items() if len(v) > 0]}')
    return final_rules



if __name__ == '__main__':
    # fp = 'Day16_Input_test.txt'
    # fp = 'Day16_Input_test2.txt'
    fp = 'Day16_Input.txt'
    rules = get_rules(fp)
    my_ticket = get_my_ticket(fp)
    nearby_tickets = get_nearby_tickets(fp)

    print(rules, '\n\n', my_ticket, '\n\n', nearby_tickets)

    invalid_values, invalid_rows = part1(rules, nearby_tickets)
    print(f'\n\nPart1:\nInvalid rows: {invalid_rows}\nSum of invalid values: {sum(invalid_values)}\n\n')

    # Drop invalid rows
    nearby_tickets.drop(invalid_rows, inplace=True)

    possibilities = determine_possible_rules(rules, nearby_tickets)
    print(f'Possibility of rules: {possibilities}')

    final_rules = figure_out_combination(possibilities)
    print(f'Final Rules: {final_rules}')

    print(f'\n\nPart2:\nProduct = :{np.product([float(my_ticket[x]) for k, x in final_rules.items() if k.startswith("departure")]):.0f}')


