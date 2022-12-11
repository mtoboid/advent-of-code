"""
--- Day 3: Rucksack Reorganization ---

One Elf has the important job of loading all of the rucksacks with supplies
for the jungle journey. Unfortunately, that Elf didn't quite follow the
packing instructions, and so a few items now need to be rearranged.

Each rucksack has two large compartments. All items of a given type are meant
to go into exactly one of the two compartments. The Elf that did the packing
failed to follow this rule for exactly one item type per rucksack.

The Elves have made a list of all of the items currently in each rucksack (
your puzzle input), but they need your help finding the errors. Every item
type is identified by a single lowercase or uppercase letter (that is,
a and A refer to different types of items).

The list of items for each rucksack is given as characters all on a single
line. A given rucksack always has the same number of items in each of its two
compartments, so the first half of the characters represent items in the
first compartment, while the second half of the characters represent items in
the second compartment.

For example, suppose you have the following list of contents from six
rucksacks:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw

    The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp,
    which means its first compartment contains the items vJrwpWtwJgWr,
    while the second compartment contains the items hcsFMMfFFhFp. The only
    item type that appears in both compartments is lowercase p. The second
    rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL.
    The only item type that appears in both compartments is uppercase L. The
    third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only
    common item type is uppercase P. The fourth rucksack's compartments only
    share item type v. The fifth rucksack's compartments only share item type
    t. The sixth rucksack's compartments only share item type s.

To help prioritize item rearrangement, every item type can be converted to a
priority:

    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.

In the above example, the priority of the item type that appears in both
compartments of each rucksack is 16 (p), 38 (L), 42 (P), 22 (v), 20 (t),
and 19 (s); the sum of these is 157.

Find the item type that appears in both compartments of each rucksack. What
is the sum of the priorities of those item types?


--- Part Two ---

As you finish identifying the misplaced items, the Elves come to you with
another issue.

For safety, the Elves are divided into groups of three. Every Elf carries a
badge that identifies their group. For efficiency, within each group of three
Elves, the badge is the only item type carried by all three Elves. That is,
if a group's badge is item type B, then all three Elves will have item type B
somewhere in their rucksack, and at most two of the Elves will be carrying
any other item type.

The problem is that someone forgot to put this year's updated authenticity
sticker on the badges. All of the badges need to be pulled out of the
rucksacks so the new authenticity stickers can be attached.

Additionally, nobody wrote down which item type corresponds to each group's
badges. The only way to tell which item type is the right one is by finding
the one item type that is common between all three Elves in each group.

Every set of three lines in your list corresponds to a single group, but each
group can have a different badge item type. So, in the above example,
the first group's rucksacks are the first three lines:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg

And the second group's rucksacks are the next three lines:

wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw

In the first group, the only item type that appears in all three rucksacks is
lowercase r; this must be their badges. In the second group, their badge item
type must be Z.

Priorities for these items must still be found to organize the sticker
attachment efforts: here, they are 18 (r) for the first group and 52 (Z) for
the second group. The sum of these is 70.

Find the item type that corresponds to the badges of each three-Elf group.
What is the sum of the priorities of those item types?
"""

from string import ascii_letters
from collections.abc import Sequence
from adventofcode.challenge import DayChallenge, Path


class Day3(DayChallenge):
    """Advent of Code year_2022 day 3"""

    LETTER_PRIORITIES: dict[str, int] = {
        letter: value for value, letter in enumerate(ascii_letters, start=1)
    }

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 3

    def run(self, input_data: Path) -> None:
        data: list[str]

        with input_data.open() as f:
            data = f.read().split("\n")

        # PART 1
        print("Part 1:")
        total_score = sum([Day3.priority_score(x) for x in data if len(x) > 0])

        print(f"The sum of all priorities is: {total_score}")

        # PART 2
        print("\nPart 2:")
        # get rid of the empty line at the bottom
        data = [x for x in data if not x == '']
        
        elf_groups: list[tuple[str, ...]]
        total_badge_score: int
        elf_groups = Day3.split_into_groups_of_three(data)
        total_badge_score = sum([Day3.group_score_badge(x) for x in elf_groups])
        print(f"Total priority score of all badges: {total_badge_score}")

    @staticmethod
    def cut_in_two(s: str) -> tuple[str, str]:
        """Cut the provided string in two, exactly in the middle."""

        if len(s) % 2 != 0:
            raise ValueError("String has to have an even number of characters.")
        half = len(s) // 2
        return s[:half], s[half:]

    @staticmethod
    def present_in_both_halves(s: str) -> list[str]:
        """Return elements that are present in both halves of the string."""

        a, b = Day3.cut_in_two(s)
        first = set(a)
        second = set(b)
        return list(first.intersection(second))

    @staticmethod
    def priority_score(s: str) -> int:
        """Return the priority of the element present in both halves"""

        letters: list[str] = Day3.present_in_both_halves(s)
        if len(letters) > 1:
            raise ValueError(f"More than one letter found in both halves, "
                             f"input: '{s}' letters: '{letters}.")
        return Day3.LETTER_PRIORITIES[letters.pop()]

    @staticmethod
    def split_into_groups_of_three(
            data: Sequence[str]
    ) -> list[tuple[str, ...]]:
        """Sort the data into groups of three 'elves' each."""

        if len(data) % 3 != 0:
            raise ValueError("Only lists with a length a multiple of three "
                             "can be processed.")

        return [tuple(data[x:x+3]) for x in range(0, len(data), 3)]

    @staticmethod
    def present_in_all_rucksacks(rucksacks: Sequence[str]) -> tuple[str, ...]:
        """Return the element(s) that are present in all rucksacks."""

        common_elements: set[str]

        if len(rucksacks) < 1:
            raise ValueError("At least one rucksack has to be provided")

        common_elements = set(rucksacks[0])
        for r in rucksacks:
            new_elements = set(r)
            common_elements = common_elements.intersection(new_elements)

        return tuple(common_elements)

    @staticmethod
    def group_score_badge(group: Sequence[str]) -> int:
        badges = Day3.present_in_all_rucksacks(group)
        if len(badges) > 1:
            raise ValueError("More than one badge found.")
        return Day3.LETTER_PRIORITIES[badges[0]]
