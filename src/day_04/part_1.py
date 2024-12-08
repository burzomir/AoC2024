
def get_columns(matrix):
    """Returns all columns of a 2D list."""
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


def get_diagonals(matrix):
    """
    Returns all diagonals parallel to the main diagonal (top-left to bottom-right).
    Includes diagonals above and below the main diagonal.
    """
    rows, cols = len(matrix), len(matrix[0])
    diagonals = []

    # Upper diagonals (including the main diagonal)
    for start in range(cols):
        diagonal = [matrix[i][start + i]
                    for i in range(min(rows, cols - start))]
        diagonals.append(diagonal)

    # Lower diagonals (excluding the main diagonal)
    for start in range(1, rows):
        diagonal = [matrix[start + i][i]
                    for i in range(min(rows - start, cols))]
        diagonals.append(diagonal)

    return diagonals


def get_anti_diagonals(matrix):
    """
    Returns all diagonals parallel to the anti-diagonal (top-right to bottom-left).
    Includes diagonals above and below the anti-diagonal.
    """
    rows, cols = len(matrix), len(matrix[0])
    diagonals = []

    # Upper diagonals (including the anti-diagonal)
    for start in range(cols):
        diagonal = [matrix[i][start - i] for i in range(min(rows, start + 1))]
        diagonals.append(diagonal)

    # Lower diagonals (excluding the anti-diagonal)
    for start in range(1, rows):
        diagonal = [matrix[start + i][cols - 1 - i]
                    for i in range(min(rows - start, cols))]
        diagonals.append(diagonal)

    return diagonals


xmas = ['X', 'M', 'A', 'S']


def count_row_xmas(row):
    if len(row) < 4:
        return 0
    index = 0
    counter = 0
    while (index <= len(row) - len(xmas)):
        if row[index:index + len(xmas)] == xmas:
            counter += 1
        index += 1
    return counter


def count_xmas(matrix):
    total = 0
    for row in matrix:
        total += count_row_xmas(row)
        total += count_row_xmas(list(reversed(row)))
    return total


with open("./input.txt", "r") as file:
    word_search = [list(line) for line in file.read().split("\n")]
    rows = word_search
    columns = get_columns(word_search)
    diagonals = get_diagonals(word_search)
    anti_diagonals = get_anti_diagonals(word_search)
    searches = [
        word_search,
        get_columns(word_search),
        get_diagonals(word_search),
        get_anti_diagonals(word_search)
    ]
    total = sum([count_xmas(matrix) for matrix in searches])
    print(total)
