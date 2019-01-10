# Project
This is a Python project to study the board game Cubirds.

The game is accessible through the `Game` class, which allows one to create a
game and play it until the end. When the game reaches the end, text will be
printed to indicate this.

Basic analysis functions are defined in `game_analysis.py`. In particular, the
function `available_moves(game)` returns a dictionary linking lay options (ways
to lay down birds on the board) to flock options (ways to make a flock of
birds), with a probability mapping for each flock option in the case of a lay
which induces a draw of two random cards. A custom estimation of the cards
remaining in the deck can be supplied to this function. Otherwise, it supports
using the base probabilities of the game or probabilities based on card
counting.

# Example
The project can be tested by initializing an instance of `Game` and describing
it using the `state_summary` method.

Output of `print(Game(1).state_summary())`:

    Current turn: 0
    Current player: 0
    Current phase: lay

    Board:
    Row 0:  sparrow,     cube,    hibou
    Row 1: sandwich,     duck,   parrot
    Row 2:   toucan, sandwich,  sparrow
    Row 3:  sparrow,  flamant,   parrot


    Player 0:
    Hand: cube, sandwich, sandwich, duck, duck, hibou, flamant, flamant
    Collection: sandwich



    Deck:
    {
        "cube": 18,
        "duck": 10,
        "flamant": 4,
        "hibou": 8,
        "parrot": 11,
        "sandwich": 15,
        "sparrow": 14,
        "toucan": 9
    }

In this example game, our analysis function can be tested using this script:

```python
game = Game(n_players=1, n_rows=4)
print(game.state_summary())
am = available_moves(game)
print_available_moves(am)
```

Which gives (truncated):

    {
      "('cube', 0, 'left')": [
          "small_flamant"
      ],
      "('cube', 0, 'right')": [
          "small_flamant"
      ],
      "('cube', 1, 'left')": {
          "('big_flamant',)": 0.1237698081734779,
          "('small_duck', 'small_flamant')": 0.013010842368640535,
          "('small_flamant', 'small_hibou')": 0.007506255212677232,
          "('small_flamant',)": 0.8557130942452046
      },
      "('cube', 1, 'right')": {
          "('big_flamant',)": 0.1237698081734779,
          "('small_duck', 'small_flamant')": 0.013010842368640535,
          "('small_flamant', 'small_hibou')": 0.007506255212677232,
          "('small_flamant',)": 0.8557130942452046
      }
      ...
    }

# Tests and benchmarks

You will need to install `pytest` and `pytest-benchmark`.

To run tests, run `./test [options]`; to run benchmarks, run `./perf [options]`.
The options are pytest options.
To save benchmarks for later comparison, use `./perf --benchmark-autosave`


# Todo

    [X] Make a class for a stack of cards, with methods to draw, add, subtract, get and set in dictionary and list form.
    [X] Make a class for a game of Cubirds to store a persistent game state, with methods to play rounds and advance the game to the end.
    [>] Study strategies by simulating random player actions.
    [ ] Refine analysis by making agents smarter (using a tree search algorithm with simulation of random events).
    [ ] Develop an Alpha-Zero-like reinforcement learning approach to learn optimal strategies through self-play.
