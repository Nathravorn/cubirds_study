# Project
This is a Python project to study the board game Cubirds.

Currently only the infrastructure to describe a game has been made, playing is still not possible.

# Example
The project can be tested by initializing an instance of `Game` and describing it using the `state_summary` method.

Output of `print(Game(2).state_summary())`:
    Current turn: 0
    Current player: 0

    Deck:
        {
            "cube": 14,
            "duck": 7,
            "flamant": 3,
            "hibou": 8,
            "parrot": 10,
            "pie": 13,
            "sandwich": 18,
            "toucan": 5
        }



    Player 0:
        Hand: cube, pie, duck, parrot, parrot, hibou, toucan, toucan
        Collection: sandwich
    Player 1:
        Hand: cube, cube, cube, duck, duck, toucan, flamant, flamant
        Collection: cube



    Board:
    Row 0: sandwich, duck, toucan
    Row 1: pie, hibou, flamant
    Row 2: cube, parrot, toucan
    Row 3: pie, duck, flamant

# Todo
[X] Make a class for a stack of cards, with methods to draw, add, subtract, get and set in dictionary and list form.
[>] Make a class for a game of Cubirds to store a persistent game state, with methods to play.
[ ] Study strategies by simulating random player actions.
[ ] Refine analysis by making agents smarter (using Monte-Carlo tree search).
[ ] Develop an Alpha-Zero-like reinforcement learning approach to learn optimal strategies through self-play.