# rock-paper-scissors-lizard-spock

## Reference

[Wikipedia: Rock–paper–scissors -> Additional weapons](https://en.wikipedia.org/wiki/Rock%E2%80%93paper%E2%80%93scissors#Additional_weapons)

## Rules

- rock: crushes lizard, crushes scissors
- paper: covers rock, disproves Spock
- scissors: cuts paper, decapitates lizard
- lizard: poisons Spock, eats paper
- Spock: smashes scissors, vaporises rock

## Usage

The program reads an environment variable (`RPSLS_ROUNDS`) to determine how many rounds to run.

If no set of players is defined the program will choose randomly two players for each round.

A set of players can be assigned in a file `rpsls.txt` which should be located in the same directory. The format of the file is simple text with two players (one round) on each line, for example:
```
player1 player2
player1 player2
...
```

If `number players < number of rounds` the program will cycle through the list and restart from the beginning until the number of rounds is completed. If `number of players > number of rounds` the program will stop once the number of rounds is completed ignoring the rest of the players lines.


## Testing

Set the ENV variables needed in `pytest.ini`.

Run:

```
(env) $ python -m pytest
```

or just

```
(env) $ pytest
```
