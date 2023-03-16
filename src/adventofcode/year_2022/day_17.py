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


--- Part Two ---

The elephants are not impressed by your simulation. They demand to know how
tall the tower will be after 1000000000000 rocks have stopped! Only then will
they feel confident enough to proceed through the cave.

In the example above, the tower would be 1514285714288 units tall!

How tall will the tower be after 1000000000000 rocks have stopped?

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from itertools import chain
from typing import NamedTuple, Iterable

from adventofcode.challenge import DayChallenge, Path


class Direction(Enum):
    """A direction going straight (up, down, right, left)"""
    up = 0
    right = 1
    down = 2
    left = 3

    @staticmethod
    def invert(direction: Direction) -> Direction:
        """Get the opposite direction."""
        if direction == Direction.up:
            return Direction.down
        if direction == Direction.down:
            return Direction.up
        if direction == Direction.left:
            return Direction.right
        if direction == Direction.right:
            return Direction.left


class Coordinates(NamedTuple):
    """Coordinates of a square on a grid. 0|0 is bottom left!"""
    x: int
    y: int

    def get_adjacent(self, direction: Direction) -> Coordinates:
        """Get adjacent coordinates."""
        if direction == direction.up:
            return Coordinates(x=self.x, y=self.y + 1)
        if direction == direction.right:
            return Coordinates(x=self.x + 1, y=self.y)
        if direction == direction.down:
            return Coordinates(x=self.x, y=self.y - 1)
        if direction == direction.left:
            return Coordinates(x=self.x - 1, y=self.y)

    def get_direction(self, other: Coordinates) -> Direction | None:
        """
        Determine in which direction another adjacent pair of coordinates is.
        :returns:
            the direction (if adjacent) otherwise none
        """
        directions = {Coordinates(self.x, self.y + 1): Direction.up,
                      Coordinates(self.x, self.y - 1): Direction.down,
                      Coordinates(self.x - 1, self.y): Direction.left,
                      Coordinates(self.x + 1, self.y): Direction.right}

        if other in directions:
            return directions[other]
        else:
            return None


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


class Contour(frozenset[Coordinates]):
    """A contour made up of coordinates"""

    def __new__(cls, coordinates: Iterable[Coordinates], *args, **kwargs):
        return super(Contour, cls).__new__(cls, coordinates)

    def __init__(self, coordinates: Iterable[Coordinates]):
        super().__init__()

    @property
    def height(self) -> int:
        y = [coord.y for coord in self]
        return max(y) - min(y)

    @staticmethod
    def trace(cave: Cave) -> Contour:
        # To determine the contour of the top of the rubble we are going to
        # trace it by getting the coordinates of the topmost rock coordinates,
        # as only these can stop a falling rock...

        # tracing can be imagined like this (. free space, $ rock, x trace path)
        #
        # |.....|    |.....|    |.....|    |.....|
        # |$....|    |x....|    |x....|    |x....|
        # |$$..$|    |xx..$|    |xx..$|    |xx..x|
        # +-----+    +-x---+    +-xxxx+    +-xxxx+
        #    1          2          3          4
        # trace from top left to bottom (1-3) then up to top (4) - the path
        # marked by x's is then the contour.
        #

        # directions
        up = Direction.up
        right = Direction.right
        down = Direction.down
        left = Direction.left

        # order in which to move next depending on the last move direction
        # (sorted by priority)
        next_field: dict[Direction, list[Direction]] = {
            up: [left, up, right],
            right: [up, right, down],
            down: [right, down, left],
            left: [down, left, up]}

        # the rocks to trace
        rocks: list[list[bool]] = cave.rubble
        # stack with squares to investigate
        next_squares: list[Coordinates] = list()
        contour: list[Coordinates] = list()

        top: int = len(rocks) - 1
        right_cave_wall: int = len(rocks[0])
        contour_end: Coordinates

        # set contour start as the leftmost-topmost square with rock
        x = 0
        y = top
        while not rocks[y][x]:
            y -= 1
        next_squares.append(Coordinates(x=x, y=y))

        # set contour end as rightmost-topmost square with rock
        x = right_cave_wall - 1
        y = top
        while not rocks[y][x]:
            y -= 1
        contour_end = Coordinates(x=x, y=y)

        # tracing loop variables
        current_square: Coordinates
        current_direction: Direction

        # helper functions
        def get_adjacent_squares(square: Coordinates) -> list[Coordinates]:
            """Return rock-squares adjacent to the passed square"""
            nonlocal current_direction, next_field, top, right_cave_wall, rocks

            # all adjacent squares
            squares = [square.get_adjacent(direction)
                       for direction in next_field[current_direction]]
            # squares in cave and with rock
            squares = [s for s in squares
                       if 0 <= s.x < right_cave_wall and
                          0 <= s.y <= top and
                          rocks[s.y][s.x]]
            # return inverted to have the highest priority last
            return squares[::-1]

        def set_direction() -> Direction:
            """Determine the direction of movement we are currently in"""
            nonlocal current_square, contour
            if len(contour) < 1:
                return Direction.down
            direction = None
            idx = 1
            while direction is None and idx <= len(contour):
                direction = contour[-idx].get_direction(current_square)
                idx += 1
            return direction

        # trace the contour by always taking the square reaching into the void
        # of the cave
        #   |......x|   . empty square
        #   |x...xxx|   # rock square - NOT in contour
        #   |xxx...x|   x rock square IN contour
        #   |#x....x|
        #   |#xx.xxx|
        #   |##xxx##|
        #
        while next_squares[-1] != contour_end:
            current_square = next_squares.pop()
            # set direction we are moving in (determines choice of next squares)
            current_direction = set_direction()
            next_squares.extend(get_adjacent_squares(current_square))
            contour.append(current_square)

        contour.append(contour_end)

        # normalize the contour
        # (allow comparison irrespective of the height at which they occur)
        y_min = min([c.y for c in contour])
        contour_norm = [Coordinates(x=c.x, y=c.y - y_min) for c in contour]

        return Contour(contour_norm)


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
        self._n_rocks: int = 0
        self.rubble: list[list[bool]] = [[True] * Cave.WIDTH]

    @property
    def nr_rocks(self) -> int:
        """The number of rocks in the cave."""
        return self._n_rocks

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
            while not self._is_colliding(rock):
                self._move_rock_with_jet(rock)
                rock.move_down()
            # reached bottom
            rock.move_up()  # undo last move
            self._add_rock_to_rubble(rock)

    def _is_colliding(self, rock: Rock) -> bool:
        """
        Check if at least one point of the rock is colliding with the rubble
        already in the cave.
        """
        # Rock not even near the rocks already in the cave (no need to check)
        if rock.bottom > self.rock_pile_height:
            return False

        for sq in rock.squares():
            if sq.y <= self.rock_pile_height and self.rubble[sq.y][sq.x]:
                return True
        return False

    def _move_rock_with_jet(self, rock: Rock) -> None:
        """Attempt to move a Rock with a jet stream."""
        direction = next(self.jet)
        if direction == Direction.left and rock.left <= 0:
            return
        if direction == Direction.right and rock.right >= Cave.WIDTH - 1:
            return
        rock.move(direction)
        # check if move results in a collision (sideways)
        if self._is_colliding(rock):
            # move rock back
            rock.move(Direction.invert(direction))

    def _add_rock_to_rubble(self, rock: Rock) -> None:
        """
        Add the rock to the rubble pile in the cave.
        """
        while rock.top > self.rock_pile_height:
            self.rubble.append([False] * Cave.WIDTH)

        for sq in rock.squares():
            self.rubble[sq.y][sq.x] = True

        self._n_rocks += 1


class CaveState(NamedTuple):
    """State of the cave after rock_nr rocks have fallen into it."""
    rock_nr: int
    rock_pos: int
    jet_pos: int
    height: int
    contour: Contour

    @staticmethod
    def from_cave(cave: Cave) -> CaveState:
        contour: Contour = Contour.trace(cave)
        return CaveState(rock_nr=cave.nr_rocks,
                         rock_pos=cave.rock.current,
                         jet_pos=cave.jet.position,
                         height=cave.rock_pile_height,
                         contour=contour)

    def __hash__(self) -> int:
        return hash((self.rock_pos, self.jet_pos, hash(self.contour)))

    def __eq__(self, other) -> bool:
        if not isinstance(other, CaveState):
            return NotImplemented
        return (self.rock_pos == other.rock_pos
                and self.jet_pos == other.jet_pos
                and self.contour == other.contour)


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
        cave: Cave

        with input_data.open() as file:
            data = file.read().split("\n")
        jet_pattern = ''.join(data).strip()

        # PART 1
        print("Part 1:")
        cave = Cave(jet_pattern)
        cave.simulate_falling_rocks(2022)
        print(f"Height of the rubble after 2022 rocks: {cave.rock_pile_height}")

        # PART 2
        print("\nPart 2:")
        n = 1_000_000_000_000     # number of rocks to drop...
        cave = Cave(jet_pattern)  # new cave

        # Idea - Find repeat of the pattern.
        # Compare the contours of the cave after each new rock has come to rest.
        # if the following three factors match, we have found a loop:
        # 1) contour
        # 2) type of rock to be dropped next
        # 3) position in the jet pattern
        cave_states: dict[Contour: list[CaveState]] = dict()
        state: CaveState = CaveState.from_cave(cave)
        cave_states[state.contour] = [state]
        matching_states = []

        # find two matching states
        while len(matching_states) < 1:
            # drop a new rock
            cave.simulate_falling_rocks(1)
            state = CaveState.from_cave(cave)

            if state.contour not in cave_states:
                cave_states[state.contour] = [state]
            else:
                matching_states = [other_state
                                   for other_state in cave_states[state.contour]
                                   if other_state == state]
                cave_states[state.contour].append(state)

        # found a matching state
        match = matching_states[0]

        # height gain between states
        height_diff = state.height - match.height
        # number of rocks that were added in between states
        rock_diff = state.rock_nr - match.rock_nr
        # number of rounds (of dropping in rock_diff rocks) to approach n
        rounds = (n - match.rock_nr) // rock_diff
        # number of rocks in the cave after the rounds
        n_rocks_after_rounds = rounds * rock_diff + match.rock_nr
        # rocks missing to reach n rocks in cave
        missing_rocks = n - n_rocks_after_rounds
        height_after_rounds = rounds * height_diff + match.height

        # get the state of the cave after adding the missing rocks to the
        # matching cave where the loop starts
        def get_cave_state(rocks_of_state: int, states: Iterable[CaveState]) \
                -> CaveState:
            for s in states:
                if s.rock_nr == rocks_of_state:
                    return s

        cave_state_n: CaveState = get_cave_state(
            rocks_of_state=match.rock_nr + missing_rocks,
            states=chain(*cave_states.values())
        )

        # height added by the missing number of rocks
        height_from_rocks_after_loop = cave_state_n.height - match.height

        total_height = height_after_rounds + height_from_rocks_after_loop

        print(f"Simulated height of rubble after {n} rocks: {total_height}")
