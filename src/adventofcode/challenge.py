from abc import ABC, abstractmethod
from pathlib import Path
from timeit import default_timer as timer

from .errors import AdventOfCodeError
from .input_data import InputData


class ChallengeNotDefined(AdventOfCodeError):
    """Raised when the challenge for day x is not in the ChallengesList."""

    def __init__(self, day: int, *args):
        super().__init__(args)
        self.msg = f"A challenge for day {day} is not defined."

    def __str__(self):
        return self.msg


class DayChallenge(ABC):
    """Baseclass for a day challenge"""

    @property
    @abstractmethod
    def year(self) -> int:
        """Returns the year the challenge is for."""
        pass

    @property
    @abstractmethod
    def day(self) -> int:
        """Returns the day the challenge is for."""
        pass

    @abstractmethod
    def run(self, input_data: Path) -> None:
        """Run the challenge to obtain the answer."""
        pass


class ChallengesList:
    """
    A list of Advent of Code challenges accessible by day.
    """
    def __init__(self, year: int, input_data: InputData):
        self.year: int
        self.input_data: InputData
        self.challenges: dict[int, DayChallenge]

        self.year = year
        self.input_data = input_data
        self.challenges = {x+1: None for x in range(25)}

    def add(self, challenge: DayChallenge):
        """Add a new challenge to the list."""
        if challenge.year != self.year:
            raise ValueError("Trying to add challenge from wrong year.")
        if challenge.day not in self.challenges:
            raise ValueError(f"Challenge for day {challenge.day} not "
                             f"settable, only values between 1 and 25 are "
                             f"possible.")
        if self.challenges[challenge.day] is not None:
            raise IndexError(f"Challenge for day {challenge.day} is already "
                             f"set, re-setting is not supported.")
        self.challenges[challenge.day] = challenge

    def run(self, day: int):
        """Run the challenge from day x"""
        if day not in self.challenges or self.challenges[day] is None:
            raise ChallengeNotDefined(day)
        challenge: DayChallenge = self.challenges[day]
        print(f"Running {challenge.year} day {challenge.day}:\n")
        start_time = timer()
        challenge.run(self.input_data.day(day))
        end_time = timer()
        print(f"\nRunning time: {end_time - start_time} s")
