import more_itertools

from utils import read_inputs


def main():
    inputs = read_inputs(1, False)

    elf_calories = list(
        map(
            sum,
            [
                map(int, sub_list)
                for sub_list in more_itertools.split_at(inputs, lambda x: not x)
            ],
        )
    )

    part_a = max(elf_calories)

    part_b = sum(sorted(elf_calories)[-3:])

    print(f"Part A: {part_a}")
    print(f"Part B: {part_b}")
