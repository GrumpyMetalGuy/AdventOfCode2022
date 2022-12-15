from aoc.utils import read_inputs


def generate_cavern(rock_descriptions, cavern):
    for rock_description in rock_descriptions:
        rock_coordinates = rock_description.split(" -> ")

        for rock_start, rock_end in zip(rock_coordinates[:-1], rock_coordinates[1:]):
            start_x, start_y = rock_start.split(",")

            start_x = int(start_x)
            start_y = int(start_y)

            end_x, end_y = rock_end.split(",")

            end_x = int(end_x)
            end_y = int(end_y)

            if start_x == end_x:
                x_offset = 0

                if start_y > end_y:
                    y_offset = -1
                else:
                    y_offset = 1

            if start_y == end_y:
                y_offset = 0

                if start_x > end_x:
                    x_offset = -1
                else:
                    x_offset = 1

            cavern[start_y][start_x] = "#"

            while start_x != end_x or start_y != end_y:
                start_x += x_offset
                start_y += y_offset

                cavern[start_y][start_x] = "#"


def simulate_sandfall(cavern, look_for_blocked, min_x, max_x, max_y):
    count = 0

    if look_for_blocked:
        cavern.append(["." for _ in range(min_x, max_x + 1)])
        cavern.append(["#" for _ in range(min_x, max_x + 1)])
        max_y += 2

    while True:
        sand_x = 500
        sand_y = 0

        resting = False
        falling = False
        blocked = False

        while not resting and not falling and not blocked:
            if sand_y >= max_y:
                falling = True
                break

            if cavern[0][500] == "o":
                blocked = True
                break

            below = cavern[sand_y + 1][sand_x]

            if below == ".":
                sand_y += 1
                continue

            if sand_x - 1 < min_x:
                falling = True
                break

            below_left = cavern[sand_y + 1][sand_x - 1]

            if below_left == ".":
                sand_y += 1
                sand_x -= 1
                continue

            if sand_x + 1 > max_x:
                falling = True
                break

            below_right = cavern[sand_y + 1][sand_x + 1]

            if below_right == ".":
                sand_y += 1
                sand_x += 1
                continue

            cavern[sand_y][sand_x] = "o"
            resting = True
            break

        if resting:
            count += 1
        elif falling or blocked:
            break

    for cavern_line in cavern:
        print("".join(cavern_line))

    return count


def main():
    rock_descriptions = read_inputs(14, False)

    min_x = min_y = 99999
    max_x = max_y = -99999

    for rock_description in rock_descriptions:
        for rock_coordinates in rock_description.split(" -> "):
            x, y = rock_coordinates.split(",")

            min_x = min(min_x, int(x))
            max_x = max(max_x, int(x))

            min_y = 0
            max_y = max(max_y, int(y))

    # Hack in some extra space to allow us to not need to worry about offsetting x coords
    cavern = [["." for _ in range(0, max_x * 2)] for __ in range(min_y, max_y + 1)]

    generate_cavern(rock_descriptions, cavern)

    part_a = simulate_sandfall(cavern, False, min_x, max_x, max_y)

    print(f"Part A: {part_a}")

    cavern = [["." for _ in range(0, max_x * 2)] for __ in range(min_y, max_y + 1)]

    generate_cavern(rock_descriptions, cavern)

    part_b = simulate_sandfall(cavern, True, 0, max_x * 2, max_y)

    print(f"Part B: {part_b}")
