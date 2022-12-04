from aoc.utils import read_inputs


def main():
    assignments = read_inputs(4, False)

    part_a_count = 0
    part_b_count = 0

    for assignment in assignments:
        elf_one, elf_two = assignment.split(",")
        elf_one_lower, elf_one_higher = elf_one.split("-")
        elf_two_lower, elf_two_higher = elf_two.split("-")

        elf_one_range = set(range(int(elf_one_lower), int(elf_one_higher) + 1))
        elf_two_range = set(range(int(elf_two_lower), int(elf_two_higher) + 1))

        common = elf_one_range.intersection(elf_two_range)

        if common == elf_one_range or common == elf_two_range:
            part_a_count = part_a_count + 1

        if common:
            part_b_count = part_b_count + 1

    print(f"Part A: {part_a_count}")
    print(f"Part B: {part_b_count}")
