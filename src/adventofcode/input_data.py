from pathlib import Path

from .errors import AdventOfCodeError


# Errors
class InvalidDirError(AdventOfCodeError):
    """Raised when the specified dir does not exist."""
    def __init__(self, directory: Path, *args):
        super().__init__(args)
        self.directory = directory.absolute()

    def __str__(self):
        return f"Directory {self.directory} not found."


class InputFileMissingError(AdventOfCodeError):
    """Raised when the corresponding input file is missing."""
    def __init__(self, day: int, folder: Path, *args):
        super().__init__(args)
        self.msg = f"Input file for day {day} not found in {folder.absolute()}."

    def __str__(self):
        return self.msg


# Classes
class InputData:
    """
    Class representing a folder with the input files for the challenges.

    Load all files in directory into a list. All input file names have to
    have the format 'input_day_<int>'

    :argument directory:
        directory in which the input files reside
    """

    def __init__(self, directory: Path):
        self.directory: Path
        self.data: dict[int, Path]

        if not directory.exists():
            raise InvalidDirError(directory)
        self.directory = directory.absolute()
        self.data = dict()
        for file in self.directory.iterdir():
            if file.name.startswith("input"):
                day = int(file.name.split("_")[2])
                self.data[day] = file

    def __len__(self):
        return len(self.data)

    def day(self, n: int) -> Path:
        if n not in self.data:
            raise InputFileMissingError(day=n, folder=self.directory)
        return self.data[n]
