from pathlib import Path

from adventofcode.challenge import ChallengesList
from adventofcode.input_data import InputData

from .day_1 import Day1

DATA_DIR_2022: Path
INPUT_DATA_2022: InputData
CHALLENGES_2022: ChallengesList

DATA_DIR_2022 = Path(__file__).parent.joinpath("data")
INPUT_DATA_2022 = InputData(DATA_DIR_2022)
CHALLENGES_2022 = ChallengesList(2022, INPUT_DATA_2022)

CHALLENGES_2022.add(Day1())
