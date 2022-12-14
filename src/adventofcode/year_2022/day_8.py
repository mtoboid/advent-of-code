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


--- Part Two ---

Content with the amount of tree cover available, the Elves just need to know
the best spot to build their tree house: they would like to be able to see a
lot of trees.

To measure the viewing distance from a given tree, look up, down, left,
and right from that tree; stop if you reach an edge or at the first tree that
is the same height or taller than the tree under consideration. (If a tree is
right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules
above; the proposed tree house has large eaves to keep it dry, so they
wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

    Looking up, its view is not blocked; it can see 1 tree (of height 3).

    Looking left, its view is blocked immediately; it can see only 1 tree (of
    height 5, right next to it).

    Looking right, its view is not blocked; it can see 2 trees.

    Looking down, its view is blocked eventually; it can see 2 trees (one of
    height 3, then the tree of height 5 that blocks its view).

A tree's scenic score is found by multiplying together its viewing distance
in each of the four directions. For this tree, this is 4 (found by
multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle
of the fourth row:

30373
25512
65332
33549
35390

    Looking up, its view is blocked at 2 trees (by another tree with a height
    of 5).

    Looking left, its view is not blocked; it can see 2 trees.

    Looking down, its view is also not blocked; it can see 1 tree.

    Looking right, its view is blocked at 2 trees (by a massive tree of
    height 9).

This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the
tree house.

Consider each tree on your map. What is the highest scenic score possible for
any tree?
"""

import numpy as np

from collections.abc import Sequence

from adventofcode.challenge import DayChallenge, Path


class TreeGrid:
    def __init__(self, tree_heights: list[list[int]]):
        self._tree_height: np.ndarray
        self._visible: np.ndarray
        self._scenic_score: np.ndarray

        self._tree_heights = np.array(tree_heights, dtype=int)
        self._visible = TreeGrid.gen_visibility_grid(self._tree_heights)
        self._scenic_scores = TreeGrid.gen_scenic_score_grid(self._tree_heights)

    def __str__(self):
        return self._tree_heights.__str__()

    @property
    def tree_heights(self) -> np.ndarray:
        """Return the grid of tree heights in the forrest."""
        out = self._tree_heights.copy()
        return out

    @property
    def visible(self) -> np.ndarray:
        """
        Return a boolean grid indicating visibility from the outside of all
        trees in the forrest.
        """
        out = self._visible
        return out

    @property
    def scenic_score(self) -> np.ndarray:
        """
        The scenic scores of the trees in the forest.
        :return:
            integer grid of scenic scores
        """
        out = self._scenic_scores.copy()
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
    def gen_scenic_score_grid(trees: np.ndarray) -> np.ndarray:
        """
        Generate a grid of integers indicating the 'scenic score' of each
        tree in the forest.
        """
        scenic_score_grid: np.ndarray = np.full(shape=trees.shape, dtype=int,
                                                fill_value=0)
        row_max: int = trees.shape[0] - 1
        col_max: int = trees.shape[1] - 1

        for row in range(0, row_max):
            for col in range(0, col_max):
                scenic_score_grid[row, col] = \
                  TreeGrid.calc_scenic_score_for_tree(trees, row, col)
        return scenic_score_grid

    @staticmethod
    def calc_scenic_score_for_tree(trees: np.ndarray, row: int, col: int) -> int:
        """Calculate the scenic score for the tree at (row, col)."""
        tree_height: int = trees[row, col]
        score_n: int = 0
        score_e: int = 0
        score_s: int = 0
        score_w: int = 0
        score_total: int

        # max for rows (y) and cols (x)
        max_y: int = trees.shape[0] - 1
        max_x: int = trees.shape[1] - 1

        # row / col the tree is in
        east_west = trees[row, :]
        north_south = trees[:, col]

        # visibility of trees
        # east-west in the same row
        # to west
        for x in [i-1 for i in range(col, 0, -1)]:
            score_w += 1
            if east_west[x] >= tree_height:
                break
        # to east
        for x in [i+1 for i in range(col, max_x)]:
            score_e += 1
            if east_west[x] >= tree_height:
                break
        # north-south in same col
        # to north
        for y in [i-1 for i in range(row, 0, -1)]:
            score_n += 1
            if north_south[y] >= tree_height:
                break
        # to south
        for y in [i + 1 for i in range(row, max_y)]:
            score_s += 1
            if north_south[y] >= tree_height:
                break

        score_total = score_n * score_e * score_s * score_w
        return score_total

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
        print(f"Mean scenic score: {tg.scenic_score.mean()}")
        print(f"Max scenic score: {tg.scenic_score.max()}")

    @staticmethod
    def tree_grid_from_input(data: list[str]) -> TreeGrid:
        grid: list[list[int]] = [[int(x) for x in line.strip()]
                                 for line in data if len(line.strip()) > 0]
        return TreeGrid(grid)
