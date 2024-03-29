from pathlib import Path

from adventofcode.challenge import ChallengesList
from adventofcode.input_data import InputData

from .day_1 import Day1
from .day_2 import Day2
from .day_3 import Day3
from .day_4 import Day4
from .day_5 import Day5
from .day_6 import Day6
from .day_7 import Day7
from .day_8 import Day8
from .day_9 import Day9
from .day_10 import Day10
from .day_11 import Day11
from .day_12 import Day12
from .day_13 import Day13
from .day_14 import Day14
from .day_15 import Day15
from .day_16 import Day16
from .day_17 import Day17
from .day_18 import Day18

DATA_DIR_2022: Path
INPUT_DATA_2022: InputData
CHALLENGES_2022: ChallengesList

DATA_DIR_2022 = Path(__file__).parent.joinpath("data")
INPUT_DATA_2022 = InputData(DATA_DIR_2022)
CHALLENGES_2022 = ChallengesList(2022, INPUT_DATA_2022)

CHALLENGES_2022.add(Day1())
CHALLENGES_2022.add(Day2())
CHALLENGES_2022.add(Day3())
CHALLENGES_2022.add(Day4())
CHALLENGES_2022.add(Day5())
CHALLENGES_2022.add(Day6())
CHALLENGES_2022.add(Day7())
CHALLENGES_2022.add(Day8())
CHALLENGES_2022.add(Day9())
CHALLENGES_2022.add(Day10())
CHALLENGES_2022.add(Day11())
CHALLENGES_2022.add(Day12())
CHALLENGES_2022.add(Day13())
CHALLENGES_2022.add(Day14())
CHALLENGES_2022.add(Day15())
CHALLENGES_2022.add(Day16())
CHALLENGES_2022.add(Day17())
CHALLENGES_2022.add(Day18())
