from dataclasses import dataclass
from parsy import string, regex, seq


@dataclass
class Rule:
    page_before: int
    page_after: int


@dataclass
class Update:
    pages: list[int]

    def middle_page(self):
        return self.pages[len(self.pages) // 2]


integer = regex(r'\d+').map(int)


rule_parser = seq(integer, string("|"), integer).map(
    lambda x: Rule(page_before=x[0], page_after=x[2]))
ruleset_parser = seq(rule_parser, string("\n")).map(lambda x: x[0]).many()

update_parser = seq(integer, string(",") | string("")).map(
    lambda x: x[0]).many().map(lambda xs: Update(xs))

updateset_parser = seq(update_parser, string("\n")).map(lambda x: x[0]).many()

input_parser = seq(ruleset_parser, string(
    "\n"), updateset_parser).map(lambda x: (x[0], x[2]))


class RuleDict:
    def __init__(self):
        self.dict = dict()

    def add(self, rule: Rule):
        if not rule.page_before in self.dict:
            self.dict[rule.page_before] = set()
        self.dict[rule.page_before].add(rule.page_after)

    def get_pages_after(self, page: int):
        if page in self.dict:
            return self.dict[page]
        return set()


def check_order(rule_dict: RuleDict, update: Update):
    pages_checked = set()
    for page in update.pages:
        pages_after = rule_dict.get_pages_after(page)
        if len(pages_after & pages_checked) > 0:
            return False
        pages_checked.add(page)
    return True


with open("./input.txt", "r") as file:
    ruleset, updateset = input_parser.parse(file.read())
    rule_dict = RuleDict()
    for rule in ruleset:
        rule_dict.add(rule)
    total = 0
    for update in updateset:
        if (check_order(rule_dict, update)):
            total += update.middle_page()
    print(total)
