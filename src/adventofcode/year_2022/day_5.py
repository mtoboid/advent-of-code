"""
--- Day 5: Supply Stacks ---

The expedition can depart as soon as the final supplies have been unloaded
from the ships. Supplies are stored in stacks of marked crates, but because
the needed supplies are buried under many other crates, the crates need to be
rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To
ensure none of the crates get crushed or fall over, the crane operator will
rearrange them in a series of carefully-planned steps. After the crates are
rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate
procedure, but they forgot to ask her which crate will end up where, and they
want to be ready to unload them as soon as possible, so they can embark.

They do, however, have a drawing of the starting stacks of crates and the
rearrangement procedure (your puzzle input). For example:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

In this example, there are three stacks of crates. Stack 1 contains two
crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains
three crates; from bottom to top, they are crates M, C, and D. Finally,
stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure,
a quantity of crates is moved from one stack to a different stack. In the
first step of the above rearrangement procedure, one crate is moved from
stack 2 to stack 1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3

In the second step, three crates are moved from stack 1 to stack 3. Crates
are moved one at a time, so the first crate to be moved (D) ends up below the
second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3

Then, both crates are moved from stack 2 to stack 1. Again, because crates
are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3

Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3

The Elves just need to know which crate will end up on top of each stack; in
this example, the top crates are C in stack 1, M in stack 2, and Z in stack
3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of
each stack?


--- Part Two ---

As you watch the crane operator expertly rearrange the crates, you notice the
process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly
wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air
conditioning, leather seats, an extra cup holder, and the ability to pick up
and move multiple crates at once.

Again considering the example above, the crates begin in the same
configuration:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3

However, the action of moving three crates from stack 1 to stack 3 means that
those three moved crates stay in the same order, resulting in this new
configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3

Next, as both crates are moved from stack 2 to stack 1, they retain their
order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3

Finally, a single crate is still moved from stack 1 to stack 2, but now it's
crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3

In this example, the CrateMover 9001 has put the crates in a totally
different order: MCD.

Before the rearrangement process finishes, update your simulation so that the
Elves know where they should stand to be ready to unload the final supplies.
After the rearrangement procedure completes, what crate ends up on top of
each stack?
"""

import re

from adventofcode.challenge import DayChallenge, Path


class Day5(DayChallenge):
    """Advent of Code 2022 day 5"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 5

    def run(self, input_data: Path) -> None:
        data: list[str]
        stacks_1: dict[int, list[str]]

        with input_data.open() as file:
            data = file.read().split("\n")

        # split data into initial setup and moves
        initial_setup: list[str]
        moves: list[str]

        # get separating blank line between initial setup and moves
        sep: int = 0
        while not data[sep] == '':
            sep += 1
        # stack setup
        initial_setup = data[:sep]
        moves = data[sep+1:]

        # PART 1
        print("Part 1:")
        stacks_1 = Day5.gen_initial_stacks(initial_setup)
        for m in moves:
            if not m == '':
                Day5.move(stacks_1, m)
        print(f"Top items are: {Day5.topmost_items(stacks_1)}")

        # PART 2
        print("\nPart 2:")
        stacks_2 = Day5.gen_initial_stacks(initial_setup)
        for m in moves:
            if not m == '':
                Day5.move_v2(stacks_2, m)
        print(f"Top items are: {Day5.topmost_items(stacks_2)}")

    @staticmethod
    def gen_initial_stacks(structure: list[str]) -> dict[int, list[str]]:
        """
        Convert a string representation of stacks to a list representation.
        """
        stacks: dict[int, list[str]]
        pattern_stack: re.Pattern = re.compile(r'\[(.)]|\s{3,4}')

        # determine number of stacks
        stack_nos = list(map(int, structure[-1].split()))
        stacks = {x: list() for x in stack_nos}

        # invert input and remove stack numbers to build up stacks from
        # bottom-up
        stacks_in = structure[-2::-1]
        for line in stacks_in:
            # get the items for that row
            items = pattern_stack.findall(line)
            # put them onto the stacks
            for idx, value in enumerate(items, start=stack_nos[0]):
                if not value == '':
                    stacks[idx].append(value)
        return stacks

    @staticmethod
    def gen_move_from_line(line: str) -> tuple[int, int, int]:
        """
        Convert a line of the form 'move <n> from <from_> to <to_>' to
        a tuple of integers (<n>, <from_>, <to_>).
        """

        line_pattern: re.Pattern = re.compile(r'\s*move\s*(?P<n>\d+)\s*'
                                              r'from\s*(?P<from_>\d+)\s*'
                                              r'to\s*(?P<to_>\d+)\s*')
        m = line_pattern.match(line)
        if m is None:
            raise ValueError(f"Passed line {line} does not conform to"
                             f"'move <n> from <from> to <to>'")
        return int(m.group("n")), int(m.group("from_")), int(m.group("to_"))

    @staticmethod
    def move(stacks: dict[int, list[str]], action: str) -> None:
        """Perform the move <action> specified on the passed stacks."""
        n: int
        from_: int
        to_: int
        n, from_, to_ = Day5.gen_move_from_line(action)
        for i in range(n):
            stacks[to_].append(stacks[from_].pop())
        return None

    @staticmethod
    def move_v2(stacks: dict[int, list[str]], action: str) -> None:
        """Perform a combined move of crates specified in the move action."""
        n: int
        from_: int
        to_: int
        n, from_, to_ = Day5.gen_move_from_line(action)
        stacks[to_].extend(stacks[from_][-n:])
        del stacks[from_][-n:]



    @staticmethod
    def topmost_items(stacks: dict[int, list[str]]) -> str:
        """Return a string composed of the top items of the stacks."""
        out: list[str] = list()
        idx = sorted(stacks.keys())
        for i in idx:
            out.append(stacks[i][-1])
        return "".join(out)
