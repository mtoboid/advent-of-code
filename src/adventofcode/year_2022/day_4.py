"""
--- Day 4: Camp Cleanup ---

Space needs to be cleared before the last supplies can be unloaded from the
ships, and so several Elves have been assigned the job of cleaning up
sections of the camp. Every section has a unique ID number, and each Elf is
assigned a range of section IDs.

However, as some of the Elves compare their section assignments with each
other, they've noticed that many of the assignments overlap. To try to
quickly find overlaps and reduce duplicated effort, the Elves pair up and
make a big list of the section assignments for each pair (your puzzle input).

For example, consider the following list of section assignment pairs:

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8

For the first few pairs, this list means:

    Within the first pair of Elves, the first Elf was assigned sections 2-4 (
    sections 2, 3, and 4), while the second Elf was assigned sections 6-8 (
    sections 6, 7, 8). The Elves in the second pair were each assigned two
    sections. The Elves in the third pair were each assigned three sections:
    one got sections 5, 6, and 7, while the other also got 7, plus 8 and 9.

This example list uses single-digit section IDs to make it easier to draw;
your actual list might contain larger numbers. Visually, these pairs of
section assignments look like this:

.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8

Some of the pairs have noticed that one of their assignments fully contains
the other. For example, 2-8 fully contains 3-7, and 6-6 is fully contained by
4-6. In pairs where one assignment fully contains the other, one Elf in the
pair would be exclusively cleaning sections their partner will already be
cleaning, so these seem like the most in need of reconsideration. In this
example, there are 2 such pairs.

In how many assignment pairs does one range fully contain the other?

--- Part Two ---

It seems like there is still quite a bit of duplicate work planned. Instead,
the Elves would like to know the number of pairs that overlap at all.

In the above example, the first two pairs (2-4,6-8 and 2-3,4-5) don't
overlap, while the remaining four pairs (5-7,7-9, 2-8,3-7, 6-6,4-6, and 2-6,
4-8) do overlap:

    5-7,7-9 overlaps in a single section, 7.
    2-8,3-7 overlaps all of the sections 3 through 7.
    6-6,4-6 overlaps in a single section, 6.
    2-6,4-8 overlaps in sections 4, 5, and 6.

So, in this example, the number of overlapping assignment pairs is 4.

In how many assignment pairs do the ranges overlap?
"""

from adventofcode.challenge import DayChallenge, Path


class Day4(DayChallenge):
    """Advent of Code 2022 day 4"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 4

    def run(self, input_data: Path) -> None:
        data: list[str]

        with input_data.open() as file:
            data = file.read().split("\n")

        # PART 1
        print("Part 1:")
        total_complete = sum([Day4.complete_overlap(line)
                             for line in data
                             if not line == ''])
        print(f"In {total_complete} assignment pairs do the ranges overlap "
              f"completely.")

        # PART 2
        print("\nPart 2:")
        total_any = sum([Day4.any_overlap(line)
                         for line in data
                         if not line == ''])
        print(f"In {total_any} assignment pairs do the ranges overlap "
              f"to a certain extent.")

    @staticmethod
    def range_to_set(range_: str) -> set[int]:
        """
        Convert a string representing a range e.g. '3-12' to a set containing
        all the numbers.
        """
        start, stop = range_.split("-")
        return set(range(int(start), int(stop)+1))

    @staticmethod
    def one_set_contained_in_other(a: set[int], b: set[int]) -> bool:
        """Is one of the sets (a or b) completely contained in the other?"""
        return a.issubset(b) or b.issubset(a)

    @staticmethod
    def complete_overlap(line: str) -> bool:
        """Do the sections represented by the line completely overlap?"""
        a, b = line.strip().split(",")
        return Day4.one_set_contained_in_other(Day4.range_to_set(a),
                                               Day4.range_to_set(b))

    @staticmethod
    def any_overlap(line: str) -> bool:
        """Do the sections represented by the line overlap at all?"""
        a, b = line.strip().split(",")
        return len(Day4.range_to_set(a) & Day4.range_to_set(b)) > 0
