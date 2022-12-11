"""
--- Day 2: Rock Paper Scissors ---

The Elves begin to set up camp on the beach. To decide whose tent gets to be
closest to the snack storage, a giant Rock Paper Scissors tournament is
already in progress.

Rock Paper Scissors is a game between two players. Each game contains many
rounds; in each round, the players each simultaneously choose one of Rock,
Paper, or Scissors using a hand shape. Then, a winner for that round is
selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats
Rock. If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an encrypted strategy
guide (your puzzle input) that they say will be sure to help you win. "The
first column is what your opponent is going to play: A for Rock, B for Paper,
and C for Scissors. The second column--" Suddenly, the Elf is called away to
help with someone's tent.

The second column, you reason, must be what you should play in response: X
for Rock, Y for Paper, and Z for Scissors. Winning every time would be
suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your
total score is the sum of your scores for each round. The score for a single
round is the score for the shape you selected (1 for Rock, 2 for Paper,
and 3 for Scissors) plus the score for the outcome of the round (0 if you
lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you,
you should calculate the score you would get if you were to follow the
strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z

This strategy guide predicts and recommends the following:

    In the first round, your opponent will choose Rock (A), and you should
    choose Paper (Y). This ends in a win for you with a score of 8 (2 because
    you chose Paper + 6 because you won). In the second round, your opponent
    will choose Paper (B), and you should choose Rock (X). This ends in a
    loss for you with a score of 1 (1 + 0). The third round is a draw with
    both players choosing Scissors, giving you a score of 3 + 3 = 6.

In this example, if you were to follow the strategy guide, you would get a
total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your
strategy guide?


--- Part Two ---

The Elf finishes helping with the tent and sneaks back over to you. "Anyway,
the second column says how the round needs to end: X means you need to lose,
Y means you need to end the round in a draw, and Z means you need to win.
Good luck!"

The total score is still calculated in the same way, but now you need to
figure out what shape to choose so the round ends as indicated. The example
above now goes like this:

    In the first round, your opponent will choose Rock (A), and you need the
    round to end in a draw (Y), so you also choose Rock. This gives you a
    score of 1 + 3 = 4. In the second round, your opponent will choose Paper
    (B), and you choose Rock so you lose (X) with a score of 1 + 0 = 1. In
    the third round, you will defeat your opponent's Scissors with Rock for a
    score of 1 + 6 = 7.

Now that you're correctly decrypting the ultra top secret strategy guide,
you would get a total score of 12.

Following the Elf's instructions for the second column, what would your total
score be if everything goes exactly according to your strategy guide?
"""

from enum import Enum
from adventofcode.challenge import DayChallenge, Path


class GameOutcome(Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6


class GameChoice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def play(self, other: 'GameChoice') -> GameOutcome:
        rock = GameChoice.ROCK
        paper = GameChoice.PAPER
        scissors = GameChoice.SCISSORS

        loss = GameOutcome.LOSS
        draw = GameOutcome.DRAW
        win = GameOutcome.WIN

        # draws
        if self == other:
            return draw

        # wins and losses
        if self == rock:
            if other == paper:
                return loss
            else:
                return win

        elif self == paper:
            if other == scissors:
                return loss
            else:
                return win

        elif self == scissors:
            if other == rock:
                return loss
            else:
                return win
        else:
            raise RuntimeError(f"Can't obtain result for self = {self}, "
                               f"other = {other}")


class Day2(DayChallenge):
    """Advent of Code year_2022 day 2"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 2

    def run(self, input_data: Path) -> None:
        data: list[str]
        total_score: int

        with input_data.open() as f:
            data = f.read().split("\n")

        # PART 1
        print("Part 1:")

        total_score = sum([Day2._line_to_score(line)
                           for line in data
                           if len(line) > 0])

        print(f"Total Score: {total_score}")

        # PART 2
        print("\nPart 2:")

        total_score_v2 = sum([Day2._line_to_score_v2(line)
                              for line in data
                              if len(line) > 0])

        print(f"Total Score (2): {total_score_v2}")

    @staticmethod
    def _score_for(my_choice: GameChoice, other_choice: GameChoice) -> int:
        """Return the score for one round of rock-paper-scissors"""

        score: int = 0
        score += my_choice.value
        score += my_choice.play(other_choice).value
        return score

    @staticmethod
    def _game_choice_from_letter(letter: str) -> GameChoice:
        conversion = {
            'A': GameChoice.ROCK,
            'B': GameChoice.PAPER,
            'C': GameChoice.SCISSORS,
            'X': GameChoice.ROCK,
            'Y': GameChoice.PAPER,
            'Z': GameChoice.SCISSORS
        }
        if letter not in conversion:
            raise ValueError(f"Letter: {letter} can not be converted.")
        return conversion[letter]

    @staticmethod
    def _game_outcome_from_letter(letter: str) -> GameOutcome:
        conversion = {
            'X': GameOutcome.LOSS,
            'Y': GameOutcome.DRAW,
            'Z': GameOutcome.WIN
        }
        if letter not in conversion:
            raise ValueError(f"Letter: {letter} can not be converted.")
        return conversion[letter]

    @staticmethod
    def _line_to_score(line: str) -> int:
        """Convert an input line of the format 'A X' or 'B X'... to a score."""

        other, me = line.strip().split()
        return Day2._score_for(Day2._game_choice_from_letter(me),
                               Day2._game_choice_from_letter(other))

    @staticmethod
    def _complementary_game_choice(
            other: GameChoice,
            outcome: GameOutcome
    ) -> GameChoice:

        rock = GameChoice.ROCK
        paper = GameChoice.PAPER
        scissors = GameChoice.SCISSORS
        win = GameOutcome.WIN
        draw = GameOutcome.DRAW
        loose = GameOutcome.LOSS

        convert = {
            rock:     {win: paper,    loose: scissors, draw: rock},
            paper:    {win: scissors, loose: rock,     draw: paper},
            scissors: {win: rock,     loose: paper,    draw: scissors}
        }

        return convert[other][outcome]

    @staticmethod
    def _line_to_score_v2(line: str) -> int:
        """Convert an input line of the format 'A X' or 'B X'... to a score."""

        letters = line.strip().split()
        other = Day2._game_choice_from_letter(letters[0])
        outcome = Day2._game_outcome_from_letter(letters[1])
        me = Day2._complementary_game_choice(other, outcome)
        return Day2._score_for(my_choice=me, other_choice=other)
