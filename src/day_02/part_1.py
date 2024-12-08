from collections import Counter


def compare(a, b):
    if abs(a - b) > 3:
        return 'x'
    if a < b:
        return '<'
    if a > b:
        return '>'
    return 'x'


def analyze_report(report):
    analysis = [compare(a, b) for a, b in zip(report, report[1:])]
    return all(v == '>' for v in analysis) or all(v == '<' for v in analysis)


with open("./input.txt", "r") as file:
    reports = [[int(v) for v in line.strip().split(" ")] for line in file]
    counter = Counter([analyze_report(report) for report in reports])
    print(counter[True])
