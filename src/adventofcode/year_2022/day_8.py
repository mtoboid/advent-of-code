"""
--- Day 8: Treetop Tree House ---

The expedition comes across a peculiar patch of tall trees all planted
carefully in a grid. The Elves explain that a previous expedition planted
these trees as a reforestation effort. Now, they're curious if this would be
a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house
hidden. To do this, you need to count the number of trees that are visible
from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the
height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390

Each tree is represented as a single digit whose value is its height, where 0
is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the
grid are shorter than it. Only consider trees in the same row or column; that
is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are
already on the edge, there are no trees to block the view. In this example,
that only leaves the interior nine trees to consider:

    The top-left 5 is visible from the left and top. (It isn't visible from
    the right or bottom since other trees of height 5 are in the way.)

    The top-middle 5 is visible from the top and right.

    The top-right 1 is not visible from any direction; for it to be visible,
    there would need to only be trees of height 0 between it and an edge.

    The left-middle 5 is visible, but only from the right.

    The center 3 is not visible from any direction; for it to be visible,
    there would need to be only trees of at most height 2 between it and an
    edge.

    The right-middle 3 is visible from the right.

    In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

With 16 trees visible on the edge and another 5 visible in the interior,
a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?

"""
import numpy as np

from collections.abc import Sequence

from adventofcode.challenge import DayChallenge, Path


class TreeGrid:
    def __init__(self, tree_heights: list[list[int]]):
        self._tree_height: np.ndarray
        self._visible: np.ndarray

        self._tree_height = np.array(tree_heights, dtype=int)
        self._visible = TreeGrid.gen_visibility_grid(self._tree_height)

    def __str__(self):
        return self._tree_height.__str__()

    @property
    def tree_height(self) -> np.ndarray:
        """Return the grid of tree heights in the forrest."""
        out = self._tree_height.copy()
        return out

    @property
    def visible(self) -> np.ndarray:
        """
        Return a boolean grid indicating visibility from the outside of all
        trees in the forrest.
        """
        out = self._visible
        return out

    @staticmethod
    def gen_visibility_grid(trees: np.ndarray) -> np.ndarray:
        """
        Generate a boolean grid of the same shape as _trees indicating
        visibility of each tree from outside the grid.
        """
        # mark trees visible from north(n), east(e), south(s) and west(w)
        vis_n: np.ndarray = np.full(shape=trees.shape, dtype=bool,
                                    fill_value=False)
        vis_e: np.ndarray = np.full(shape=trees.shape, dtype=bool,
                                    fill_value=False)
        vis_s: np.ndarray = np.full(shape=trees.shape, dtype=bool,
                                    fill_value=False)
        vis_w: np.ndarray = np.full(shape=trees.shape, dtype=bool,
                                    fill_value=False)
        # North (columns of trees)
        vis_n = np.array([TreeGrid._visibility(x) for x in trees.T]).T
        # East (inverted rows of trees)
        vis_e = np.array([TreeGrid._visibility(x) for x in trees[:,::-1]])[:,::-1]
        # South (inverted columns of trees)
        vis_s = np.array([TreeGrid._visibility(x) for x in trees[::-1,:].T]
                         ).T[::-1,:]
        # West (rows of trees)
        vis_w = np.array([TreeGrid._visibility(x) for x in trees])

        vis_any = vis_n | vis_e | vis_s | vis_w
        return vis_any

    @staticmethod
    def _visibility(trees: Sequence[int]) -> np.ndarray:
        """
        Return a boolean array indicating which tres in the row are visible.
        """
        vis: list[bool]
        tallest: int
        vis = [False]*len(trees)
        vis[0] = True
        tallest = trees[0]
        for i in range(len(trees)):
            if trees[i] > tallest:
                vis[i] = True
                tallest = trees[i]
        return np.array(vis, dtype=bool)


class Day8(DayChallenge):
    """Advent of Code 2022 day 8"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 8

    def run(self, input_data: Path) -> None:
        data: list[str]

        with input_data.open() as file:
            data = file.read().split("\n")

        tg: TreeGrid
        tg = Day8.tree_grid_from_input(data)

        # PART 1
        print("Part 1:")
        visible_trees: int = tg.visible.sum()
        print(f"A total of {visible_trees} trees are visible.")

        # PART 2
        print("\nPart 2:")

    @staticmethod
    def tree_grid_from_input(data: list[str]) -> TreeGrid:
        grid: list[list[int]] = [[int(x) for x in line.strip()]
                                 for line in data if len(line.strip()) > 0]
        return TreeGrid(grid)
