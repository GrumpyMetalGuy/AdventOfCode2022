import functools
import operator

from aoc.utils import read_inputs


def main():
    forest_input = read_inputs(8, False)

    forest = [list(forest_input_line) for forest_input_line in forest_input]

    unobstructed_count = 0

    line_count = len(forest)
    col_count = len(forest[0])

    for line_counter in range(0, line_count):
        for col_counter in range(0, col_count):
            if (
                line_counter == 0
                or col_counter == 0
                or line_counter == line_count - 1
                or col_counter == col_count - 1
            ):
                unobstructed_count += 1
                continue

            height_to_compare = forest[line_counter][col_counter]

            blocked = False

            for line_check in range(0, line_counter):
                if forest[line_check][col_counter] >= height_to_compare:
                    blocked = True
                    break

            if not blocked:
                unobstructed_count += 1
                continue

            blocked = False

            for line_check in range(line_counter + 1, line_count):
                if forest[line_check][col_counter] >= height_to_compare:
                    blocked = True
                    break

            if not blocked:
                unobstructed_count += 1
                continue

            blocked = False

            for col_check in range(0, col_counter):
                if forest[line_counter][col_check] >= height_to_compare:
                    blocked = True
                    break

            if not blocked:
                unobstructed_count += 1
                continue

            blocked = False

            for col_check in range(col_counter + 1, col_count):
                if forest[line_counter][col_check] >= height_to_compare:
                    blocked = True
                    break

            if not blocked:
                unobstructed_count += 1

    print(f"Part A: {unobstructed_count}")

    max_scenic_score = 0

    for line_counter in range(0, line_count):
        for col_counter in range(0, col_count):
            multipliers = []

            primary_tree_height = forest[line_counter][col_counter]

            visible_tree_count = 0

            for line_check in range(line_counter - 1, -1, -1):
                visible_tree_count += 1

                if forest[line_check][col_counter] >= primary_tree_height:
                    break

            multipliers.append(visible_tree_count)

            visible_tree_count = 0

            for line_check in range(line_counter + 1, line_count):
                visible_tree_count += 1

                if forest[line_check][col_counter] >= primary_tree_height:
                    break

            multipliers.append(visible_tree_count)

            visible_tree_count = 0

            for col_check in range(col_counter - 1, -1, -1):
                visible_tree_count += 1

                if forest[line_counter][col_check] >= primary_tree_height:
                    break

            multipliers.append(visible_tree_count)

            visible_tree_count = 0

            for col_check in range(col_counter + 1, col_count):
                visible_tree_count += 1

                if forest[line_counter][col_check] >= primary_tree_height:
                    break

            multipliers.append(visible_tree_count)

            scenic_score = functools.reduce(operator.mul, filter(None, multipliers), 1)

            max_scenic_score = max(max_scenic_score, scenic_score)

    print(f"Part B: {max_scenic_score}")
