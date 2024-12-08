
def get_main_diagonal(matrix):
    return [matrix[i][i] for i in range(min(len(matrix), len(matrix[0])))]


def get_anti_diagonal(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    return [matrix[i][cols - i - 1] for i in range(min(rows, cols))]


def get_window(matrix, top_left_row, top_left_col, size=3):
    return [
        row[top_left_col:top_left_col + size]
        for row in matrix[top_left_row:top_left_row + size]
    ]


def get_all_windows(matrix, window_size):
    windows = []
    rows = len(word_search)
    cols = len(word_search[0])
    for i in range(rows - window_size + 1):
        for j in range(cols - window_size + 1):
            window = get_window(matrix, i, j, window_size)
            windows.append(window)
    return windows


mas = ['M', 'A', 'S']


def is_xmas(window):
    diagonal = get_main_diagonal(window)
    anti_diagonal = get_anti_diagonal(window)
    return all([
        diagonal == mas or list(reversed(diagonal)) == mas,
        anti_diagonal == mas or (list(reversed(anti_diagonal))) == mas
    ])


with open("./input.txt", "r") as file:
    word_search = [list(line) for line in file.read().split("\n")]
    windows = get_all_windows(word_search, len(mas))
    result = list(filter(is_xmas, windows))
    print(len(result))
