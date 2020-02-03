import pytest

import rpsls

test_all_plays_data = {
    "rock": "scissors,lizard",
    "paper": "rock,spock",
    "scissors": "paper,lizard",
    "lizard": "spock,paper",
    "spock": "scissors,rock",
}
test_single_plays_data = [
    ("rock", ["lizard", "scissors"]),
    ("scissors", ["lizard", "paper"]),
    ("spock", ["rock", "scissors"]),
]


def test_output(capsys):
    rpsls.main()
    captured = capsys.readouterr()
    assert "Will play 15 rounds" in captured.out


def test_all_plays():
    assert rpsls.play() == test_all_plays_data


@pytest.mark.parametrize("arg, expected", test_single_plays_data)
# @pytest.mark.parametrize('arg, expected', [("spock", ["rock", "scissors"])])
def test_single_plays(arg, expected):
    assert rpsls.play(arg) == expected


def test_single():
    assert rpsls.play("spock") == ["rock", "scissors"]
