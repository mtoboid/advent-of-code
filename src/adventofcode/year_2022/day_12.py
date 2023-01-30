"""
--- Day 12: Hill Climbing Algorithm ---

You try contacting the Elves using your handheld device, but the river you're
following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle
input). The heightmap shows the local area from above broken into a grid; the
elevation of each square of the grid is given by a single lowercase letter,
where a is the lowest elevation, b is the next-lowest, and so on up to the
highest elevation, z.

Also included on the heightmap are marks for your current position (S) and
the location that should get the best signal (E). Your current position (S)
has elevation a, and the location that should get the best signal (E) has
elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps
as possible. During each step, you can move exactly one square up, down,
left, or right. To avoid needing to get out your climbing gear, the elevation
of the destination square can be at most one higher than the elevation of
your current square; that is, if your current elevation is m, you could step
to elevation n, but not to elevation o. (This also means that the elevation
of the destination square can be much lower than the elevation of your
current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Here, you start in the top-left corner; your goal is near the middle. You
could start by moving down or right, but eventually you'll need to head
toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^

In the above diagram, the symbols indicate whether the path exits each square
moving up (^), down (v), left (<), or right (>). The location that should get
the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the
location that should get the best signal?

--- Part Two ---

As you walk up the hill, you suspect that the Elves will want to turn this
into a hiking trail. The beginning isn't very scenic, though; perhaps you can
find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible:
elevation a. The goal is still the square marked E. However, the trail should
still be direct, taking the fewest steps to reach its goal. So, you'll need
to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Now, there are six choices for starting position (five marked a, plus the
square marked S that counts as being at elevation a). If you start at the
bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^

This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with
elevation a to the location that should get the best signal?"""

from __future__ import annotations

import numpy as np

import tkinter as tk
from tkinter import font as tk_font
from threading import Event, Thread

from enum import IntEnum
from typing import Any, NamedTuple, Sequence

from numpy import dtype
from sortedcontainers import SortedSet
from string import ascii_lowercase

from adventofcode.challenge import DayChallenge, Path


class Coordinates(NamedTuple):
    """Coordinates with an x and y value"""
    x: int
    y: int

    def __eq__(self, other) -> bool:
        if not isinstance(other, Coordinates):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __gt__(self, other) -> bool:
        if not isinstance(other, Coordinates):
            return NotImplemented
        if self.y > other.y:
            return True
        elif self.y < other.y:
            return False
        else:
            return self.x > other.x

    def __ge__(self, other) -> bool:
        if not isinstance(other, Coordinates):
            return NotImplemented
        if self.y > other.y:
            return True
        elif self.y < other.y:
            return False
        else:
            return self.x >= other.x

    def __lt__(self, other) -> bool:
        if not isinstance(other, Coordinates):
            return NotImplemented
        if self.y < other.y:
            return True
        elif self.y > other.y:
            return False
        else:
            return self.x < other.x

    def __le__(self, other) -> bool:
        if not isinstance(other, Coordinates):
            return NotImplemented
        if self.y < other.y:
            return True
        elif self.y > other.y:
            return False
        else:
            return self.x <= other.x

    def distance(self, other: Coordinates) -> int:
        """Manhattan distance to the other coordinate"""
        return abs(self.x - other.x) + abs(self.y - other.y)


class MapHeightValue(int):
    __slots__ = ()
    MAX_VALUE: int = len(ascii_lowercase) - 1
    REPRESENTATION: dict[int, str] = {
        i: ascii_lowercase[i] for i in range(MAX_VALUE+1)
    }
    CONVERSION: dict[str, int] = {
        ascii_lowercase[i]: i for i in range(MAX_VALUE+1)
    }

    def __new__(cls, value: str):
        if value not in MapHeightValue.CONVERSION.keys():
            raise ValueError(f"{value} is not a legal MapHeightValue.")
        return super().__new__(MapHeightValue, MapHeightValue.CONVERSION[value])

    def __str__(self) -> str:
        return MapHeightValue.REPRESENTATION[self]

    def __repr__(self) -> str:
        return f"MapHeightValue('{self.__str__()}') [{int(self)}]"

    @staticmethod
    def min() -> MapHeightValue:
        """The smallest possible height value"""
        return MapHeightValue(MapHeightValue.REPRESENTATION[0])

    @staticmethod
    def max() -> MapHeightValue:
        """The largest possible height value"""
        return MapHeightValue(
            MapHeightValue.REPRESENTATION[MapHeightValue.MAX_VALUE])


class MapField(NamedTuple):
    """A field / square on a map"""
    x: int
    y: int
    height: MapHeightValue

    @staticmethod
    def from_coordinates(coordinates: Coordinates,
                         height: MapHeightValue
                         ) -> MapField:
        return MapField(x=coordinates.x, y=coordinates.y, height=height)

    @property
    def coordinates(self) -> Coordinates:
        return Coordinates(x=self.x, y=self.y)

    def distance(self, other: MapField) -> int:
        return self.coordinates.distance(other.coordinates)

    def height_difference(self, other: MapField) -> int:
        return abs(self.height - other.height)


mapfield: dtype = np.dtype([("x", int), ("y", int), ("height", MapHeightValue)])


class HeightMap:
    START_CHAR: str = "S"
    START_HEIGHT: MapHeightValue = MapHeightValue.min()
    GOAL_CHAR: str = "E"
    GOAL_HEIGHT: MapHeightValue = MapHeightValue.max()

    def __init__(self, grid: list[str]):
        self.grid: np.ndarray[MapHeightValue]
        self.start: MapField
        self.goal: MapField

        self.start, self.goal, self.grid = self._initialize_values_from_list(
            grid)

    def __str__(self):
        return self.grid.__str__()

    @property
    def columns(self) -> int:
        return self.grid.shape[1]

    @property
    def rows(self) -> int:
        return self.grid.shape[0]

    def get_value(self, x: int, y: int) -> MapHeightValue:
        return self.grid[y, x]

    def get_field(self, pos: Coordinates) -> MapField:
        """Get the map field at the specified position (row y, col x)"""
        return MapField.from_coordinates(coordinates=pos,
                                         height=self.grid[pos.y, pos.x])

    def _initialize_values_from_list(self, lst: list[str]) -> \
            tuple[MapField, MapField, np.ndarray[MapHeightValue]]:
        """
        Set the initial values of the Map.

        Convert rows of letters representing heights in a grid to a numpy array.
        Furthermore, set the start and goal positions for the Map.
        """
        y_dim: int = len(lst)
        x_dim: int = len(lst[0])
        grid: np.ndarray = np.full(shape=(y_dim, x_dim),
                                   dtype=MapHeightValue,
                                   fill_value=0)
        start = None
        goal = None

        for i in range(y_dim):
            if len(lst[i]) != x_dim:
                raise ValueError("x dimensions of list are not identical.")
            for j in range(x_dim):
                char: str = lst[i][j]
                if char == HeightMap.START_CHAR:
                    if start is not None:
                        raise ValueError("More than one start position found.")
                    start = MapField(x=j, y=i, height=self.START_HEIGHT)
                    char = str(self.START_HEIGHT)
                if char == HeightMap.GOAL_CHAR:
                    if goal is not None:
                        raise ValueError("More than one goal position found.")
                    goal = MapField(x=j, y=i, height=self.GOAL_HEIGHT)
                    char = str(self.GOAL_HEIGHT)
                grid[i, j] = MapHeightValue(char)

        if start is None:
            raise ValueError("No start position found.")
        if goal is None:
            raise ValueError("No goal position found.")

        return start, goal, grid


class AStarFinishedError(Exception):
    """
    Raised when step is called although the algorithm has already found a path.
    """
    def __init__(self):
        super().__init__("Algorithm has already found a shortest path.")


class AStar:
    """Find the shortest path using an A-Star algorythm."""

    class Node:
        """A node on a path from start to goal"""
        def __init__(self,
                     height_map: HeightMap,
                     x: int, y: int,
                     previous: AStar.Node | None = None):
            self.height_map: HeightMap = height_map
            self.field: MapField = height_map.get_field(Coordinates(x=x, y=y))
            self._previous: AStar.Node | None = None
            self._dist_to_goal: int = self._calc_dist_to_goal()
            self._dist_to_start: int = 0

            self.previous = previous

        def __str__(self) -> str:
            return f"({self.field.x}|{self.field.y})[{str(self.field.height)}]"

        def __repr__(self) -> str:
            return f"Node {str(self)}"

        def __hash__(self):
            return hash(self.field.coordinates)

        def __eq__(self, other) -> bool:
            if not isinstance(other, AStar.Node):
                return NotImplemented
            else:
                return self.field.coordinates == other.field.coordinates

        @property
        def previous(self) -> AStar.Node | None:
            """The node that comes just before this in the path"""
            return self._previous

        @previous.setter
        def previous(self, value: AStar.Node) -> None:
            self._previous = value
            if value is None:
                self._dist_to_start = 0
            else:
                self._dist_to_start = self._previous._dist_to_start + 1

        @property
        def dist_to_start(self) -> int:
            return self._dist_to_start

        @property
        def dist_to_goal(self) -> int:
            return self._dist_to_goal

        @property
        def overall_dist(self) -> int:
            """Overall estimated distance from start to goal"""
            return self.dist_to_start + self.dist_to_goal

        def _calc_dist_to_goal(self) -> int:
            """
            Return the estimated distance to the goal, taking height into
            account.
            """
            distance = self.field.coordinates.distance(
                self.height_map.goal.coordinates)
            climb = self.height_map.goal.height - self.field.height
            if distance > climb:
                return distance
            else:
                return climb

    # ----- A-Star ----- #
    def __init__(self, height_map: HeightMap):
        self._finished:       bool = False
        self._height_map:     HeightMap = height_map
        self._nodes_in_paths: dict[MapField, AStar.Node] = dict()
        self._path_tip_nodes: SortedSet[AStar.Node] = SortedSet(
                    key=lambda node: (node.overall_dist, node.dist_to_goal))

        self.reset()

    @property
    def finished(self) -> bool:
        """This will be true if a shortest path has been found"""
        return self._finished

    def get_visited_squares(self) -> list[Coordinates]:
        """
        Return a list of all squares that have been visited by the A-Star
        algorithm.
        """
        visited = list(self._nodes_in_paths.values())
        return [node.field.coordinates for node in visited]

    def get_known_squares(self) -> list[Coordinates]:
        """
        Return a list of all squares that have been discovered by the A-Star
        algorithm.
        """
        known: set[Coordinates]
        nodes_in_path = list(self._nodes_in_paths.values())
        path_tips = list(self._path_tip_nodes)
        known = set([node.field.coordinates
                     for node in [*nodes_in_path, *path_tips]])
        return list(known)

    def get_current_path(self) -> list[Coordinates]:
        """Get the current best path from start to active square"""
        current_node: AStar.Node = self._path_tip_nodes[0]
        node_path: list[AStar.Node] = AStar._get_path_to_start(current_node)
        coord_path = [n.field.coordinates for n in node_path]
        return coord_path

    def reset(self) -> None:
        """Reset the search, discarding all current insights :)"""
        self._path_tip_nodes.clear()
        self._nodes_in_paths.clear()
        self._path_tip_nodes.add(AStar.Node(height_map=self._height_map,
                                            x=self._height_map.start.x,
                                            y=self._height_map.start.y))
        self._finished = False

    def step(self) -> None:
        """
        Calculate the next round for the A-Star search.
        """

        if self.finished:
            raise AStarFinishedError()

        tip_nodes:     SortedSet[AStar.Node] = self._path_tip_nodes
        visited_nodes: dict[MapField, AStar.Node] = self._nodes_in_paths
        current_node:  AStar.Node = tip_nodes.pop(0)
        next_nodes:    list[AStar.Node] = self._get_reachable_neighbours(
                                                              current_node)
        # remove the node we came from
        if current_node.previous in next_nodes:
            next_nodes.remove(current_node.previous)

        for node in next_nodes:
            # Found Goal
            if node.field == self._height_map.goal:
                node.previous = current_node
                tip_nodes.clear()
                tip_nodes.add(node)
                self._finished = True
            # Found node already in other path (update if adequate)
            elif node.field in visited_nodes:
                old_dist = visited_nodes[node.field].dist_to_start
                new_dist = current_node.dist_to_start + 1
                if new_dist < old_dist:
                    n = visited_nodes.pop(node.field)
                    n.previous = current_node
                    tip_nodes.add(n)
            # Found node already in tips
            elif node in tip_nodes:
                idx = AStar._get_index_by_coordinates(tip_nodes, node)
                other: AStar.Node = tip_nodes.pop(idx)
                if other.dist_to_start > current_node.dist_to_start + 1:
                    other.previous = current_node
                tip_nodes.add(other)

            # New path
            else:
                node.previous = current_node
                self._path_tip_nodes.add(node)

        visited_nodes[current_node.field] = current_node

    def _get_reachable_neighbours(self, node: Node) -> list[AStar.Node]:
        """
        Get the neighbours of a node that are reachable.

        Reachable are adjacent nodes on the grid horizontally and vertically,
        which height is not more than one larger than the node.
        """

        x: int = node.field.coordinates.x
        y: int = node.field.coordinates.y
        h: int = node.field.height
        max_x: int = self._height_map.columns - 1
        max_y: int = self._height_map.rows - 1
        neighbours: list[AStar.Node] = list()

        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            xx = x + i
            yy = y + j
            if any([xx < 0, yy < 0, xx > max_x, yy > max_y]):
                continue
            nb_node = AStar.Node(height_map=self._height_map, x=xx, y=yy)
            if (h + 1) >= nb_node.field.height:
                neighbours.append(nb_node)

        return neighbours

    @staticmethod
    def _get_index_by_coordinates(
            nodes: SortedSet[AStar.Node],
            node: AStar.Node) -> int:
        """
        In a SortedSet of nodes that is ordered by total distance, get an index
        using the node coordinated, NOT the distance.
        """
        idx: int = 0

        for n in nodes:
            if node.field.coordinates == n.field.coordinates:
                return idx
            else:
                idx += 1
        raise IndexError(f"{node} not in Set.")

    @staticmethod
    def _get_path_to_start(node: AStar.Node) -> list[AStar.Node]:
        """Trace a path from the node to start (if node is on a path)"""
        path: list[AStar.Node] = list()
        path.append(node)
        while path[-1].previous is not None:
            path.append(path[-1].previous)
        return path


class GridCellState(IntEnum):
    """
    State for colouring of a grid cell

    unset   - state that indicates a missing setting
    unknown - not yet discovered by A-Star
    known   - discovered by A-Star
    active  - member of the active path
    current - cell that is currently the cell investigated by A-Star
    """
    unset = -1
    unknown = 0
    known = 1
    visited = 2
    active = 3
    current = 4


class GuiMapGrid(tk.Canvas):
    """
    A gui grid-widget that can display a height-map and the progress of an
    A-Star algorithm.
    """
    class Cell(NamedTuple):
        """
        A cell in the grid, consisting of the id of the corresponding rectangle,
        and the id of the corresponding text.
        """
        rect_id: int
        label_id: int
        height: int
        state: GridCellState
        update: bool

    # datatype for the Cell class
    cell = np.dtype([("rect_id", int), ("label_id", int), ("height", int),
                     ("state", int), ("update", bool)])

    def __init__(self,
                 master: tk.Frame,
                 height_map: HeightMap,
                 square_size: int = 20,
                 line_width: int = 2,
                 margin: int = 5):

        self.widgetName = "GuiMapGrid"
        self._square_size: int = 0   # width and height of a square in px
        self._line_width: int = 0    # width of the lines between the squares px
        self._margin: int = 0        # margin around the grid in px
        self._height_map: HeightMap
        self._cells: np.ndarray      # array with rectangle ids (cells of grid)

        super().__init__(master=master)

        # normally here check input values...
        self._height_map = height_map
        self._cells = self._init_cells(height_map)
        self._square_size = square_size
        self._line_width = line_width
        self._margin = margin
        self._redraw_grid()

    @property
    def rows(self) -> int:
        """Number of rows in the grid"""
        return self._height_map.grid.shape[0]

    @property
    def columns(self) -> int:
        """Number of columns in the grid"""
        return self._height_map.grid.shape[1]

    @property
    def line_width(self) -> int:
        """Width of the grid lines in px."""
        return self._line_width

    @line_width.setter
    def line_width(self, value: int) -> None:
        if value != self._line_width:
            self._line_width = value
            self._redraw_grid()

    @property
    def outline_width(self) -> int:
        """The thickness of the outline of a single square in px."""
        return int(round(self.line_width / 2))

    @property
    def margin(self) -> int:
        """Spacing around the grid"""
        return self._margin

    @margin.setter
    def margin(self, value: int) -> None:
        if value != self._margin:
            self._margin = value
            self._redraw_grid()

    @property
    def square_size(self) -> int:
        """The size of the grid squares (width and height in px)"""
        return self._square_size

    @square_size.setter
    def square_size(self, value) -> None:
        if value < 1:
            raise ValueError("Square size has to be >=1 px.")
        if value != self._square_size:
            self._square_size = value
            self._redraw_grid()

    @property
    def width(self) -> int:
        """Width in pixels"""
        return self.columns * (self.square_size + self.line_width) + \
            2*self.margin

    @property
    def height(self) -> int:
        """Height in pixels"""
        return self.rows * (self.square_size + self.line_width) + 2*self.margin

    def clear_all_states(self, redraw: bool = True) -> None:
        """Set the state of all cells to GridCellState.unknown"""
        idx: np.ndarray = self._cells["state"] != GridCellState.unknown

        if idx.any():
            self._cells["state"] = GridCellState.unknown
            self._cells["update"] = idx
            if redraw:
                self._redraw_cells()

    def set_states(self,
                   cells: Sequence[Coordinates],
                   states: Sequence[GridCellState],
                   redraw: bool = True) -> None:
        """
        Change the states of several cells on the grid.

        If several cells are specified, but only one state, set all cells to
        that state; otherwise set each cell to the corresponding state.
        """

        if len(states) not in [1, len(cells)]:
            raise ValueError("The length of states has to be of the same "
                             "length as cells or contain only one element.")

        idx_x: tuple[int] = tuple([cell.x for cell in cells])
        idx_y: tuple[int] = tuple([cell.y for cell in cells])

        updated: np.ndarray[bool]
        updated = self._cells["state"][idx_y, idx_x] != states

        self._cells["state"][idx_y, idx_x] = states
        self._cells["update"][idx_y, idx_x] = updated

        if redraw:
            self._redraw_cells()

    def _init_cells(self, hm: HeightMap) -> np.ndarray:
        """Initialize the grid cells"""
        rows, cols = hm.grid.shape
        cells: np.ndarray = np.full(shape=(rows, cols),
                                    dtype=GuiMapGrid.cell,
                                    fill_value=-1)
        for r in range(rows):
            for c in range(cols):
                coord = Coordinates(x=c, y=r)
                text = ''
                height = int(hm.get_field(coord).height)
                if coord == hm.start.coordinates:
                    text = 'o'
                elif coord == hm.goal.coordinates:
                    text = 'x'
                cells[r, c]["rect_id"] = self.create_rectangle((0, 0, 0, 0))
                cells[r, c]["height"] = height
                cells[r, c]["label_id"] = self.create_text((0, 0),
                                                           text=text,
                                                           anchor='center')
        cells["state"] = GridCellState.unknown
        cells["update"] = False
        return cells

    def _redraw_grid(self) -> None:
        """Set the square size of all squares."""

        font_size: int = 13
        if self.square_size <= 17:
            font_size = round(self.square_size*0.95)
        font = tk_font.Font(family="Courier", size=font_size,
                            weight=tk_font.BOLD)

        rectangle_settings: dict[str, Any] = {
            "width": self.outline_width,
            "activewidth": self.outline_width,
            "disabledwidth": self.outline_width,
            "state": "normal"
        }

        for r in range(self.rows):
            for c in range(self.columns):
                cell: cell = self._cells[r, c]
                rect_id = cell["rect_id"]
                label_id = cell["label_id"]
                s = self.square_size
                o = self.outline_width
                m = 1 + self._margin
                x1 = m + c*(s+2*o)
                x2 = x1 + s
                y1 = m + r*(s+2*o)
                y2 = y1 + s
                rect_coord = (x1, y1, x2, y2)
                label_coord = (((x1+x2)/2 - 1), ((y1+y2)/2 - 1))
                self.coords(rect_id, rect_coord)
                self.itemconfigure(rect_id,
                                   cnf=self._cell_style(cell).update(
                                       rectangle_settings))
                self.coords(label_id, label_coord)
                self.itemconfigure(label_id, font=font)

        self.configure(width=self.width, height=self.height)
        self._cells["update"] = True
        self._redraw_cells()

    def _redraw_cells(self) -> None:
        """Re-set the style of all the cells for which update is true"""
        idx: np.ndarray = self._cells["update"]
        if idx.any():
            for cell in np.nditer(self._cells[idx]):
                self.itemconfigure(cell["rect_id"],
                                   cnf=GuiMapGrid._cell_style(cell))
            self._cells["update"] = False

    @staticmethod
    def _cell_outline(state: GridCellState) -> dict[str, Any]:
        """
        Return a dictionary with outline specs for a cell depending on state.
        """
        outline_color: str
        # cases
        if state == GridCellState.unknown:
            outline_color = ''
        elif state == GridCellState.known:
            outline_color = 'grey75'
        elif state == GridCellState.visited:
            outline_color = 'khaki'
        elif state == GridCellState.active:
            outline_color = 'blue'
        elif state == GridCellState.current:
            outline_color = 'blue'
        else:
            outline_color = 'red'

        return {
            "outline": outline_color,
            "activeoutline": outline_color,
            "disabledoutline": outline_color,
        }

    @staticmethod
    def _cell_background(cell: cell) -> dict[str, Any]:
        """
        Return a dictionary with the correct background settings for a cell.
        """
        state: GridCellState = cell["state"]
        height: int = cell["height"]
        grey_shade = GuiMapGrid._height_as_grey_shade(height)
        fill_color: str = grey_shade
        if state == GridCellState.current:
            fill_color = "blue"

        return {
            "fill": fill_color,
            "activefill": fill_color,
            "disabledfill": fill_color,
        }

    @staticmethod
    def _cell_style(cell: cell) -> dict[str, Any]:
        """
        Return a dictionary, for .configure, with the settings for a cell.
        """
        state: GridCellState = cell["state"]
        style: dict[str, Any] = dict()
        style.update(GuiMapGrid._cell_background(cell=cell))
        style.update(GuiMapGrid._cell_outline(state=state))
        return style

    @staticmethod
    def _height_as_grey_shade(height: int) -> str:
        """Convert a height to a corresponding shade of grey"""
        return f"grey{100 - 2 * height}"


class Gui(tk.Tk):
    """
    A Window with a grid to display a height map and show the progress of the
    A-Star algorithm.
    """
    def __init__(self, height_map: HeightMap):
        super().__init__()

        self._height_map: HeightMap = height_map
        self._a_star: AStar = AStar(height_map=self._height_map)
        # variables
        # - is the a-star currently paused? -
        self._paused_var: tk.BooleanVar = tk.BooleanVar(master=self,
                                                        name="_paused",
                                                        value=False)
        # - interval for drawing the a-star state to the grid
        self._draw_interval_var: tk.IntVar = tk.IntVar(master=self,
                                                       name="_draw_interval",
                                                       value=1)
        # Event an a_star thread will wait for to continue (for pausing)
        self._do_run_a_star: Event = Event()
        # Event an a_star thread will check to abort
        self._abort_a_star: Event = Event()
        self._a_star_thread: Thread | None = None
        # - to display the length of the currently active path -
        self._path_len_var: tk.StringVar = tk.StringVar(master=self,
                                                        name="_path_len_var",
                                                        value="")
        # gui
        self.baseFrame: tk.Frame
        self.dataGrid: GuiMapGrid
        # buttons
        self.buttonPanel: tk.Frame
        self.resetButton: tk.Button
        self.startButton: tk.Button
        self.pauseButton: tk.Button
        self.quitButton: tk.Button
        # labels
        self.pathLengthLabel: tk.Label
        self.drawIntervalLabel: tk.Label
        # slider
        self.drawIntervalSlider: tk.Scale

        self.title("Advent of Code day 12")
        self.create_widgets()
        self.reset()

    # noinspection PyAttributeOutsideInit
    def create_widgets(self):
        # Window root (self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.resizable(width=False, height=False)
        # Main Window canvas
        self.baseFrame = tk.Frame(master=self)
        self.baseFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
        self.baseFrame.rowconfigure(0, weight=1)
        self.baseFrame.columnconfigure(0, weight=1)
        # Grid for display of the height map and A-Star search
        self.dataGrid = GuiMapGrid(master=self.baseFrame,
                                   height_map=self._height_map,
                                   square_size=10)
        self.dataGrid.grid(row=0, column=0, padx=2, pady=2, ipadx=0,
                           sticky="nesw")

        # Buttons / Labels #
        self.buttonPanel = tk.Frame(master=self.baseFrame)
        self.buttonPanel.grid(row=1, column=0, padx=2, pady=2, sticky="wse")
        self.buttonPanel.rowconfigure(0, weight=1)
        self.buttonPanel.columnconfigure(4, weight=1)

        # reset
        self.resetButton = tk.Button(master=self.buttonPanel,
                                     text="Reset",
                                     command=self.reset)
        self.resetButton.grid(row=0, column=0, sticky=tk.W)
        # start
        self.startButton = tk.Button(master=self.buttonPanel,
                                     text="Start",
                                     command=self.start)
        self.startButton.grid(row=0, column=1, sticky=tk.W)
        # pause
        self.pauseButton = tk.Button(master=self.buttonPanel,
                                     text="Pause",
                                     command=self.pause)
        self.pauseButton.grid(row=0, column=2, sticky=tk.W)
        self._paused_var.trace_add(mode="write",
                                   callback=self._set_pause_btn_style)
        # draw interval
        draw_interval_bg = 'grey85'
        self.drawIntervalFrame = tk.Frame(master=self.buttonPanel)
        self.drawIntervalFrame.grid(row=0, column=3,
                                    padx=100, pady=0, ipadx=2, ipady=2)
        self.drawIntervalFrame.configure(background=draw_interval_bg,
                                         borderwidth=2,
                                         relief='groove')
        self.drawIntervalFrame.rowconfigure(0, weight=1)
        self.drawIntervalFrame.columnconfigure(1, weight=1)
        self.drawIntervalLabel = tk.Label(master=self.drawIntervalFrame,
                                          text="Grid refresh interval:")
        self.drawIntervalLabel.grid(row=0, column=0, padx=10)
        self.drawIntervalLabel.configure(background=draw_interval_bg)
        self.drawIntervalSlider = tk.Scale(master=self.drawIntervalFrame,
                                           orient='horizontal',
                                           from_=1, to=1000,
                                           variable=self._draw_interval_var)
        self.drawIntervalSlider.grid(row=0, column=1)
        self.drawIntervalSlider.configure(background=draw_interval_bg)

        # path length label
        self.pathLengthLabel = tk.Label(master=self.buttonPanel,
                                        textvariable=self._path_len_var)
        self.pathLengthLabel.grid(row=0, column=4)
        # quit
        self.quitButton = tk.Button(master=self.buttonPanel,
                                    text="Quit",
                                    command=self.close)
        self.quitButton.grid(row=0, column=5, sticky=tk.E)

    def reset(self) -> None:
        if self._a_star_thread is not None:
            self._abort_a_star.set()
            self._do_run_a_star.set()
            self._a_star_thread.join()
            self._a_star_thread = None
        self._a_star.reset()
        self._abort_a_star.clear()
        self._paused_var.set(False)
        self._draw_interval_var.set(100)
        self._path_len_var.set(f"Press Start")
        self.dataGrid.clear_all_states()

    def start(self) -> None:
        """Start a thread running A-Star, or re-start a paused one."""
        if self._a_star_thread is None:
            self._a_star_thread = Thread(target=self._run_a_star,
                                         name="run_a_star",
                                         kwargs={
                                             'do_run': self._do_run_a_star,
                                             'abort': self._abort_a_star,
                                             'interval': self._draw_interval_var
                                         })
            self._a_star_thread.start()

        self._paused_var.set(False)
        self._do_run_a_star.set()

    def pause(self) -> None:
        """Pause a running A-Star search"""
        if self._a_star_thread is None:
            return

        if self._paused_var.get():
            # unpause
            self._paused_var.set(False)
            self._do_run_a_star.set()
        else:
            # pause
            self._paused_var.set(True)
            self._do_run_a_star.clear()

    def close(self) -> None:
        """Quit the application after killing the A-Star thread"""
        self.reset()
        self.quit()

    def _set_pause_btn_style(self, *args) -> None:
        """Set the style of the pause button according to the state un/paused"""

        if self._paused_var.get():
            # paused
            self.pauseButton.configure(relief="sunken")
        else:
            # un-paused
            self.pauseButton.configure(relief="raised")

    def _run_a_star(self, do_run: Event, abort: Event, interval: tk.IntVar) \
            -> None:
        """Run the A-Star search."""
        a_star = self._a_star
        counter: int = 0

        while not a_star.finished:
            do_run.wait()
            if abort.is_set():
                return
            a_star.step()
            counter += 1
            if counter % interval.get() == 0:
                self._update_grid()

        self._update_grid()
        return

    def _update_grid(self) -> None:
        """Update the datagrid to show the current state of the search"""
        gui = self.dataGrid
        known_squares = self._a_star.get_known_squares()
        visited_squares = self._a_star.get_visited_squares()
        current_path = self._a_star.get_current_path()
        current_path_states = [GridCellState.active] * (len(current_path) - 1)
        current_path_states.insert(0, GridCellState.current)

        if self._a_star.finished:
            self._path_len_var.set(f"FINISHED  --  Final shortest path ="
                                   f" {len(current_path)}"
                                   f" ({len(current_path) - 1} steps)"
                                   f"          ")
        else:
            self._path_len_var.set(f"Running search  ---  Current active path ="
                                   f" {len(current_path)}")

        gui.set_states(known_squares, states=[GridCellState.known],
                       redraw=False)
        gui.set_states(visited_squares, states=[GridCellState.visited],
                       redraw=False)
        gui.set_states(current_path, states=current_path_states)


class Day12(DayChallenge):
    """Advent of Code 2022 day 12"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 12

    def run(self, input_data: Path) -> None:
        data: list[str]

        with input_data.open() as file:
            data = file.read().split("\n")

        # remove empty last line
        data = [d for d in data if d]

        # PART 1
        print("Part 1:")
        height_map: HeightMap = HeightMap(data)
        gui = Gui(height_map=height_map)
        gui.mainloop()

        # PART 2
        print("\nPart 2:")
