import pytest

import rpsls

from collections import namedtuple

Play = namedtuple("Play", "name, winover")
test_all_plays_data = [
    Play(name="rock", winover=[1, 2, 3]),
    Play(name="paper", winover=[1, 2, 3]),
    Play(name="scissors", winover=[1, 2, 3]),
    Play(name="lizard", winover=[1, 2, 3]),
    Play(name="spock", winover=[1, 2, 3]),
]
test_single_plays_data = [
    ("rock", [Play(name="rock", winover=[1, 2, 3])]),
    ("scissors", [Play(name="scissors", winover=[1, 2, 3])]),
    ("spock", [Play(name="spock", winover=[1, 2, 3])]),
]


def test_output(capsys):
    rpsls.main()
    captured = capsys.readouterr()
    assert "Will play 15 rounds" in captured.out


def test_all_plays():
    assert rpsls.play() == test_all_plays_data


@pytest.mark.parametrize("arg, expected", test_single_plays_data)
# @pytest.mark.parametrize('arg, expected', [("spock", [Play(name="spock", winover=[1, 2, 3])])])
def test_single_plays(arg, expected):
    assert rpsls.play(arg) == expected


def test_single():
    assert rpsls.play("spock") == [Play(name="spock", winover=[1, 2, 3])]
