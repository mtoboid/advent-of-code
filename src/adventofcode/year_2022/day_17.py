"""
--- Day 17: Pyroclastic Flow ---

Your handheld device has located an alternative exit from the cave for you
and the elephants. The ground is rumbling almost continuously now, but the
strange valves bought you some time. It's definitely getting warmer in here,
though.

The tunnels eventually open into a very tall, narrow chamber. Large,
oddly-shaped rocks are falling into the chamber from above, presumably due to
all the rumbling. If you can't work out where the rocks will fall next,
you might be crushed!

The five types of rocks have the following peculiar shapes, where # is rock
and . is empty space:

####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##

The rocks fall in the order shown above: first the - shape, then the + shape,
and so on. Once the end of the list is reached, the same order repeats: the -
shape falls first, sixth, 11th, 16th, etc.

The rocks don't spin, but they do get pushed around by jets of hot gas coming
out of the walls themselves. A quick scan reveals the effect the jets of hot
gas will have on the rocks as they fall (your puzzle input).

For example, suppose this was the jet pattern in your cave:

>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>

In jet patterns, < means a push to the left, while > means a push to the
right. The pattern above means that the jets will push a falling rock right,
then right, then right, then left, then left, then right, and so on. If the
end of the list is reached, it repeats.

The tall, vertical chamber is exactly seven units wide. Each rock appears so
that its left edge is two units away from the left wall and its bottom edge
is three units above the highest rock in the room (or the floor, if there
isn't one).

After a rock appears, it alternates between being pushed by a jet of hot gas
one unit (in the direction indicated by the next symbol in the jet pattern)
and then falling one unit down. If any movement would cause any part of the
rock to move into the walls, floor, or a stopped rock, the movement instead
does not occur. If a downward movement would have caused a falling rock to
move into the floor or an already-fallen rock, the falling rock stops where
it is (having landed on something) and a new rock immediately begins falling.

Drawing falling rocks with @ and stopped rocks with #, the jet pattern in the
example above manifests as follows:

The first rock begins falling:
|..@@@@.|
|.......|
|.......|
|.......|
+-------+

Jet of gas pushes rock right:
|...@@@@|
|.......|
|.......|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
|.......|
|.......|
+-------+

Jet of gas pushes rock right, but nothing happens:
|...@@@@|
|.......|
|.......|
+-------+

Rock falls 1 unit:x
|...@@@@|
|.......|
+-------+

Jet of gas pushes rock right, but nothing happens:
|...@@@@|
|.......|
+-------+

Rock falls 1 unit:
|...@@@@|
+-------+

Jet of gas pushes rock left:
|..@@@@.|
+-------+

Rock falls 1 unit, causing it to come to rest:
|..####.|
+-------+

A new rock begins falling:
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|.......|
|..####.|
+-------+

Jet of gas pushes rock left:
|..@....|
|.@@@...|
|..@....|
|.......|
|.......|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|..@....|
|.@@@...|
|..@....|
|.......|
|.......|
|..####.|
+-------+

Jet of gas pushes rock right:
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|...@...|
|..@@@..|
|...@...|
|.......|
|..####.|
+-------+

Jet of gas pushes rock left:
|..@....|
|.@@@...|
|..@....|
|.......|
|..####.|
+-------+

Rock falls 1 unit:
|..@....|
|.@@@...|
|..@....|
|..####.|
+-------+

Jet of gas pushes rock right:
|...@...|
|..@@@..|
|...@...|
|..####.|
+-------+

Rock falls 1 unit, causing it to come to rest:
|...#...|
|..###..|
|...#...|
|..####.|
+-------+

A new rock begins falling:
|....@..|
|....@..|
|..@@@..|
|.......|
|.......|
|.......|
|...#...|
|..###..|
|...#...|
|..####.|
+-------+

The moment each of the next few rocks begins falling, you would see this:

|..@....|
|..@....|
|..@....|
|..@....|
|.......|
|.......|
|.......|
|..#....|
|..#....|
|####...|
|..###..|
|...#...|
|..####.|
+-------+

|..@@...|
|..@@...|
|.......|
|.......|
|.......|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@@@@.|
|.......|
|.......|
|.......|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|.......|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|....@..|
|....@..|
|..@@@..|
|.......|
|.......|
|.......|
|..#....|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@....|
|..@....|
|..@....|
|..@....|
|.......|
|.......|
|.......|
|.....#.|
|.....#.|
|..####.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@@...|
|..@@...|
|.......|
|.......|
|.......|
|....#..|
|....#..|
|....##.|
|....##.|
|..####.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

|..@@@@.|
|.......|
|.......|
|.......|
|....#..|
|....#..|
|....##.|
|##..##.|
|######.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+

To prove to the elephants your simulation is accurate, they want to know how
tall the tower will get after 2022 rocks have stopped (but before the 2023rd
rock begins falling). In this example, the tower of rocks will be 3068 units
tall.

How many units tall will the tower of rocks be after 2022 rocks have stopped
falling?

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import NamedTuple

from adventofcode.challenge import DayChallenge, Path


class Coordinates(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    up = 0
    left = 1
    down = 2
    right = 3

    @staticmethod
    def invert(direction: Direction) -> Direction:
        if direction == Direction.up:
            return Direction.down
        if direction == Direction.down:
            return Direction.up
        if direction == Direction.left:
            return Direction.right
        if direction == Direction.right:
            return Direction.left


class Rock(ABC):
    """A falling rock that comes in several shapes."""

    def __init__(self, height: int, width: int):
        # largest y stretch of the rock
        self._height: int
        # largest x stretch of the rock
        self._width: int
        # coordinates of the top left corner of the rock
        self._anchor: Coordinates

        self._height = height
        self._width = width
        self._anchor = Coordinates(0, 0)

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def anchor(self) -> Coordinates:
        """Top-left corner of the rock"""
        return self._anchor

    @anchor.setter
    def anchor(self, value: Coordinates) -> None:
        self._anchor = value

    @property
    def top(self) -> int:
        """Topmost y coordinate of the rock."""
        return self._anchor.y

    @property
    def bottom(self) -> int:
        """Bottommost y coordinate of the rock."""
        return self._anchor.y - (self.height - 1)

    @property
    def left(self) -> int:
        """Leftmost x coordinate of the rock."""
        return self._anchor.x

    @property
    def right(self) -> int:
        """Rightmost x coordinate of the rock."""
        return self._anchor.x + (self.width - 1)

    def move_up(self) -> None:
        """Move the rock upwards"""
        self._anchor = Coordinates(x=self._anchor.x, y=self._anchor.y + 1)

    def move_down(self) -> None:
        """Move the rock downwards"""
        self._anchor = Coordinates(x=self._anchor.x, y=self._anchor.y - 1)

    def move_left(self) -> None:
        self._anchor = Coordinates(x=self._anchor.x - 1, y=self._anchor.y)

    def move_right(self) -> None:
        self._anchor = Coordinates(x=self._anchor.x + 1, y=self._anchor.y)

    def move(self, direction: Direction) -> None:
        if direction == Direction.up:
            self.move_up()
        elif direction == Direction.left:
            self.move_left()
        elif direction == Direction.down:
            self.move_down()
        elif direction == Direction.right:
            self.move_right()

    @abstractmethod
    def squares(self) -> list[Coordinates]:
        """
        Return a list of coordinates that represent the squares that the rock
        covers.
        """


class HorizontalLine(Rock):
    """
    _####_
    """

    def __init__(self):
        super().__init__(height=1, width=4)

    def squares(self) -> list[Coordinates]:
        return [Coordinates(x=self.anchor.x + i, y=self.anchor.y)
                for i in range(self.width)]


class Cross(Rock):
    """
    _#_\n
    ###\n
    _#_\n
    """

    def __init__(self):
        super().__init__(height=3, width=3)

    def squares(self) -> list[Coordinates]:
        x = self.anchor.x
        y = self.anchor.y
        fields = [Coordinates(x=x + 1, y=y),
                  *[Coordinates(x=x + i, y=y - 1) for i in range(self.width)],
                  Coordinates(x=x + 1, y=y - 2)]
        return fields


class InvertedL(Rock):
    """
    __#\n
    __#\n
    ###\n
    """

    def __init__(self):
        super().__init__(height=3, width=3)

    def squares(self) -> list[Coordinates]:
        x = self.anchor.x
        y = self.anchor.y
        fields = [Coordinates(x=x + 2, y=y),
                  Coordinates(x=x + 2, y=y - 1),
                  *[Coordinates(x=x + i, y=y - 2) for i in range(self.width)]]
        return fields


class VerticalLine(Rock):
    """
    _#\n
    _#\n
    _#\n
    _#\n
    """

    def __init__(self):
        super().__init__(height=4, width=1)

    def squares(self) -> list[Coordinates]:
        x = self.anchor.x
        y = self.anchor.y
        return [Coordinates(x=x, y=y - i) for i in range(self.height)]


class Square(Rock):
    """
    _##_\n
    _##_\n
    """

    def __init__(self):
        super().__init__(height=2, width=2)

    def squares(self) -> list[Coordinates]:
        x = self.anchor.x
        y = self.anchor.y
        fields = [Coordinates(x=x + i, y=y - j)
                  for i in range(self.width)
                  for j in range(self.height)]
        return fields


class Cave:
    """A cave in which rocks are falling from the ceiling."""
    WIDTH: int = 7  # width of the cave (squares)
    ENTRY_POINT: int = 2  # point were new rocks (anchor) enter

    class Rocks:
        def __init__(self):
            self.rocks: list[type(Rock)] = [
                HorizontalLine, Cross, InvertedL, VerticalLine, Square
            ]
            self.current: int = -1

        def __iter__(self):
            return self

        def __next__(self) -> Rock:
            self.current += 1
            if self.current >= len(self.rocks):
                self.current = 0
            # return a Rock
            return self.rocks[self.current]()

    class Jet:
        SYMBOLS = {'<': Direction.left, '>': Direction.right}

        def __init__(self, pattern: str):
            self.position: int
            self.directions: list[Direction]

            self.position = -1
            self.directions = [Cave.Jet.SYMBOLS[char] for char in pattern]

        def __iter__(self):
            return self

        def __next__(self) -> Direction:
            self.position += 1
            if self.position >= len(self.directions):
                self.position = 0
            return self.directions[self.position]

    def __init__(self, jet_pattern: str):
        # iterator for rock to fall
        self.rock: Cave.Rocks = Cave.Rocks()
        # pattern for jets
        self.jet: Cave.Jet = Cave.Jet(jet_pattern)
        # rocks in the cave
        self.rubble: list[list[bool]] = [[True] * Cave.WIDTH]

    @property
    def rock_pile_height(self) -> int:
        """The current height of the rock pile"""
        return len(self.rubble) - 1

    def simulate_falling_rocks(self, n: int) -> None:
        """Let n rocks drop and come to rest on the rock-pile"""
        # distance from the top of the pile where a new rock appears
        fall_height: int = 3

        for _ in range(n):
            # new rock
            rock: Rock = next(self.rock)
            rock.anchor = Coordinates(x=Cave.ENTRY_POINT,
                                      y=self.rock_pile_height +
                                        rock.height +
                                        fall_height)
            # drop rock
            while not self.is_colliding(rock):
                self.move_rock_with_jet(rock)
                rock.move_down()
            # reached bottom
            rock.move_up()  # undo last move
            self.add_rock_to_rubble(rock)

    def is_colliding(self, rock: Rock) -> bool:
        """
        Check at least one point of the rock is colliding with the rubble
        already in the cave.
        When down is True only collisions downwards are checked
        """
        if rock.bottom > self.rock_pile_height:
            return False

        for sq in rock.squares():
            if sq.y <= self.rock_pile_height and self.rubble[sq.y][sq.x]:
                return True
        return False

    def move_rock_with_jet(self, rock: Rock) -> None:
        """Attempt to move a Rock with a jet stream."""
        direction = next(self.jet)
        if direction == Direction.left and rock.left <= 0:
            return
        if direction == Direction.right and rock.right >= Cave.WIDTH - 1:
            return
        rock.move(direction)
        # check if move results in a collision (sideways)
        if self.is_colliding(rock):
            # move rock back
            rock.move(Direction.invert(direction))

    def add_rock_to_rubble(self, rock: Rock) -> None:
        """
        Add the rock to the rubble pile in the cave.
        """
        while rock.top > self.rock_pile_height:
            self.rubble.append([False] * Cave.WIDTH)

        for sq in rock.squares():
            self.rubble[sq.y][sq.x] = True


class Day17(DayChallenge):
    """Advent of Code 2022 day 17"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 17

    def run(self, input_data: Path) -> None:
        data: list[str]

        with input_data.open() as file:
            data = file.read().split("\n")
        jet_pattern = ''.join(data).strip()

        cave: Cave = Cave(jet_pattern)
        # PART 1
        print("Part 1:")
        cave.simulate_falling_rocks(2022)
        print(f"Height of the rubble after 2022 rocks: {cave.rock_pile_height}")

        # PART 2
        print("\nPart 2:")

    def test(self):
        test_result: int = 3068
        test_n_rocks: int = 2022
        jet_pattern: str = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

        # The tall, vertical chamber is exactly seven units wide. Each rock
        # appears so that its left edge is two units away from the left wall
        # and its bottom edge is three units above the highest rock in the
        # room (or the floor, if there isn't one).

        cave: Cave = Cave(jet_pattern)
        print(f"Initial rubble pile: {cave.rock_pile_height}")
        cave.simulate_falling_rocks(test_n_rocks)
        print(f"Rubble pile after {test_n_rocks}: {cave.rock_pile_height}"
              f" (correct: {test_result})")
        # for i in range(6):
        #     cave.simulate_falling_rocks(1)
        #     print(f"Rock nr.: {i}\n")
        #     Day17.print_cave(cave)

    @staticmethod
    def print_cave(cave: Cave) -> None:
        rubble = cave.rubble
        for i in range(len(rubble) - 1, 0, -1):
            layer = ''.join(['#' if r else '.' for r in rubble[i]])
            print(f"|{layer}|")
        print(f"+-------+")
