def read_disk_map(compact_disk_map):
    id = 0
    on_file_block = True
    disk_map = []
    for c in compact_disk_map:
        if on_file_block:
            blocks = [id] * int(c)
            disk_map.extend(blocks)
            id += 1
        else:
            blocks = ["."] * int(c)
            disk_map.extend(blocks)
        on_file_block = not on_file_block
    return disk_map


def next_free_space_index(current_index, disk_map):
    index = current_index
    while index < len(disk_map):
        if disk_map[index] == ".":
            return index
        else:
            index += 1
    return None


def next_block_index(current_index, disk_map):
    index = current_index
    while index < len(disk_map):
        if disk_map[index] != ".":
            return index
        else:
            index -= 1
    return None


def defragment(disk_map):
    disk_map = list(disk_map)
    free_space_index = next_free_space_index(0, disk_map)
    last_block_index = next_block_index(len(disk_map) - 1, disk_map)
    while free_space_index <= last_block_index:
        disk_map[free_space_index] = disk_map[last_block_index]
        disk_map[last_block_index] = "."
        free_space_index = next_free_space_index(free_space_index, disk_map)
        last_block_index = next_block_index(last_block_index, disk_map)
    return disk_map


def get_checksum(disk_map):
    checksum = 0
    for index, c in enumerate(disk_map):
        if c == ".":
            continue
        checksum += index * int(c)
    return checksum


with open("./input.txt", "r") as file:
    disk_map = read_disk_map(file.read())
    disk_map = defragment(disk_map)
    checksum = get_checksum(disk_map)
    print(checksum)
