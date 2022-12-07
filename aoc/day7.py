from aoc.utils import read_inputs

from typing import List, Dict, Optional

import benedict


def output_iterator(terminal_output: List[str]):
    yield from terminal_output


def traverse(
    fs: benedict.benedict,
    parent: str,
    output: Dict,
    *,
    size_filter: Optional[int] = None,
) -> int:
    total_size = 0

    for name, val in fs.items():
        if isinstance(val, benedict.benedict):
            sub_dir_size = traverse(
                val, f"{parent}/{name}", output, size_filter=size_filter
            )

            output_name = f"{parent}/{name}"

            if size_filter:
                if sub_dir_size < size_filter:
                    output[output_name] = sub_dir_size
            else:
                output[output_name] = sub_dir_size

            total_size += sub_dir_size
        else:
            total_size += val

    return total_size


def main():
    terminal_output = read_inputs(7, False)

    filesystem = benedict.benedict(keypath_separator="/")
    current_path_stack = []

    it = output_iterator(terminal_output)

    current_line = next(it)

    try:
        while current_line:
            current_line = current_line[2:]

            if current_line.startswith("cd "):
                current_line = current_line[3:]

                if current_line == "/":
                    current_path_stack = []
                elif current_line == "..":
                    current_path_stack.pop()
                else:
                    current_path_stack.append(current_line)

                current_line = next(it)
            else:
                # In ls mode, so grab lines until they start with $ again
                current_line = next(it)

                while not current_line.startswith("$"):
                    if current_line.startswith("dir "):
                        filesystem[
                            current_path_stack + [current_line[4:]]
                        ] = benedict.benedict(keypath_separator="/")
                    else:
                        size, name = current_line.split(" ")

                        size = int(size)

                        if current_path_stack:
                            filesystem[current_path_stack][name] = size
                        else:
                            filesystem[name] = size

                    current_line = next(it)
    except StopIteration:
        pass

    part_a_results = {}
    total_fs_used = traverse(filesystem, "", part_a_results, size_filter=100000)

    deletion_min_size = total_fs_used - (70000000 - 30000000)

    part_b_results = {}
    traverse(filesystem, "", part_b_results)

    print(f"Part A: {sum(part_a_results.values())}")
    print(
        f"Part B: {min(filter(lambda m: m > deletion_min_size, part_b_results.values()))}"
    )
