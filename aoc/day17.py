from aoc.utils import read_inputs


def next_jet(jet_patterns):
    counter = 0

    while True:
        yield jet_patterns[counter % len(jet_patterns)]
        counter += 1


def draw_shape(space, shape, row, col, char):
    for row_count, row_val in enumerate(shape):
        for col_count, val in enumerate(row_val):
            if val == "#":
                space[row - row_count][col + col_count] = char


def can_move(space, shape, new_row, new_col) -> bool:
    shape_height = len(shape)

    blocked = False

    for block_row in range(0, shape_height):
        for block_val, row_val in zip(
            space[new_row - block_row][new_col:], shape[block_row]
        ):
            if block_val == row_val == "#":
                blocked = True

    return not blocked


def pattern(seq):
    storage = {}
    for length in range(1, int(len(seq) / 2) + 1):
        valid_strings = {}
        for start in range(0, len(seq) - length + 1):
            valid_strings[start] = tuple(seq[start : start + length])
        candidates = set(valid_strings.values())
        if len(candidates) != len(valid_strings):
            storage = valid_strings
        else:
            break
    return set(v for v in storage.values() if list(storage.values()).count(v) > 1)


def calculate(jet_patterns, rock_count, sample_size=None) -> int:
    shapes = [
        [
            "####",
        ],
        [
            ".#.",
            "###",
            ".#.",
        ],
        [
            "..#",
            "..#",
            "###",
        ],
        [
            "#",
            "#",
            "#",
            "#",
        ],
        [
            "##",
            "##",
        ],
    ]

    width = 7

    block_heights = []

    space = []

    last_row = []

    for _ in range(0, width):
        last_row.append("#")

    space.append(last_row)

    current_shape_index = 0
    top_row = 0

    it = next_jet(jet_patterns)

    for counter in range(0, (sample_size or 2000)):
        current_shape = shapes[current_shape_index % len(shapes)]

        left_position = 2
        shape_width = max([len(row) for row in current_shape])
        shape_height = len(current_shape)

        shape_row = top_row + shape_height + 3

        additional_rows_needed = []

        if shape_row >= len(space):
            for _ in range(0, shape_row - len(space) + 1):
                new_row = []

                for _ in range(0, width):
                    new_row.append(".")

                additional_rows_needed.append(new_row)

            space.extend(additional_rows_needed)

        blocked = False

        while not blocked:
            jet_direction = next(it)

            if jet_direction == "<" and left_position > 0:
                left_delta = -1
            elif jet_direction == ">" and left_position + 1 <= width - shape_width:
                left_delta = 1
            else:
                left_delta = 0

            if can_move(space, current_shape, shape_row, left_position + left_delta):
                left_position += left_delta

            row_delta = 1

            if can_move(space, current_shape, shape_row - row_delta, left_position):
                shape_row -= row_delta
            else:
                blocked = True

            if blocked:
                draw_shape(space, current_shape, shape_row, left_position, "#")

                current_shape_index += 1

        for top_row, row_contents in enumerate(space):
            if all(val == "." for val in row_contents):
                top_row -= 1
                break

        block_heights.append(top_row)

    if sample_size is None:
        return top_row

    block_height_deltas = [
        second - first for second, first in zip(block_heights[1:], block_heights[:-1])
    ]

    longest_pattern = list(list(pattern(block_height_deltas))[0])
    longest_pattern_length = len(longest_pattern)
    pattern_starts = []

    for start in range(0, len(block_heights) - longest_pattern_length):
        if (
            block_height_deltas[start : start + longest_pattern_length]
            == longest_pattern
        ):
            pattern_starts.append(start)

    pattern_start_deltas = [
        second - first for second, first in zip(pattern_starts[1:], pattern_starts[:-1])
    ]

    pattern_cycle_length = pattern_start_deltas[0]
    pattern_start_index = pattern_starts[0]
    pattern_height = (
        block_heights[pattern_start_index + pattern_cycle_length]
        - block_heights[pattern_start_index]
    )

    return (
        rock_count - pattern_start_index
    ) // pattern_cycle_length * pattern_height + block_heights[
        (rock_count - pattern_start_index) % pattern_cycle_length
        + pattern_start_index
        - 1
    ]


def main():
    jet_pattern = read_inputs(17, False)[0]

    part_a = calculate(jet_pattern, 2022)
    print(part_a)

    part_b = calculate(
        jet_pattern, 1_000_000_000_000, sample_size=int(len(jet_pattern) * 1.5)
    )
    print(part_b)
