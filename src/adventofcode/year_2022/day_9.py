"""
--- Day 9: Rope Bridge ---

This rope bridge creaks as you walk along it. You aren't sure how old it is,
or whether it can even support your weight.

It seems to support the Elves just fine, though. The bridge spans a gorge
which was carved out by the massive river far below you.

You step carefully; as you do, the ropes stretch and twist. You decide to
distract yourself by modeling rope physics; maybe you can even figure out
where not to step.

Consider a rope with a knot at each end; these knots mark the head and the
tail of the rope. If the head moves far enough away from the tail, the tail
is pulled toward the head.

Due to nebulous reasoning involving Planck lengths, you should be able to
model the positions of the knots on a two-dimensional grid. Then,
by following a hypothetical series of motions (your puzzle input) for the
head, you can determine how the tail will move.

Due to the aforementioned Planck lengths, the rope must be quite short; in
fact, the head (H) and tail (T) must always be touching (diagonally adjacent
and even overlapping both count as touching):

....
.TH.
....

....
.H..
..T.
....

...
.H. (H covers T)
...

If the head is ever two steps directly up, down, left, or right from the
tail, the tail must also move one step in that direction so it remains close
enough:

.....    .....    .....
.TH.. -> .T.H. -> ..TH.
.....    .....    .....

...    ...    ...
.T.    .T.    ...
.H. -> ... -> .T.
...    .H.    .H.
...    ...    ...

Otherwise, if the head and tail aren't touching and aren't in the same row or
column, the tail always moves one step diagonally to keep up:

.....    .....    .....
.....    ..H..    ..H..
..H.. -> ..... -> ..T..
.T...    .T...    .....
.....    .....    .....

.....    .....    .....
.....    .....    .....
..H.. -> ...H. -> ..TH.
.T...    .T...    .....
.....    .....    .....

You just need to work out where the tail goes as the head follows a series of
motions. Assume the head and the tail both start at the same position,
overlapping.

For example:

R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2

This series of motions moves the head right four steps, then up four steps,
then left three steps, then down one step, and so on. After each step,
you'll need to update the position of the tail if the step means the head is
no longer adjacent to the tail. Visually, these motions occur as follows (s
marks the starting position as a reference point):

== Initial State ==

......
......
......
......
H.....  (H covers T, s)

== R 4 ==

......
......
......
......
TH....  (T covers s)

......
......
......
......
sTH...

......
......
......
......
s.TH..

......
......
......
......
s..TH.

== U 4 ==

......
......
......
....H.
s..T..

......
......
....H.
....T.
s.....

......
....H.
....T.
......
s.....

....H.
....T.
......
......
s.....

== L 3 ==

...H..
....T.
......
......
s.....

..HT..
......
......
......
s.....

.HT...
......
......
......
s.....

== D 1 ==

..T...
.H....
......
......
s.....

== R 4 ==

..T...
..H...
......
......
s.....

..T...
...H..
......
......
s.....

......
...TH.
......
......
s.....

......
....TH
......
......
s.....

== D 1 ==

......
....T.
.....H
......
s.....

== L 5 ==

......
....T.
....H.
......
s.....

......
....T.
...H..
......
s.....

......
......
..HT..
......
s.....

......
......
.HT...
......
s.....

......
......
HT....
......
s.....

== R 2 ==

......
......
.H....  (H covers T)
......
s.....

......
......
.TH...
......
s.....

After simulating the rope, you can count up all of the positions the tail
visited at least once. In this diagram, s again marks the starting position (
which the tail also visited) and # marks other positions the tail visited:

..##..
...##.
.####.
....#.
s###..

So, there are 13 positions the tail visited at least once.

Simulate your complete hypothetical series of motions. How many positions
does the tail of the rope visit at least once?

"""

from enum import Enum

from adventofcode.challenge import DayChallenge, Path


class Move(Enum):
    UP = (0, "U")
    RIGHT = (1, "R")
    DOWN = (2, "D")
    LEFT = (3, "L")

    @staticmethod
    def from_string(s: str) -> 'Move':
        """Generate a move from a string"""
        m = s.upper()
        if "UP".startswith(m):
            return Move.UP
        elif "RIGHT".startswith(m):
            return Move.RIGHT
        elif "DOWN".startswith(m):
            return Move.DOWN
        elif "LEFT".startswith(m):
            return Move.LEFT
        else:
            raise ValueError(f"No move direction corresponds to '{s}'.")


class Position:
    """A position in 2D space with x, y coordinates."""

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def __hash__(self):
        return self.x * 977 + self.y * 13

    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return self.__str__()

    def __copy__(self) -> 'Position':
        return Position(self.x, self.y)

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y


class RopeHead:
    """The head (start) of a rope."""
    def __init__(self):
        self._position: Position = Position(0, 0)

    @property
    def position(self) -> Position:
        return self._position

    """The head of a rope that can be moved around."""
    def move_left(self) -> None:
        """Move left one step."""
        self._position = Position(self.position.x - 1, self.position.y)

    def move_right(self) -> None:
        """Move right one step."""
        self._position = Position(self.position.x + 1, self.position.y)

    def move_up(self) -> None:
        """Move up one step."""
        self._position = Position(self.position.x, self.position.y - 1)

    def move_down(self) -> None:
        """Move down one step."""
        self._position = Position(self.position.x, self.position.y + 1)

    def move(self, direction: Move) -> None:
        if direction == Move.UP:
            self.move_up()
        if direction == Move.RIGHT:
            self.move_right()
        if direction == Move.DOWN:
            self.move_down()
        if direction == Move.LEFT:
            self.move_left()


class RopeTail:
    """The tail of a rope that moves after the head."""
    def __init__(self, head: RopeHead):
        self._head: RopeHead
        self._position: Position
        self._head = head
        self._position = head.position

    @property
    def position(self) -> Position:
        return self._position

    def move(self) -> None:
        """Move the tail towards the position of the head."""
        if self.is_touching():
            return
        tail = self.position
        head = self._head.position
        delta_x = RopeTail._as_unit(head.x - tail.x)
        delta_y = RopeTail._as_unit(head.y - tail.y)
        # move left-right
        self._position = Position(self.position.x + delta_x,
                                  self.position.y + delta_y)

    def is_touching(self) -> bool:
        tail = self.position
        head = self._head.position
        """Is the tail on top or just next to the head?"""
        delta_x = abs(tail.x - head.x)
        delta_y = abs(tail.y - head.y)
        return delta_x <= 1 and delta_y <= 1

    @staticmethod
    def _as_unit(number: int) -> int:
        """Convert an integer to one leaving the sign untouched."""
        if number < 0:
            return -1
        elif number > 0:
            return 1
        else:
            return 0


class Rope:
    """A rope with two ends a head and a tail."""
    def __init__(self):
        self.head: RopeHead = RopeHead()
        self.tail: RopeTail = RopeTail(self.head)
        self.tail_positions: set[Position] = set()
        self.tail_positions.add(self.tail.position)

    def move(self, direction: Move, amount: int):
        """Move the rope head a certain amount right."""
        for i in range(amount):
            self.head.move(direction)
            self.tail.move()
            self.tail_positions.add(self.tail.position)


class Day9(DayChallenge):
    """Advent of Code 2022 day 9"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 9

    def run(self, input_data: Path) -> None:
        data: list[str]

        with input_data.open() as file:
            data = file.read().split("\n")

        # PART 1
        print("Part 1:")
        rope: Rope = Rope()

        for action in data:
            if not action == '':
                move, amount = Day9.instruction_to_move(action)
                rope.move(move, amount)

        print(f"unique rope tail positions: {len(rope.tail_positions)}")

        # PART 2
        print("\nPart 2:")

    @staticmethod
    def instruction_to_move(line: str) -> tuple[Move, int]:
        """Parse a string instruction to move a rope"""
        parts = line.split()
        m: Move = Move.from_string(parts[0])
        a: int = int(parts[1])
        return m, a
