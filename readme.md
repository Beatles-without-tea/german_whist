# German Whist Python Game

This is a German Whist card game implemented in Python that utilizes the Monte Carlo Tree Search (MCTS) algorithm to simulate an intelligent opponent. 

## Overview

German Whist is a variation of the classic Whist card game for two players. The uniqueness of this project lies in its use of MCTS, a heuristic search algorithm used for making optimal decisions in a given context, to simulate an opponent. This opponent adapts its strategy based on the game's progression and player's actions, providing a challenging gaming experience.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.7 or later
- pip package manager

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/Beatles-without-tea/german_whist.git
cd german_whist
```

Install the necessary packages:

```bash
pip install -r requirements.txt
```

### Usage

To start a new game, run:

```bash
python german_whist.py
```

The game will start and you'll be asked to make your move via command line prompts.
Simply select a card from the list of cards proposed.

## Game Rules

German Whist is a two-player game played with a standard 52-card deck. The object of the game is to win more tricks than your opponent. The game consists of two halves:

### The First Half (Tricks)

1. The dealer shuffles the deck and the non-dealer cuts. The dealer then deals out the entire deck, one card at a time, so that both players have 13 cards and there is a "stock" pile of 26 cards left over. The top card of the stock is turned face up.

2. The non-dealer leads to the first trick. A trick consists of both players playing one card, with the second card played either following suit (matching the suit of the first card) or being a card of a different suit.

3. If both cards are of the same suit, the higher card wins the trick. If they are of different suits, the player who led the trick wins. The winner of a trick leads to the next trick.

4. Before the next trick starts, both players draw a card from the top of the stock, beginning with the winner of the trick. The face-up card is also drawn, but this is done last and can be drawn by either player (the winner if the stock is empty, or the player who will lead to the next trick if it is not).

5. The first half of the game continues until the stock is exhausted. At this point, each player will have a hand of 13 cards and will have won a certain number of tricks.

### The Second Half (Points)

1. The player who took more tricks in the first half of the game leads to the first trick of the second half. Play continues as before, but without any cards being drawn, and with the rule that players must always follow suit if they can.

2. In the second half of the game, each trick is worth one point. The player who scores more points in the second half wins the game.

Remember, strategic play in the first half can greatly affect the outcome in the second half!

<!-- ## Contributing

If you're interested in improving the game or adding features, feel free to fork the repository and submit pull requests. We'd love to get your contributions. -->

## License

This project is licensed under the MIT License. See the LICENSE.md file for details.


