import re

from aoc.utils import read_inputs

SENSOR_MATCH_RE = re.compile(
    r"Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)"
)


def calculate_mahattan_coverage_for_line(sensor_descriptions, debug: bool) -> int:
    line = 10 if debug else 2000000
    covered_x_coords = set()
    beacons = set()

    for sensor_description in sensor_descriptions:
        x, y, beacon_x, beacon_y = list(
            map(int, re.findall(SENSOR_MATCH_RE, sensor_description)[0])
        )

        beacons.add((beacon_x, beacon_y))

        manhattan_x = abs(x - beacon_x)
        manhattan_y = abs(y - beacon_y)

        total_manhattan_distance = manhattan_x + manhattan_y

        if y - total_manhattan_distance <= line <= y + total_manhattan_distance:
            y_offset = abs(y - line)

            for x_offset in range(
                x - total_manhattan_distance + y_offset,
                x + total_manhattan_distance - y_offset + 1,
            ):
                covered_x_coords.add(x_offset)

    for beacon in beacons:
        if beacon[1] == line and beacon[0] in covered_x_coords:
            covered_x_coords.remove(beacon[0])

    return len(covered_x_coords)


def find_non_covered_beacon(sensor_descriptions, debug):
    max_y = 20 if debug else 4000000
    max_x = 20 if debug else 4000000

    sensor_max_distances = {}

    for sensor_description in sensor_descriptions:
        x, y, beacon_x, beacon_y = list(
            map(int, re.findall(SENSOR_MATCH_RE, sensor_description)[0])
        )

        manhattan_x = abs(x - beacon_x)
        manhattan_y = abs(y - beacon_y)

        total_manhattan_distance = manhattan_x + manhattan_y

        sensor_max_distances[(x, y)] = total_manhattan_distance

    # Kind of klunky. For each row, we'll start at the beginning, and find which sensor covers this square. Once we
    # find it, we can jump to the furthest right edge of the sensor's coverage on this row. We then repeat. If we can't
    # find any sensors that cover this one, we're done. It's not super fast, but it gets the job done in reasonable
    # time. Go make yourself a coffee while you wait....
    y = 0

    while y <= max_y:
        x = 0

        while x <= max_x:
            reached = False

            seen_coords = set()

            for sensor_coords, sensor_max_distance in sensor_max_distances.items():
                if sensor_coords in seen_coords:
                    continue

                if (
                    abs(sensor_coords[0] - x) + abs(sensor_coords[1] - y)
                    <= sensor_max_distance
                ):
                    # This square is in range of this sensor, so we can jump ahead a bit without checking
                    seen_coords.add(sensor_coords)

                    y_diff = abs(y - sensor_coords[1])

                    new_x = sensor_coords[0] + sensor_max_distance - y_diff

                    if new_x > x:
                        x = new_x + 1
                        reached = True
                        break

            if not reached:
                return x * 4000000 + y

        y += 1

    return -1


def main():
    debug = False

    sensor_descriptions = read_inputs(15, debug)

    part_a = calculate_mahattan_coverage_for_line(sensor_descriptions, debug)

    print(f"Part A: {part_a}")

    part_b = find_non_covered_beacon(sensor_descriptions, debug)

    print(f"Part B: {part_b}")
