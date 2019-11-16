import pytest

import rpsls

from collections import namedtuple

Play = namedtuple("Play", "name, winover")


def test_output(capsys):
    rpsls.main()
    captured = capsys.readouterr()
    assert "Will play 15 rounds" in captured.out


def test_play():
    assert rpsls.play() == [
        Play(name="rock", winover=[1, 2, 3]),
        Play(name="paper", winover=[1, 2, 3]),
        Play(name="scissors", winover=[1, 2, 3]),
        Play(name="lizard", winover=[1, 2, 3]),
        Play(name="spock", winover=[1, 2, 3]),
    ]
