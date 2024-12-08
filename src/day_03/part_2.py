from parsy import string, regex
from dataclasses import dataclass


@dataclass
class EnableMul:
    pass


@dataclass
class DisableMul:
    pass


@dataclass
class Mul:
    a: int
    b: int


integer = regex(r'\d+').map(int)
mul = (
    string("mul(")
    >> integer.bind(lambda x: string(",") >> integer.map(lambda y: Mul(a=x, b=y)))
    << string(")")
)
enable_mul = string("do()").map(lambda _: EnableMul())
disable_mul = string("don't()").map(lambda _: DisableMul())
instruction = enable_mul | disable_mul | mul

with open("./input.txt", "r") as file:
    data = file.read()
    total = 0
    enabled = True
    while True:
        try:
            instr, remaining = instruction.parse_partial(data)
            match instr:
                case EnableMul():
                    enabled = True
                case DisableMul():
                    enabled = False
                case Mul(a, b):
                    if enabled:
                        total += a * b
            data = remaining
        except:
            data = data[1:]
            if len(data) == 0:
                break
    print(total)
