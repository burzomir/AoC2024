from parsy import string, regex

integer = regex(r'\d+').map(int)
mul = (
    string("mul(")
    >> integer.bind(lambda x: string(",") >> integer.map(lambda y: (x, y)))
    << string(")")
)

with open("./input.txt", "r") as file:
    data = file.read()
    total = 0
    while True:
        try:
            (a, b), remaining = mul.parse_partial(data)
            total += a * b
            data = remaining
        except:
            data = data[1:]
            if len(data) == 0:
                break
    print(total)
