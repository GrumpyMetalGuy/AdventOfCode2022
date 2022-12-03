from aoc.utils import read_inputs


def score_round(opponent: str, you: str, win_lose: bool) -> int:
    if win_lose:
        if you == "Y":
            you = opponent
        elif you == "Z":
            you = {"A": "B", "B": "C", "C": "A"}.get(opponent)
        else:
            you = {"A": "C", "B": "A", "C": "B"}.get(opponent)
    else:
        you = {"X": "A", "Y": "B", "Z": "C"}.get(you)

    score = {"A": 1, "B": 2, "C": 3}.get(you)

    if opponent == you:
        score = score + 3
    elif (opponent, you) in {("A", "B"), ("B", "C"), ("C", "A")}:
        score = score + 6

    return score


def main():
    game_inputs = read_inputs(2, False)

    game_moves = [game_input.split(" ") for game_input in game_inputs]

    part_a = sum(score_round(opponent, you, False) for (opponent, you) in game_moves)
    part_b = sum(score_round(opponent, you, True) for (opponent, you) in game_moves)

    print(f"Part A: {part_a}")
    print(f"Part B: {part_b}")
