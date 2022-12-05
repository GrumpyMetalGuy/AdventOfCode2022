from aoc.utils import read_inputs
import re
from typing import List


def first_non_space(text: str):
    text = text.strip()

    if text:
        return text.strip()[0]
    else:
        return text


def process(crates_inputs: List, move_bulk: bool):
    crate_rows = []
    crate_columns = [[]]

    for crate_input in crates_inputs:
        first_char = first_non_space(crate_input)

        if first_char == "[":
            # Dealing with a crate entry. Split into strings of len 4
            current_line = []

            for crate_detail in [
                crate_input[i : i + 4] for i in range(0, len(crate_input), 4)
            ]:
                current_line.append(crate_detail.strip("[ ]\n") or None)

            crate_rows.append(current_line)
        elif first_char.isdigit():
            # Work out how many columns we have and transpose the input
            crate_count = int(crate_input.strip().split(" ")[-1])

            for count in range(0, crate_count):
                crate_columns.append([])

            for crate_row in reversed(crate_rows):
                for column, crate in enumerate(crate_row):
                    if crate:
                        crate_columns[column + 1].append(crate)
        elif first_char == "m":
            # Perform the moves
            matcher = re.compile("move ([0-9]+) from ([0-9]+) to ([0-9]+)")

            move_count, from_col, to_col = matcher.findall(crate_input)[0]
            move_count, from_col, to_col = int(move_count), int(from_col), int(to_col)

            if move_bulk:
                remaining, moved = [
                    crate_columns[from_col][:-move_count],
                    crate_columns[from_col][-move_count:],
                ]

                crate_columns[to_col].extend(moved)
                crate_columns[from_col] = remaining
            else:
                for move in range(0, move_count):
                    crate_columns[to_col].append(crate_columns[from_col].pop())

    top_crates = "".join(
        filter(None, [column.pop() if column else None for column in crate_columns])
    )

    return top_crates


def main():
    crates_inputs = read_inputs(5, False, trim=False)

    part_a = process(crates_inputs, False)
    part_b = process(crates_inputs, True)

    print(f"Part A: {part_a}")
    print(f"Part B: {part_b}")
