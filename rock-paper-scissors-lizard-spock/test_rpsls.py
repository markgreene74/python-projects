import pytest

import rpsls

test_all_players_data = {
    "rock": "scissors,lizard",
    "paper": "rock,spock",
    "scissors": "paper,lizard",
    "lizard": "spock,paper",
    "spock": "scissors,rock",
}
test_single_players_data = [
    ("rock", ["lizard", "scissors"]),
    ("scissors", ["lizard", "paper"]),
    ("spock", ["rock", "scissors"]),
]
test_single_matches_data = [
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
    assert "Will play 15 rounds" in captured.out


## test the data (players, wins)
def test_all_players():
    assert rpsls.player() == test_all_players_data


# replaced by a more general test
# def test_single_player():
#     assert rpsls.player("spock") == ["rock", "scissors"]


@pytest.mark.parametrize("arg, expected", test_single_players_data)
# @pytest.mark.parametrize('arg, expected', [("spock", ["rock", "scissors"])])
def test_single_players(arg, expected):
    assert rpsls.player(arg) == expected


## test the results of a match (player vs player)
# replaced it with a more general test
# def test_single_match_win():
#     assert rpsls.match("scissors", "rock") == "rock"
# def test_single_match_tie():
#     assert rpsls.match("rock", "rock") == "tie"


@pytest.mark.parametrize("arg1, arg2, expected", test_single_matches_data)
def test_single_matches(arg1, arg2, expected):
    assert rpsls.match(arg1, arg2) == expected


def test_random_single_match():
    assert rpsls.match() in list(test_all_players_data.keys()) + ["tie"]


def test_random_single_match_player_one():
    assert rpsls.match(one="spock") in list(test_all_players_data.keys()) + ["tie"]


def test_random_single_match_player_two():
    assert rpsls.match(two="rock") in list(test_all_players_data.keys()) + ["tie"]
