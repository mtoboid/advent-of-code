"""
--- Day 18: Boiling Boulders ---

You and the elephants finally reach fresh air. You've emerged near the base
of a large volcano that seems to be actively erupting! Fortunately, the lava
seems to be flowing away from you and toward the ocean.

Bits of lava are still being ejected toward you, so you're sheltering in the
cavern exit a little longer. Outside the cave, you can see the lava landing
in a pond and hear it loudly hissing as it solidifies.

Depending on the specific compounds in the lava and speed at which it cools,
it might be forming obsidian! The cooling rate should be based on the surface
area of the lava droplets, so you take a quick scan of a droplet as it flies
past you (your puzzle input).

Because of how quickly the lava is moving, the scan isn't very good; its
resolution is quite low and, as a result, it approximates the shape of the
lava droplet with 1x1x1 cubes on a 3D grid, each given as its x,y,z position.

To approximate the surface area, count the number of sides of each cube that
are not immediately connected to another cube. So, if your scan were only two
adjacent cubes like 1,1,1 and 2,1,1, each cube would have a single side
covered and five sides exposed, a total surface area of 10 sides.

Here's a larger example:

2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5

In the above example, after counting up all the sides that aren't connected
to another cube, the total surface area is 64.

What is the surface area of your scanned lava droplet?

--- Part Two ---

Something seems off about your calculation. The cooling rate depends on
exterior surface area, but your calculation also included the surface area of
air pockets trapped in the lava droplet.

Instead, consider only cube sides that could be reached by the water and
steam as the lava droplet tumbles into the pond. The steam will expand to
reach as much as possible, completely displacing any air on the outside of
the lava droplet but never expanding diagonally.

In the larger example above, exactly one cube of air is trapped within the
lava droplet (at 2,2,5), so the exterior surface area of the lava droplet is 58.

What is the exterior surface area of your scanned lava droplet?

"""

from __future__ import annotations

import numpy as np

from itertools import permutations
from typing import Iterable, NamedTuple

from adventofcode.challenge import DayChallenge, Path


class Coordinates3D(NamedTuple):
    x: int
    y: int
    z: int

    @staticmethod
    def from_string(s: str) -> Coordinates3D:
        """Convert a string of the form x,y,z into Coordinates3D."""
        x, y, z = map(int, s.strip().split(","))
        return Coordinates3D(x=x, y=y, z=z)


class Scan3D:
    """A 3D scan of a lava droplet"""

    class Matrix3D:
        """
        A wrapped np.ndarray (x, y, z) in which fields can be accessed with a
        Coordinate3D.
        """
        # set describing a step in each axis direction + and -
        ADJACENT: frozenset[tuple[int, int, int]] = frozenset(
            [*permutations((0, 0, 1)), *permutations((0, 0, -1))]
        )

        def __init__(self, shape: tuple[int, int, int]):
            self.array: np.ndarray[bool]
            self.array = np.full(shape=shape, dtype=bool, fill_value=False)

        def get(self, field: Coordinates3D) -> bool:
            return self.array[field.x, field.y, field.z]

        def set(self, field: Coordinates3D, value: bool) -> None:
            self.array[field.x, field.y, field.z] = value

        def get_neighbors(self, field: Coordinates3D) -> list[Coordinates3D]:
            """Get matrix neighbors of the specified field"""
            adjacent = Scan3D.Matrix3D.ADJACENT
            x_max = self.array.shape[0] - 1
            y_max = self.array.shape[1] - 1
            z_max = self.array.shape[2] - 1

            neighbors = [Coordinates3D(x=field.x + a[0],
                                       y=field.y + a[1],
                                       z=field.z + a[2]) for a in adjacent]
            # filter out squares outside the matrix
            neighbors = [n for n in neighbors
                         if 0 <= n.x <= x_max and
                            0 <= n.y <= y_max and
                            0 <= n.z <= z_max]
            return neighbors

    class Cube:
        """A 1x1x1 cube in the matrix"""
        def __init__(self, x: int, y: int, z: int):
            # coordinates of the cube in the matrix
            self.coordinates: Coordinates3D = Coordinates3D(x, y, z)
            # faces of the cube that are in contact with the same cube type
            # (matter for matter-cubes, empty for empty-cubes)
            self.contact_faces: int = 0

        def __hash__(self):
            return hash(self.coordinates)

        def __eq__(self, other):
            if not isinstance(other, Scan3D.Cube):
                return NotImplemented
            return self.coordinates == other.coordinates

        @staticmethod
        def from_coordinates3d(c: Coordinates3D) -> Scan3D.Cube:
            return Scan3D.Cube(x=c.x, y=c.y, z=c.z)

    def __init__(self, scan_data: Iterable[Coordinates3D]):
        # Boolean 3D array that represents the scan data for each coordinate
        # (True means lava/matter, False means an empty cube)
        self.matrix: Scan3D.Matrix3D
        # All the cubes that contain matter
        self.matter: frozenset[Scan3D.Cube]
        # All the empty cubes that are outside the matter (surrounding)
        self.outer_shell: frozenset[Scan3D.Cube]

        self.matrix = Scan3D._generate_matter_matrix(scan_data)
        self.matter = Scan3D._perform_matter_scan(matrix=self.matrix)
        self.outer_shell = Scan3D._perform_outer_shell_scan(matrix=self.matrix)

    @staticmethod
    def _generate_matter_matrix(data: Iterable[Coordinates3D]) \
            -> Scan3D.Matrix3D:
        """
        Generate a boolean 3D matrix holding the data for all cubes; True in
        the matrix means this cube contains matter.
        """
        max_x = max([c.x for c in data])
        max_y = max([c.y for c in data])
        max_z = max([c.z for c in data])
        # generate the matrix with a 'padding' of one (sub)cube of space (False)
        # on all sides, adjust the coordinates accordingly
        # shape +2 for padding +1 as input data are indices = +3
        matrix: Scan3D.Matrix3D = Scan3D.Matrix3D(
            shape=(max_x+3, max_y+3, max_z+3))
        # mark all 'matter' (sub)cubes with True
        # !also shift them by +1 in all dimensions to account for the padding
        for cube in data:
            matrix.array[cube.x+1, cube.y+1, cube.z+1] = True
        return matrix

    @staticmethod
    def _perform_matter_scan(matrix: Scan3D.Matrix3D) \
            -> frozenset[Scan3D.Cube]:
        """
        Scan the whole matrix identifying all matter cubes and counting their
        neighbors.
        """
        matter = True
        m = matrix.array
        matter_cubes: set[Scan3D.Cube] = set()

        # function to determine the number of faces in contact with another
        # matter-cube
        def calc_contact_faces(_cube: Scan3D.Cube) -> int:
            nonlocal matrix
            neighbors = matrix.get_neighbors(_cube.coordinates)
            return sum([1 for n in neighbors if matrix.get(n)])

        for x in range(m.shape[0]):
            for y in range(m.shape[1]):
                for z in range(m.shape[2]):
                    if m[x, y, z] == matter:
                        cube: Scan3D.Cube = Scan3D.Cube(x=x, y=y, z=z)
                        cube.contact_faces = calc_contact_faces(cube)
                        matter_cubes.add(cube)

        return frozenset(matter_cubes)

    @staticmethod
    def _perform_outer_shell_scan(matrix: Scan3D.Matrix3D) \
            -> frozenset[Scan3D.Cube]:
        """
        Perform a walk around the matrix to identify all empty cubes that are
        outside (surrounding) the matter, and count their (empty) neighbors
        """
        empty = False
        outer_shell_cubes: dict[Coordinates3D, Scan3D.Cube] = dict()
        # the matrix is padded, so we know the cube (0, 0, 0) is empty
        unvisited_coordinates: set[Coordinates3D] = {Coordinates3D(0, 0, 0)}

        # helper function to determine the number of faces in contact with
        # another empty-cube, or are at the extremes of the matrix
        # (count cubes as outside the matrix as empty neighbors!)
        def calc_contact_faces() -> int:
            nonlocal matrix, empty, neighbors
            contact_faces = 0
            # when neighboring cubes are missing these are outside the matrix
            contact_faces += 6 - len(neighbors)
            contact_faces += sum([1 for nb in neighbors
                                  if matrix.get(nb) == empty])
            return contact_faces

        while len(unvisited_coordinates) > 0:
            current_coordinates = unvisited_coordinates.pop()
            neighbors = matrix.get_neighbors(current_coordinates)
            # add un-visited (empty) cubes to the stack
            for n in neighbors:
                if matrix.get(n) == empty \
                        and n not in outer_shell_cubes:
                    unvisited_coordinates.add(n)
            # process current cube
            if matrix.get(current_coordinates) == empty:
                cube = Scan3D.Cube.from_coordinates3d(current_coordinates)
                cube.contact_faces = calc_contact_faces()
                outer_shell_cubes[cube.coordinates] = cube

        return frozenset(outer_shell_cubes.values())


class Day18(DayChallenge):
    """Advent of Code 2022 day 18"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 18

    def run(self, input_data: Path) -> None:
        data: list[str]

        with input_data.open() as file:
            data = file.read().split("\n")

        coordinates = [Coordinates3D.from_string(line)
                       for line in data if line]

        scan = Scan3D(coordinates)

        # PART 1
        print("Part 1:")
        surface_area = sum([6 - cube.contact_faces for cube in scan.matter])
        print(f"surface area: {surface_area}")
        #
        # # PART 2
        print("\nPart 2:")
        exterior_surface_area = sum([6 - cube.contact_faces
                                     for cube in scan.outer_shell])
        print(f"outer surface area: {exterior_surface_area}")
