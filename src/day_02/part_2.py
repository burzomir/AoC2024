from collections import Counter
from enum import Enum, auto


class ReportStatus(Enum):
    Safe = auto()
    Unsafe = auto()


def compare(a, b):
    if abs(a - b) > 3:
        return 'x'
    if a < b:
        return '<'
    if a > b:
        return '>'
    return 'x'


def analyze_report(report):
    return [compare(a, b) for a, b in zip(report, report[1:])]


def is_safe(report, analysis):
    counter = Counter(analysis)
    return any([
        counter['>'] == len(report),
        counter['>'] == len(report) - 1,
        counter['<'] == len(report),
        counter['<'] == len(report) - 1
    ])


def find_error_index(analysis):
    error_index = -1
    for index in range(len(analysis) - 1):
        if analysis[index] != analysis[index + 1]:
            error_index = index
            break
    if error_index != -1:
        return error_index + 1
    return error_index


def check_report(report):
    analysis = analyze_report(report)
    if (is_safe(report, analysis)):
        return ReportStatus.Safe

    error_index = find_error_index(analysis)

    for i in [error_index - 1, error_index, error_index + 1]:
        r = report[:]
        del r[i]
        a = analyze_report(r)
        if (is_safe(r, a)):
            return ReportStatus.Safe

    return ReportStatus.Unsafe


with open("./input.txt", "r") as file:
    reports = [[int(v) for v in line.strip().split(" ")] for line in file]
    status_counter = Counter([check_report(report) for report in reports])
    print(status_counter[ReportStatus.Safe])
