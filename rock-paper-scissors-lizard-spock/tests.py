import pytest

import rpsls


def test_output(capsys):
    rpsls.main()
    captured = capsys.readouterr()
    assert "Will play 15 rounds" in captured.out
