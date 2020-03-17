import pytest

import os
import rpsls

ROUNDS: int = int(os.environ.get("RPSLS_ROUNDS", 10))
test_all_players_data: dict = {
    "rock": "scissors,lizard",
    "paper": "rock,spock",
    "scissors": "paper,lizard",
    "lizard": "spock,paper",
    "spock": "scissors,rock",
}
test_all_results_data: list = list(test_all_players_data.keys()) + ["tie"]
test_single_players_data: list = [
    ("rock", ["lizard", "scissors"]),
    ("scissors", ["lizard", "paper"]),
    ("spock", ["rock", "scissors"]),
]
test_single_matches_data: list = [
    ("rock", "rock", "tie"),
    ("scissors", "lizard", "scissors"),
    ("lizard", "scissors", "scissors"),
    ("spock", "paper", "paper"),
    ("spock", "rock", "spock"),
    ("paper", "lizard", "lizard"),
]


## test the general behaviour
def test_output(capsys):
    rpsls.main()
    captured = capsys.readouterr()
    assert f"Will play {ROUNDS} rounds" in captured.out


## test the data (players, wins)
def test_all_players():
    assert rpsls.player() == test_all_players_data


# replaced with a more general test
# def test_single_player():
#     assert rpsls.player("spock") == ["rock", "scissors"]


@pytest.mark.parametrize("arg, expected", test_single_players_data)
# @pytest.mark.parametrize('arg, expected', [("spock", ["rock", "scissors"])])
def test_single_players(arg, expected):
    assert rpsls.player(arg) == expected


## test the results of a match (player vs player)

# replaced with a more general test
# def test_single_match_win():
#     assert rpsls.match("scissors", "rock") == "rock"
# def test_single_match_tie():
#     assert rpsls.match("rock", "rock") == "tie"


@pytest.mark.parametrize("arg1, arg2, expected", test_single_matches_data)
def test_single_matches(arg1, arg2, expected):
    assert rpsls.match(arg1, arg2) == expected


def test_random_single_match():
    assert rpsls.match() in test_all_results_data


def test_random_single_match_player_one():
    assert rpsls.match(one="spock") in test_all_results_data


def test_random_single_match_player_two():
    assert rpsls.match(two="rock") in test_all_results_data


## test e2e (full cycle of 15 matches)


# first with random players
def test_e2e_random_players(capsys):
    rpsls.main()
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()
    assert f"Will play {ROUNDS} rounds" in captured.out
    assert len(captured_lines) == 2 + ROUNDS
    assert all(line in test_all_results_data for line in captured_lines[2:])


# then with assigned players
