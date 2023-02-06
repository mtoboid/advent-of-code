"""
--- Day 14: Regolith Reservoir ---

The distress signal leads you to a giant waterfall! Actually, hang on - the
signal seems like it's coming from the waterfall itself, and that doesn't
make any sense. However, you do notice a little path that leads behind the
waterfall.

Correction: the distress signal leads you behind a giant waterfall! There
seems to be a large cave system here, and the signal definitely leads further
inside.

As you begin to make your way deeper underground, you feel the ground rumble
for a moment. Sand begins pouring into the cave! If you don't quickly figure
out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material
will come in handy here. You scan a two-dimensional vertical slice of the
cave above you (your puzzle input) and discover that it is mostly air with
structures made of rock.

Your scan traces the path of each solid rock structure and reports the x,
y coordinates that form the shape of the path, where x represents distance to
the right and y represents distance down. Each path appears as a single line
of text in your scan. After the first point of each path, each point
indicates the end of a straight horizontal or vertical line to be drawn from
the previous point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9

This scan means that there are two paths of rock; the first path consists of
two straight lines, and the second path consists of three straight lines. (
Specifically, the first path consists of a line of rock from 498,4 through
498,6 and another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:


  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.

Sand is produced one unit at a time, and the next unit of sand is not
produced until the previous unit of sand comes to rest. A unit of sand is
large enough to fill one tile of air in your scan.

A unit of sand always falls down one step if possible. If the tile
immediately below is blocked (by rock or sand), the unit of sand attempts to
instead move diagonally one step down and to the left. If that tile is
blocked, the unit of sand attempts to instead move diagonally one step down
and to the right. Sand keeps moving as long as it is able to do so, at each
step trying to move down, then down-left, then down-right. If all three
possible destinations are blocked, the unit of sand comes to rest and no
longer moves, at which point the next unit of sand is created back at the
source.

So, drawing sand that has come to rest as o, the first unit of sand simply
falls straight down and then stops:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.

The second unit of sand then falls straight down, lands on the first one,
and then comes to rest to its left:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.

After a total of five units of sand have come to rest, they form this pattern:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.

After a total of 22 units of sand:

......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.

Finally, only two more units of sand can possibly come to rest:

......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.

Once all 24 units of sand shown above have come to rest, all further sand
flows out the bottom, falling into the endless void. Just for fun, the path
any new sand takes before falling forever is shown here with ~:

.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........

Using your scan, simulate the falling sand. How many units of sand come to
rest before sand starts flowing into the abyss below?


--- Part Two ---

You realize you misread the scan. There isn't an endless void at the bottom
of the scan - there's floor, and you're standing on it!

You don't have time to scan the floor, so assume the floor is an infinite
horizontal line with a y coordinate equal to two plus the highest y
coordinate of any point in your scan.

In the example above, the highest y coordinate of any point is 9, and so the
floor is at y=11. (This is as if your scan contained one extra rock path like
-infinity,11 -> infinity,11.) With the added floor, the example above now
looks like this:

        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->

To find somewhere safe to stand, you'll need to simulate falling sand until a
unit of sand comes to rest at 500,0, blocking the source entirely and
stopping the flow of sand into the cave. In the example above, the situation
finally looks like this after 93 units of sand come to rest:

............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################

Using your scan, simulate the falling sand until the source of the sand
becomes blocked. How many units of sand come to rest?

"""
from __future__ import annotations

import numpy as np

from typing import NamedTuple

from adventofcode.challenge import DayChallenge, Path
from adventofcode.errors import AdventOfCodeError


class Coordinates(NamedTuple):
    x: int
    y: int

    @staticmethod
    def from_string(s: str) -> Coordinates:
        """Convert a string of the form <int>,<int> to coordinates"""
        coord: list[str] = s.strip().split(sep=",")
        if len(coord) != 2:
            raise ValueError("String not of appropriate format.")
        x: int = int(coord[0].strip())
        y: int = int(coord[1].strip())
        return Coordinates(x=x, y=y)

    @staticmethod
    def straight_line(from_: Coordinates, to_: Coordinates) \
            -> list[Coordinates]:
        """Create a line between two coordinates"""
        line: list[Coordinates]
        x_start: int = from_.x
        x_finish: int = to_.x
        y_start: int = from_.y
        y_finish: int = to_.y

        # determine the coordinate that is changing
        if x_start != x_finish and y_start != y_finish:
            raise NotImplemented("Both coordinates are changing")

        if x_start != x_finish:
            if x_finish < x_start:
                x_start, x_finish = x_finish, x_start
            line = [Coordinates(x, y_start) for x in
                    range(x_start, x_finish + 1)]
        elif y_start != y_finish:
            if y_finish < y_start:
                y_start, y_finish = y_finish, y_start
            line = [Coordinates(x_start, y) for y in
                    range(y_start, y_finish + 1)]
        else:
            line = [from_]

        return line


class Cave:
    class CaveSquare(NamedTuple):
        """A square in the cave"""
        occupied: bool
        sand: bool

    cave_square = np.dtype([("occupied", bool), ("sand", bool)])

    class SandGrainDroppedIntoVoid(AdventOfCodeError):
        """Raised when a grain dropped into the void"""

    def __init__(self, rows: int, columns: int,
                 sand_entry: Coordinates = Coordinates(x=500, y=0)):
        if sand_entry.x < 0 or sand_entry.x > columns \
        or sand_entry.y < 0 or sand_entry.y > rows:
            raise ValueError("Sand entry point not in cave.")

        self.rows: int = rows
        self.columns: int = columns
        self.sand_entry: Coordinates = sand_entry
        self.squares: np.ndarray[Cave.cave_square] = np.full(
            shape=(self.rows, self.columns),
            dtype=Cave.cave_square,
            fill_value=False
        )

    def __repr__(self) -> str:
        return self.squares.__repr__()

    def __str__(self) -> str:
        return '\n'.join([''.join([
                          'o' if sq['sand'] else
                          '#' if sq['occupied'] else
                          '.'
                          for sq in row])
                              for row in self.squares])

    @property
    def sand_grain_count(self) -> int:
        return self.squares['sand'].sum()

    def add_rock_path(self, from_: Coordinates, to_: Coordinates) -> None:
        """Draw a 'line' between the given coordinates (inclusive)"""
        line: list[Coordinates] = Coordinates.straight_line(from_, to_)
        x_coordinates = tuple(c.x for c in line)
        y_coordinates = tuple(c.y for c in line)
        self.squares["occupied"][y_coordinates, x_coordinates] = True

    def pour_one_grain_of_sand(self) -> bool:
        """
        Drop a grain of sand from the entry point.

        :returns:
            True - if the sand came to a rest and was 'added' to the cave.
            False - if the grain falls into the void.
        """

        pos: Coordinates = self.sand_entry
        next_pos: Coordinates = pos

        while next_pos is not None:
            pos = next_pos
            try:
                next_pos = self._can_travel(pos)
            except Cave.SandGrainDroppedIntoVoid:
                return False

        self.squares[pos.y, pos.x] = Cave.CaveSquare(occupied=True, sand=True)
        return True

    def _can_travel(self, grain: Coordinates) -> Coordinates | None:
        """
        Check if the grain can travel:
        1) straight-down, 2) left-down, 3) right-down

        :returns:
            The field the grain can travel to
        """

        # down
        # reached bottom
        if grain.y >= self.rows:
            raise Cave.SandGrainDroppedIntoVoid
        # drop down if square not occupied
        if not self.squares["occupied"][grain.y+1, grain.x]:
            return Coordinates(x=grain.x, y=grain.y+1)

        # left-down
        # reached left margin
        if grain.x <= 0:
            raise Cave.SandGrainDroppedIntoVoid
        # drop left if square free
        if not self.squares["occupied"][grain.y+1, grain.x-1]:
            return Coordinates(x=grain.x-1, y=grain.y+1)

        # right down
        # reached right margin
        if grain.x >= self.columns - 1:
            raise Cave.SandGrainDroppedIntoVoid
        # drop right if not occupied
        if not self.squares["occupied"][grain.y+1, grain.x+1]:
            return Coordinates(x=grain.x+1, y=grain.y+1)

        # No free square found
        return None


class Day14(DayChallenge):
    """Advent of Code 2022 day 14"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 14

    def run(self, input_data: Path) -> None:
        data: list[str]
        cave: Cave

        with input_data.open() as file:
            data = file.read().split("\n")

        # PART 1
        print("Part 1:")
        # create the cave
        min_max = Day14.max_min_of_input(data)
        cave = Cave(rows=min_max[3]+1,
                    columns=min_max[2]+1,
                    sand_entry=Coordinates(500, 0))
        # inner structure
        for line in data:
            if line:
                end_points = Day14.parse_input_line(line)
                for _from, _to in zip(end_points[:-1], end_points[1:]):
                    cave.add_rock_path(from_=_from, to_=_to)
        # pour sand grains
        while cave.pour_one_grain_of_sand():
            pass
        print(cave)
        print(f"\nFinal grain count in cave: {cave.sand_grain_count}")

        # PART 2
        print("\nPart 2:")

    @staticmethod
    def max_min_of_input(data: list[str]) -> tuple[int, int, int, int]:
        """
        Determine the max and min values for x and y.
        :return:
            (<min x>, <min y>, <max x>, <max y>)
        """
        x_vals: list[int] = list()
        y_vals: list[int] = list()
        pairs: list[str] = list()

        for line in data:
            pairs.extend([pair.strip() for pair in line.split("->") if pair])

        for pair in pairs:
            x, y = pair.split(",")
            x_vals.append(int(x))
            y_vals.append(int(y))

        return min(x_vals), min(y_vals), max(x_vals), max(y_vals)

    @staticmethod
    def parse_input_line(line: str) -> list[Coordinates]:
        end_points: list[Coordinates] = [
            Coordinates.from_string(c) for c in line.split("->")]
        return end_points
