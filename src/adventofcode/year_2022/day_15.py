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

        if start.x > end.x:
            start, end = end, start

        self._start = start
        self._end = end

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


class Dimension(Enum):
    UNSET = 0
    X = 1
    Y = 2

    
class Line1D(Line):
    """
    A line in a 1D subspace of a 2D coordinate system
    (the x or y dimension are fixed), and the line is parallel to either the
    x- or y-axis.
    """
    def __init__(self,
                 start: int,
                 end: int,
                 fixed_dimension_value: int,
                 fixed_dimension: Dimension = Dimension.Y):
        if end < start:
            start, end = end, start
        self._start_1d: int = start
        self._end_1d: int = end
        self._fixed_dimension_value: int = fixed_dimension_value
        self._fixed_dimension: Dimension = fixed_dimension

        super().__init__(start=self.to_line_coordinates(self.start_1d),
                         end=self.to_line_coordinates(self.end_1d))

    def __repr__(self) -> str:
        return f"{self.__class__}: ({self.fixed_dimension}=" \
               f"{self.fixed_dimension_value}) " \
               f"{self.start_1d} - {self.end_1d}"

    def __str__(self) -> str:
        return f"{self.start_1d} - {self.end_1d} " \
               f"({self.fixed_dimension}={self.fixed_dimension_value})"

    def __hash__(self) -> int:
        return hash((self.fixed_dimension_value, self.start_1d, self.end_1d))

    def __eq__(self, other):
        if not isinstance(other, Line1D):
            return NotImplemented
        return self.fixed_dimension == other.fixed_dimension \
               and self.fixed_dimension_value == other.fixed_dimension_value \
               and self.start_1d == other.start_1d \
               and self.end_1d == other.end_1d

    def __len__(self) -> int:
        return self.end_1d - self.start_1d

    @property
    def fixed_dimension(self) -> Dimension:
        return self._fixed_dimension

    @property
    def fixed_dimension_value(self) -> int:
        return self._fixed_dimension_value

    @property
    def start_1d(self) -> int:
        return self._start_1d

    @property
    def end_1d(self) -> int:
        return self._end_1d

    @staticmethod
    def from_coordinates(start: Coordinates, end: Coordinates) -> Line1D:
        """Return a Line1D when the coordinates describe one."""

        fixed_dimension: Dimension
        start_val: int
        end_val: int
        fixed_val: int

        if start.x != end.x and start.y != end.y:
            raise ValueError("Coordinates do not describe a 1 dimensional "
                             "line.")
        if start.x == end.x:
            fixed_dimension = Dimension.X
            fixed_val = start.x
            start_val = start.y
            end_val = end.y
        elif start.y == end.y:
            fixed_val = start.y
            fixed_dimension = Dimension.Y
            start_val = start.x
            end_val = end.x
        else:
            raise ValueError("Fixed dimension could not be determined.")

        return Line1D(start=start_val, end=end_val,
                      fixed_dimension_value=fixed_val,
                      fixed_dimension=fixed_dimension)

    @staticmethod
    def is_one_dimensional(line: Line) -> bool:
        """Check if a line is a straight line."""
        if line.start.x != line.end.x \
        and line.start.y != line.end.y:
            return False
        return True

    @staticmethod
    def from_line(line: Line) -> Line1D:
        """Cast a Line to a Line1D."""
        if not Line1D.is_one_dimensional(line):
            raise ValueError("Not a one dimensional line.")
        return Line1D.from_coordinates(line.start, line.end)

    def to_line_coordinates(self, value: int) -> Coordinates:
        """Add the fixed dimension value for a value on the line."""
        if self.start_1d > value > self.end_1d:
            raise ValueError("Value not on line.")

        fixed: int = self.fixed_dimension_value

        if self.fixed_dimension == Dimension.X:
            return Coordinates(x=fixed, y=value)
        elif self.fixed_dimension == Dimension.Y:
            return Coordinates(x=value, y=fixed)
        else:
            return NotImplemented

    def is_in_same_dim(self, other: Line1D) -> bool:
        """Are both lines in the same 1D subspace?"""
        if self.fixed_dimension == other.fixed_dimension \
                and self.fixed_dimension_value == other.fixed_dimension_value:
            return True
        else:
            return False

    def combinable(self, other: Line1D) -> bool:
        """
        Determine if this line and the other line could be combined into
        another line.

        :return:
            True if the lines have the same slope and overlap otherwise False.
        """

        if not self.is_in_same_dim(other):
            return False

        # check if the lines are overlapping

        # self left of other
        if self.start_1d <= other.start_1d:
            # if end also left of start they are not overlapping
            return self.end_1d >= other.start_1d

        # self right of other
        else:
            # if self.start right of other.end they are not overlapping
            return other.end_1d >= self.start_1d

    def combine(self, other: Line1D) -> Line1D:
        """Combine two lines into one."""
        if not self.combinable(other):
            raise ValueError("Lines can't be combined.")

        values = [self.start_1d, self.end_1d, other.start_1d, other.end_1d]

        return Line1D(start=min(values), end=max(values),
                      fixed_dimension_value=self.fixed_dimension_value,
                      fixed_dimension=self.fixed_dimension)

    def difference(self, other: Line1D) -> tuple[Line1D | None, ...]:
        """
        Return line parts that are covered by the other line but not the
        current line.
        :return:
            None      - if both lines are the same;
            one line  - if the other line is longer and the current line
                        overlaps at one end;
            two lines - if the other line is longer, and the current line is
                        in the middle.
        """
        # complete overlap
        if self == other:
            return None,
        # no overlap
        if not self.combinable(other):
            return other,
        # overlapping to certain degree
        line_left: Line1D | None = None
        line_right: Line1D | None = None
        fixed_dim = self.fixed_dimension
        fixed_val = self.fixed_dimension_value
        if other.start_1d < self.start_1d:
            line_left = Line1D(start=other.start_1d, end=self.start_1d-1,
                               fixed_dimension_value=fixed_val,
                               fixed_dimension=fixed_dim)
        if other.end_1d > self.end_1d:
            line_right = Line1D(start=self.end_1d+1, end=other.end_1d,
                                fixed_dimension_value=fixed_val,
                                fixed_dimension=fixed_dim)
        return line_left, line_right


class Line1DSet:
    """
    A set of lines that never contains any overlapping lines.

    If a line is being added that overlaps with any of the lines already in
    the LineSet, the lines will be merged.
    """

    def __init__(self,
                 fixed_dimension: Dimension,
                 fixed_dimension_value: int):
        self._fixed_dimension: Dimension = fixed_dimension
        self._fixed_dimension_value: int = fixed_dimension_value
        self._lines: list[Line1D] = list()

    def __iter__(self):
        return self._lines.__iter__()

    def __len__(self):
        return len(self._lines)

    def __str__(self):
        return str(self._lines)

    def __repr__(self):
        return repr(self._lines)

    @property
    def fixed_dimension(self) -> Dimension:
        return self._fixed_dimension

    @property
    def fixed_dimension_value(self) -> int:
        return self._fixed_dimension_value

    def add(self, line: Line) -> None:
        new_set: list[Line1D] = list()
        new_line: Line1D = Line1D.from_line(line)

        if not self._line_in_set_dim(new_line):
            # deal with the case of a line of length zero (point)
            if len(new_line) == 0 \
                    and new_line.start_1d == self.fixed_dimension_value:
                new_line = Line1D(start=new_line.fixed_dimension_value,
                                  end=new_line.fixed_dimension_value,
                                  fixed_dimension=self.fixed_dimension,
                                  fixed_dimension_value=new_line.start_1d)
            else:
                raise ValueError("Line not appropriate for current set.")

        # transfer lines left of new line
        while len(self._lines) > 0 \
                and self._lines[0].end_1d < new_line.start_1d:
            new_set.append(self._lines.pop(0))
        # combine combinable lines
        while len(self._lines) > 0 \
                and new_line.combinable(self._lines[0]):
            new_line = new_line.combine(self._lines.pop(0))
        new_set.append(new_line)
        # add remaining lines
        new_set.extend(self._lines)
        self._lines = new_set

    def difference(self, other: Line1DSet) -> Line1DSet:
        """
        Return a new Line1DSet that contains segments present in the other set
        and not the current set.
        """

        if not (self.fixed_dimension == other.fixed_dimension
                and self.fixed_dimension_value == other.fixed_dimension_value):
            raise ValueError("Only sets in the same subspace can be compared.")

        diff_set: Line1DSet = Line1DSet(
            fixed_dimension=self.fixed_dimension,
            fixed_dimension_value=self.fixed_dimension_value)
        next_segment: list[Line1D] = list(other)
        comp_lines: list[Line1D] = list(self)

        while len(next_segment) > 0 and len(comp_lines) > 0:
            c_line = comp_lines.pop(0)
            n_line = next_segment.pop(0)
            # diff
            left_part, right_part = c_line.difference(n_line)
            if left_part is not None:
                diff_set.add(left_part)
            if right_part is not None:
                next_segment.insert(0, right_part)
        for segment in next_segment:
            diff_set.add(segment)

        return diff_set

    def _line_in_set_dim(self, line: Line1D) -> bool:
        return self.fixed_dimension == line.fixed_dimension \
               and self.fixed_dimension_value == line.fixed_dimension_value


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
        line_x_exclusions: Line1DSet = Line1DSet(
            fixed_dimension=Dimension.Y,
            fixed_dimension_value=2_000_000)
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
        max_val: int = 4_000_000
        for row in range(0, max_val+1):
            whole_row = Line1DSet(fixed_dimension=Dimension.Y,
                                  fixed_dimension_value=row)
            whole_row.add(Line1D(start=0, end=max_val,
                                 fixed_dimension=Dimension.Y,
                                 fixed_dimension_value=row))
            row_exclusions = Line1DSet(fixed_dimension=Dimension.Y,
                                       fixed_dimension_value=row)
            for circ in exclusion_circles:
                line = circ.get_intersecting_line(y=row)
                if line is not None:
                    row_exclusions.add(line)

            not_excluded = row_exclusions.difference(whole_row)
            if len(not_excluded) > 0:
                print(f"Row {row}, not excluded: {not_excluded}")
                x = min([n.start_1d for n in not_excluded])
                y = not_excluded.fixed_dimension_value
                print(f"Tuning frequency: {x * max_val + y}")
                break
            else:
                if row % 100_000 == 0:
                    print(f"Up to row {row}, all excluded.")

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
