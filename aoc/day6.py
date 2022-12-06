from aoc.utils import read_inputs
from more_itertools import windowed


def main():
    signal_inputs = read_inputs(6, False)

    required_start_packet_length = 4
    required_message_marker_length = 14

    for signal_input in signal_inputs:
        for count, chars in enumerate(
            windowed(signal_input, required_start_packet_length)
        ):
            if len(set(chars)) == required_start_packet_length:
                print(f"Part A: {count + required_start_packet_length}")
                break

        for count, chars in enumerate(
            windowed(signal_input, required_message_marker_length)
        ):
            if len(set(chars)) == required_message_marker_length:
                print(f"Part B: {count + required_message_marker_length}")
                break

    print("Done")
