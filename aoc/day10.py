from aoc.utils import read_inputs


def main():
    instructions = read_inputs(10, False)

    cycle_count = 1
    registers = {"x": 1}
    history = {cycle_count: registers.copy()}

    for instruction in instructions:
        if instruction == "noop":
            cycle_count += 1

            history[cycle_count] = registers.copy()
        elif instruction.startswith("addx"):
            cycle_count += 1
            history[cycle_count] = registers.copy()

            cycle_count += 1
            registers["x"] += int(instruction.split(" ")[-1])
            history[cycle_count] = registers.copy()

    part_a = 0

    for signal_index in [20, 60, 100, 140, 180, 220]:
        lookup = history.get(signal_index)
        part_a += signal_index * lookup["x"]

    print(f"Part A: {part_a}")

    crt = []

    line_count = 6
    col_count = 40

    for line_counter in range(0, line_count):
        line = []

        for col_counter in range(0, col_count):
            line.append('.')

        crt.append(line)

    cycle_count = 0

    while True:
        sprite_x_position = history.get(cycle_count + 1)

        if sprite_x_position is None:
            break

        sprite_x_position = sprite_x_position["x"]

        pixel_x_location = cycle_count % col_count
        pixel_y_location = (cycle_count // col_count) % line_count

        if sprite_x_position - pixel_x_location in [-1, 0, 1]:
            crt[pixel_y_location][pixel_x_location] = "#"
        else:
            crt[pixel_y_location][pixel_x_location] = "."

        cycle_count += 1

    for line in crt:
        print("".join(line))
