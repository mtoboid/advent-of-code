"""
Template for a day challenge
"""

from adventofcode.challenge import DayChallenge, Path


class DayX(DayChallenge):
    """Advent of Code 2022 day X"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return -1

    def run(self, input_data: Path) -> None:
        data: list[str]

        with input_data.open() as file:
            data = file.read().split("\n")
