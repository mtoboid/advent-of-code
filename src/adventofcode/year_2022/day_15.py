"""
--- Day 15: Beacon Exclusion Zone ---

You feel the ground rumble again as the distress signal leads you to a large
network of subterranean tunnels. You don't have time to search them all,
but you don't need to: your pack contains a set of deployable sensors that
you imagine were originally built to locate lost Elves.

The sensors aren't very powerful, but that's okay; your handheld device
indicates that you're close enough to the source of the distress signal to
use them. You pull the emergency sensor system out of your pack, hit the big
button on top, and the sensors zoom off down the tunnels.

Once a sensor finds a spot it thinks will give it a good reading, it attaches
itself to a hard surface and begins monitoring for the nearest signal source
beacon. Sensors and beacons always exist at integer coordinates. Each sensor
knows its own position and can determine the position of a beacon precisely;
however, sensors can only lock on to the one beacon closest to the sensor as
measured by the Manhattan distance. (There is never a tie where two beacons
are the same distance to a sensor.)

It doesn't take long for the sensors to report back their positions and
closest beacons (your puzzle input). For example:

Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3

So, consider the sensor at 2,18; the closest beacon to it is at -2,15. For
the sensor at 9,16, the closest beacon to it is at 10,16.

Drawing sensors as S and beacons as B, the above arrangement of sensors and
beacons looks like this:

               1    1    2    2
     0    5    0    5    0    5
 0 ....S.......................
 1 ......................S.....
 2 ...............S............
 3 ................SB..........
 4 ............................
 5 ............................
 6 ............................
 7 ..........S.......S.........
 8 ............................
 9 ............................
10 ....B.......................
11 ..S.........................
12 ............................
13 ............................
14 ..............S.......S.....
15 B...........................
16 ...........SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....

This isn't necessarily a comprehensive map of all beacons in the area,
though. Because each sensor only identifies its closest beacon, if a sensor
detects a beacon, you know there are no other beacons that close or closer to
that sensor. There could still be beacons that just happen to not be the
closest beacon to any sensor. Consider the sensor at 8,7:

               1    1    2    2
     0    5    0    5    0    5
-2 ..........#.................
-1 .........###................
 0 ....S...#####...............
 1 .......#######........S.....
 2 ......#########S............
 3 .....###########SB..........
 4 ....#############...........
 5 ...###############..........
 6 ..#################.........
 7 .#########S#######S#........
 8 ..#################.........
 9 ...###############..........
10 ....B############...........
11 ..S..###########............
12 ......#########.............
13 .......#######..............
14 ........#####.S.......S.....
15 B........###................
16 ..........#SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....

This sensor's closest beacon is at 2,10, and so you know there are no beacons
that close or closer (in any positions marked #).

None of the detected beacons seem to be producing the distress signal,
so you'll need to work out where the distress beacon is by working out where
it isn't. For now, keep things simple by counting the positions where a
beacon cannot possibly be along just a single row.

So, suppose you have an arrangement of beacons and sensors like in the
example above and, just in the row where y=10, you'd like to count the number
of positions a beacon cannot possibly exist. The coverage from all sensors
near that row looks like this:

                 1    1    2    2
       0    5    0    5    0    5
 9 ...#########################...
10 ..####B######################..
11 .###S#############.###########.

In this example, in the row where y=10, there are 26 positions where a beacon
cannot be present.

Consult the report from the sensors you just deployed. In the row where
y=2000000, how many positions cannot contain a beacon?


--- Part Two ---

Your handheld device indicates that the distress signal is coming from a
beacon nearby. The distress beacon is not detected by any sensor, but the
distress beacon must have x and y coordinates each no lower than 0 and no
larger than 4000000.

To isolate the distress beacon's signal, you need to determine its tuning
frequency, which can be found by multiplying its x coordinate by 4000000 and
then adding its y coordinate.

In the example above, the search space is smaller: instead, the x and y
coordinates can each be at most 20. With this reduced search area, there is
only a single position that could have a beacon: x=14, y=11. The tuning
frequency for this distress beacon is 56000011.

Find the only possible position for the distress beacon. What is its tuning
frequency?

"""
from __future__ import annotations

from enum import Enum
from fractions import Fraction
from re import compile, Match, Pattern
from typing import NamedTuple, Callable

from adventofcode.challenge import DayChallenge, Path


class Coordinates(NamedTuple):
    x: int
    y: int

    @staticmethod
    def manhattan_dist(a: Coordinates, b: Coordinates) -> int:
        """Calculate the manhattan distance between a and b."""
        diff_x: int = abs(a.x - b.x)
        diff_y: int = abs(a.y - b.y)
        return diff_x + diff_y


class Line:
    """A line between two coordinates."""

    def __init__(self, start: Coordinates, end: Coordinates):
        self._start: Coordinates
        self._end: Coordinates
        self._slope: Fraction

        if start.x > end.x:
            start, end = end, start

        self._start = start
        self._end = end
        self._slope = Fraction(end.y - start.y, end.x - start.x)

    def __len__(self) -> int:
        return Coordinates.manhattan_dist(self.start, self.end)

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Line):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    @property
    def start(self) -> Coordinates:
        return self._start

    @property
    def end(self) -> Coordinates:
        return self._end

    @property
    def slope(self) -> Fraction:
        return self._slope


class Dimension(Enum):
    X = 1
    Y = 2

    
class StraightLine(Line):
    """
    A straight line where x or y stay the same.
    """
    def __init__(self, start: Coordinates, end: Coordinates):
        self._fixed_dimension: Dimension
        
        if start.x != end.x and start.y != end.y:
            raise ValueError("Coordinates do not describe a straight line.")
        if start.x == end.x:
            self._fixed_dimension = Dimension.X
        elif start.y == end.y:
            self._fixed_dimension = Dimension.Y
        else:
            raise ValueError("Fixed dimension could not be set.")
        super().__init__(start=start, end=end)

    @property
    def fixed_dimension(self) -> Dimension:
        return self._fixed_dimension

    @staticmethod
    def is_straight(line: Line) -> bool:
        """Check if a line is a straight line."""
        if line.start.x != line.end.x \
        and line.start.y != line.end.y:
            return False
        return True

    @staticmethod
    def to_straight_line(line: Line) -> StraightLine:
        """Cast a Line to a StraightLine."""
        if not StraightLine.is_straight(line):
            raise ValueError("Not a straight line.")
        return StraightLine(line.start, line.end)

    def combinable(self, other: StraightLine) -> bool:
        """
        Determine if this line and the other line could be combined into
        another line.

        :return:
            True if the lines have the same slope and overlap otherwise False.
        """

        get_flexible_dim: Callable[[Coordinates], int]

        if self.fixed_dimension != other.fixed_dimension:
            return False
        if self.fixed_dimension == Dimension.X:
            if self.start.x != other.start.x:
                return False

            def get_flexible_dim(coord: Coordinates) -> int:
                return coord.y

        elif self.fixed_dimension == Dimension.Y:
            if self.start.y != other.start.y:
                return False

            def get_flexible_dim(coord: Coordinates) -> int:
                return coord.x
        else:
            return False

        a1: int = get_flexible_dim(self.start)
        a2: int = get_flexible_dim(self.end)
        if a1 > a2:
            a1, a2 = a2, a1
        b1: int = get_flexible_dim(other.start)
        b2: int = get_flexible_dim(other.end)
        if b1 > b2:
            b1, b2 = b2, b1

        # line b right of a (a2 on b?)
        if a1 <= b1:
            return b1 <= a2
        # line b left of a
        else:
            return a1 <= b2

    def combine(self, other: StraightLine) -> StraightLine:
        """Combine two lines into one."""
        if not self.combinable(other):
            raise ValueError("Lines can't be combined.")
        coordinates = (self.start, self.end, other.start, other.end)
        x = [c.x for c in coordinates]
        y = [c.y for c in coordinates]
        return StraightLine(Coordinates(x=min(x), y=min(y)),
                            Coordinates(x=max(x), y=max(y)))


class StraightLineSet:
    """
    A set of lines that never contains any overlapping lines.

    If a line is being added that overlaps with any of the lines already in
    the LineSet, the lines will be merged.
    """

    def __init__(self):
        self._lines: list[StraightLine] = list()

    def __iter__(self):
        return self._lines.__iter__()

    def __len__(self):
        return len(self._lines)

    def __str__(self):
        return str(self._lines)

    def __repr__(self):
        return repr(self._lines)

    def add(self, line: Line) -> None:
        new_set: list[StraightLine] = list()
        new_line: StraightLine = StraightLine.to_straight_line(line)
        for ln in self._lines:
            if ln.combinable(new_line):
                new_line = new_line.combine(ln)
            else:
                new_set.append(ln)
        new_set.append(new_line)
        self._lines = new_set


class ManhattanCircle:
    """A 'circle' in the universe of manhattan distance."""

    def __init__(self, center: Coordinates, radius: int):
        self.center: Coordinates
        self._radius: int = 0

        self.center = center
        self.radius = radius

    @property
    def radius(self) -> int:
        return self._radius

    @radius.setter
    def radius(self, value) -> None:
        if value < 0:
            raise ValueError("A negative radius is not supported.")
        self._radius = value

    def get_intersecting_line(self, y: int) -> Line | None:
        """
        Get the part of a straight line (y does not change) inside the
        circle that intersects at the given y.
        :returns:
            A line, or None if no intersecting line exists.
        """

        y_diff: int = abs(self.center.y - y)

        if y_diff > self.radius:
            return None
        x_left: int = self.center.x - (self.radius - y_diff)
        x_right: int = self.center.x + (self.radius - y_diff)
        return Line(Coordinates(x=x_left, y=y), Coordinates(x=x_right, y=y))


class Day15(DayChallenge):
    """Advent of Code 2022 day 15"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 15

    def run(self, input_data: Path) -> None:
        data: list[str]
        sensor_beacon_pairs: list[tuple[Coordinates, Coordinates]]
        min_x: int
        min_y: int
        max_x: int
        max_y: int

        with input_data.open() as file:
            data = file.read().split("\n")

        # PART 1
        print("Part 1:")
        # pairs
        sensor_beacon_pairs: list[tuple[Coordinates, Coordinates]] = [
            Day15.parse_input_line(line) for line in data if line]
        # min max values
        min_x, min_y, max_x, max_y = Day15.min_max(
            [c for pair in sensor_beacon_pairs for c in pair])
        # exclusion zones
        exclusion_circles: list[ManhattanCircle] = [
            ManhattanCircle(center=pair[0],
                            radius=Coordinates.manhattan_dist(pair[0], pair[1]))
            for pair in sensor_beacon_pairs
        ]
        # only on line y=2_000_000
        line_x_exclusions: StraightLineSet = StraightLineSet()
        for circ in exclusion_circles:
            line = circ.get_intersecting_line(y=2_000_000)
            if line is not None:
                line_x_exclusions.add(line)
        # excluded
        no_beacon: int = sum([len(line) for line in line_x_exclusions])

        print(f"min x: {min_x}, min y: {min_y}, max x: {max_x}, max y: {max_y}")
        print(f"excluded on line 2_000_000: {no_beacon}")

        # PART 2
        print("\nPart 2:")

    @staticmethod
    def parse_input_line(line: str) -> tuple[Coordinates, Coordinates]:
        """
        Parse a line of input to obtain the sensor and beacon coordinates
        :return:
            tuple(<sensor coordinates>, <beacon coordinates>)
        """

        regex: Pattern = compile(
            r"Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+):\s*"
            r"closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)"
        )

        m: Match = regex.match(line)
        if m is None:
            raise ValueError("Input line could not be matched!")

        return (Coordinates(x=int(m.group('sensor_x')),
                            y=int(m.group('sensor_y'))),
                Coordinates(x=int(m.group('beacon_x')),
                            y=int(m.group('beacon_y'))))

    @staticmethod
    def min_max(coordinates: list[Coordinates]) -> tuple[int, int, int, int]:
        """
        Find the minimums and maximums for a list of coordinates.
        :return:
            tuple(<min_x>, <min_y>, <max_x>, <max_y>)
        """
        xs = [cord.x for cord in coordinates]
        ys = [cord.y for cord in coordinates]

        return min(xs), min(ys), max(xs), max(ys)
