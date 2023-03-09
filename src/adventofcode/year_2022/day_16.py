"""
--- Day 16: Proboscidea Volcanium ---

The sensors have led you to the origin of the distress signal: yet another
handheld device, just like the one the Elves gave you. However, you don't see
any Elves around; instead, the device is surrounded by elephants! They must
have gotten lost in these tunnels, and one of the elephants apparently
figured out how to turn on the distress signal.

The ground rumbles again, much stronger this time. What kind of cave is this,
exactly? You scan the cave with your handheld device; it reports mostly
igneous rock, some ash, pockets of pressurized gas, magma... this isn't just
a cave, it's a volcano!

You need to get the elephants out of here, quickly. Your device estimates
that you have 30 minutes before the volcano erupts, so you don't have time to
go back out the way you came in.

You scan the cave for other options and discover a network of pipes and
pressure-release valves. You aren't sure how such a system got into a
volcano, but you don't have time to complain; your device produces a report (
your puzzle input) of each valve's flow rate if it were opened (in pressure
per minute) and the tunnels you could use to move between the valves.

There's even a valve in the room you and the elephants are currently standing
in labeled AA. You estimate it will take you one minute to open a single
valve and one minute to follow any tunnel from one valve to another. What is
the most pressure you could release?

For example, suppose you had the following scan output:

Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II

All of the valves begin closed. You start at valve AA, but it must be damaged
or jammed or something: its flow rate is 0, so there's no point in opening
it. However, you could spend one minute moving to valve BB and another minute
opening it; doing so would release pressure during the remaining 28 minutes
at a flow rate of 13, a total eventual pressure release of 28 * 13 = 364.
Then, you could spend your third minute moving to valve CC and your fourth
minute opening it, providing an additional 26 minutes of eventual pressure
release at a flow rate of 2, or 52 total pressure released by valve CC.

Making your way through the tunnels like this, you could probably open many
or all of the valves by the time 30 minutes have elapsed. However, you need
to release as much pressure as possible, so you'll need to be methodical.
Instead, consider this approach:

== Minute 1 ==
No valves are open.
You move to valve DD.

== Minute 2 ==
No valves are open.
You open valve DD.

== Minute 3 ==
Valve DD is open, releasing 20 pressure.
You move to valve CC.

== Minute 4 ==
Valve DD is open, releasing 20 pressure.
You move to valve BB.

== Minute 5 ==
Valve DD is open, releasing 20 pressure.
You open valve BB.

== Minute 6 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve AA.

== Minute 7 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve II.

== Minute 8 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve JJ.

== Minute 9 ==
Valves BB and DD are open, releasing 33 pressure.
You open valve JJ.

== Minute 10 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve II.

== Minute 11 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve AA.

== Minute 12 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve DD.

== Minute 13 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve EE.

== Minute 14 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve FF.

== Minute 15 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve GG.

== Minute 16 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve HH.

== Minute 17 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You open valve HH.

== Minute 18 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve GG.

== Minute 19 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve FF.

== Minute 20 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve EE.

== Minute 21 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You open valve EE.

== Minute 22 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You move to valve DD.

== Minute 23 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You move to valve CC.

== Minute 24 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You open valve CC.

== Minute 25 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 26 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 27 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 28 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 29 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 30 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

This approach lets you release the most pressure possible in 30 minutes with
this valve layout, 1651.

Work out the steps to release the most pressure in 30 minutes. What is the
most pressure you can release?


--- Part Two ---

You're worried that even with an optimal approach, the pressure released
won't be enough. What if you got one of the elephants to help you?

It would take you 4 minutes to teach an elephant how to open the right valves
in the right order, leaving you with only 26 minutes to actually execute your
plan. Would having two of you working together be better, even if it means
having less time? (Assume that you teach the elephant before opening any
valves yourself, giving you both the same full 26 minutes.)

In the example above, you could teach the elephant to help you as follows:

== Minute 1 ==
No valves are open.
You move to valve II.
The elephant moves to valve DD.

== Minute 2 ==
No valves are open.
You move to valve JJ.
The elephant opens valve DD.

== Minute 3 ==
Valve DD is open, releasing 20 pressure.
You open valve JJ.
The elephant moves to valve EE.

== Minute 4 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve II.
The elephant moves to valve FF.

== Minute 5 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve AA.
The elephant moves to valve GG.

== Minute 6 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve BB.
The elephant moves to valve HH.

== Minute 7 ==
Valves DD and JJ are open, releasing 41 pressure.
You open valve BB.
The elephant opens valve HH.

== Minute 8 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve CC.
The elephant moves to valve GG.

== Minute 9 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You open valve CC.
The elephant moves to valve FF.

== Minute 10 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant moves to valve EE.

== Minute 11 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant opens valve EE.

(At this point, all valves are open.)

== Minute 12 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 20 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 26 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

With the elephant helping, after 26 minutes, the best you could do would
release a total of 1707 pressure.

With you and an elephant working together for 26 minutes, what is the most
pressure you could release?

"""

from __future__ import annotations

import numpy as np

from itertools import combinations_with_replacement
from re import compile, Match, Pattern
from typing import NamedTuple, Iterable

from adventofcode.challenge import DayChallenge, Path


class Valve(NamedTuple):
    id: str
    flow_rate: int
    connections: list[str]


class Graph:
    """A network of connected valves"""

    class IntValve(NamedTuple):
        """A simplified valve that uses integers as ids."""
        id: int
        flow_rate: int
        connections: list[int]

    def __init__(self, valves: Iterable[Valve]):
        # the nodes (vertices)
        self.nodes: dict[int, Graph.IntValve]
        # conversion from string id to numerical id
        self.ids: list[str]
        # pairwise distance matrix (shortest distances)
        self.distances: np.ndarray
        # nodes with flow-rate above 0
        self.flow_nodes: list[int]

        self.ids = [valve.id for valve in valves]
        self.nodes = {
            self.ids.index(valve.id): Graph.IntValve(
                id=self.ids.index(valve.id),
                flow_rate=valve.flow_rate,
                connections=[self.ids.index(v) for v in valve.connections]
            )
            for valve in valves
        }
        self.distances = Graph._calculate_pairwise_distances(self.nodes)
        self.flow_nodes = [node.id for node in self.nodes.values()
                           if node.flow_rate > 0]

    def max_pressure_release(self, timelimit: int, start_node: str) -> int:
        """
        Calculate the maximal pressure that can be released in timelimit time
        units, starting from node start_node.
        """
        if start_node not in self.ids:
            raise ValueError("Start node not in network.")
        start_node_id = self.ids.index(start_node)
        possible_paths = self.calc_possible_paths(start_node_id, timelimit)
        max_release = max(possible_paths.values())
        return max_release

    def max_pressure_release_v2(self, timelimit: int, start_node: str) -> int:
        """
        Calculate the max pressure release after training an elefant to help.
        """
        class PathCombo(NamedTuple):
            pressure_release: int
            path1: int
            path2: int

        if start_node not in self.ids:
            raise ValueError("Start node not in network.")
        start_node_id = self.ids.index(start_node)

        # get possible paths
        paths = self.calc_possible_paths(start_node_id, timelimit)

        # choose the two, mutually exclusive, best paths
        path_combos: list[PathCombo] = [
            PathCombo(pressure_release=paths[p1]+paths[p2],
                      path1=p1, path2=p2)
            for p1, p2 in combinations_with_replacement(paths, 2)
            if p1 & p2 == 0
        ]

        max_pressure_release = max([combo.pressure_release
                                    for combo in path_combos])
        return max_pressure_release

    def calc_possible_paths(self, start_node: int, timelimit: int) \
            -> dict[int, int]:
        """
        Calculate all possible paths and pressure release, when starting from
        the specified node.
        :returns:
            dictionary with
            key=bitmask of visited nodes;
            value=total pressure released
        """
        def visit_node(node: int, time: int, pressure_released: int,
                       bitmask_visited: int) -> None:
            bitmask: int = (1 << node)
            flow_rate: int = self.nodes[node].flow_rate

            # time has run out
            if time > timelimit:
                return
            # node already visited
            if bitmask_visited & bitmask > 0:
                return
            # release pressure
            pressure_released += flow_rate * (timelimit - time)
            # update paths
            bitmask = bitmask_visited | bitmask
            if bitmask not in paths:
                paths[bitmask] = pressure_released
            else:
                paths[bitmask] = max(paths[bitmask], pressure_released)
            # visit other nodes
            for n in self.flow_nodes:
                dist = self.distances[node][n]
                visit_node(n, time=time + dist + 1,
                           pressure_released=pressure_released,
                           bitmask_visited=bitmask)

        paths: dict[int, int] = {}

        for n in self.flow_nodes:
            dist = self.distances[start_node][n]
            visit_node(n, time=dist + 1, pressure_released=0, bitmask_visited=0)

        return paths

    @staticmethod
    def _calculate_pairwise_distances(nodes: dict[str, Graph.IntValve]) -> \
            np.ndarray:
        """
        Calculate a matrix of pairwise shortest distances using a
        Floyd-Warshall algorithm.
        """
        n: int = len(nodes)
        # use a value larger than achievable by any choice of path as infinity
        infinity = n * n
        distances: np.ndarray = np.full(shape=(n, n), dtype=int,
                                        fill_value=infinity)
        # set values were direct connections exist to one
        for node in nodes.values():
            distances[node.id, node.id] = 0
            for con in node.connections:
                distances[node.id, con] = 1

        # execute Floyd-Warshall
        return Graph.floyd_warshall(distances)

    @staticmethod
    def floyd_warshall(distances: np.ndarray) -> np.ndarray:
        """Minimise pairwise distances between nodes."""
        dist = distances.copy()
        n = dist.shape[0]

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist


class Day16(DayChallenge):
    """Advent of Code 2022 day 16"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 16

    def run(self, input_data: Path) -> None:
        data: list[str]

        with input_data.open() as file:
            data = file.read().split("\n")

        valves = [Day16.parse_input_line(line)
                  for line in data if line]
        graph = Graph(valves)

        # PART 1
        print("Part 1:")
        max_release = graph.max_pressure_release(30, 'AA')
        print(f"max pressure release: {max_release}")

        # PART 2
        print("\nPart 2:")
        max_release_p2 = graph.max_pressure_release_v2(26, 'AA')
        print(f"max pressure release with an elefant in the team: "
              f"{max_release_p2}")

    @staticmethod
    def parse_input_line(line: str) -> Valve:
        line_regex: Pattern = compile(
            r'Valve (?P<id>[A-Z]{2}) has flow rate=(?P<flow>\d+); '
            r'tunnels? leads? to valves?\s+(?P<connections>([A-Z]{2}(,\s*)?)+)')
        m: Match = line_regex.match(line.strip())
        return Valve(
            id=m.group("id"),
            flow_rate=int(m.group("flow")),
            connections=[c.strip() for c in m.group("connections").split(",")]
        )
