from typing import List


def read_inputs(day_number: int, test: bool) -> List[str]:
    test_file_segment = "/test" if test else ""

    with open(f"inputs{test_file_segment}/day{day_number}.txt") as input_file:
        return [line.strip() for line in input_file.readlines()]
