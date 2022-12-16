"""
--- Day 10: Cathode-Ray Tube ---

You avoid the ropes, plunge into the river, and swim to shore.

The Elves yell something about meeting back up with them upriver, but the
river is too loud to tell exactly what they're saying. They finish crossing
the bridge and disappear from view.

Situations like this must be why the Elves prioritized getting the
communication system on your handheld device working. You pull it out of your
pack, but the amount of water slowly draining from a big crack in its screen
tells you it probably won't be of much immediate use.

Unless, that is, you can design a replacement for the device's video system!
It seems to be some kind of cathode-ray tube screen and simple CPU that are
both driven by a precise clock circuit. The clock circuit ticks at a constant
rate; each tick is called a cycle.

Start by figuring out the signal being sent by the CPU. The CPU has a single
register, X, which starts with the value 1. It supports only two instructions:

    addx V takes two cycles to complete. After two cycles, the X register is
    increased by the value V. (V can be negative.) noop takes one cycle to
    complete. It has no other effect.

The CPU uses these instructions in a program (your puzzle input) to, somehow,
tell the screen what to draw.

Consider the following small program:

noop
addx 3
addx -5

Execution of this program proceeds as follows:

    At the start of the first cycle, the noop instruction begins execution.
    During the first cycle, X is 1. After the first cycle, the noop
    instruction finishes execution, doing nothing.

    At the start of the second cycle, the addx 3 instruction begins
    execution. During the second cycle, X is still 1.

    During the third cycle, X is still 1. After the third cycle, the addx 3
    instruction finishes execution, setting X to 4.

    At the start of the fourth cycle, the addx -5 instruction begins
    execution. During the fourth cycle, X is still 4.

    During the fifth cycle, X is still 4. After the fifth cycle, the addx -5
    instruction finishes execution, setting X to -1.

Maybe you can learn something by looking at the value of the X register
throughout execution. For now, consider the signal strength (the cycle number
multiplied by the value of the X register) during the 20th cycle and every 40
cycles after that (that is, during the 20th, 60th, 100th, 140th, 180th,
and 220th cycles).

For example, consider this larger program:

addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop

The interesting signal strengths can be determined as follows:

    During the 20th cycle, register X has the value 21, so the signal
    strength is 20 * 21 = 420. (The 20th cycle occurs in the middle of the
    second addx -1, so the value of register X is the starting value, 1,
    plus all of the other addx values up to that point: 1 + 15 - 11 + 6 - 3 +
    5 - 1 - 8 + 13 + 4 = 21.)

    During the 60th cycle, register X has the value 19, so the signal
    strength is 60 * 19 = 1140.

    During the 100th cycle, register X has the value 18, so the signal
    strength is 100 * 18 = 1800.

    During the 140th cycle, register X has the value 21, so the signal
    strength is 140 * 21 = 2940.

    During the 180th cycle, register X has the value 16, so the signal
    strength is 180 * 16 = 2880.

    During the 220th cycle, register X has the value 18, so the signal
    strength is 220 * 18 = 3960.

The sum of these signal strengths is 13140.

Find the signal strength during the 20th, 60th, 100th, 140th, 180th,
and 220th cycles. What is the sum of these six signal strengths?
"""

from enum import Enum
from typing import Callable

from adventofcode.challenge import DayChallenge, Path
from adventofcode.errors import AdventOfCodeError


class TubeNotReadyError(AdventOfCodeError):
    """Raised when instruction is passed to tube before it is ready."""
    pass


class TubeNoInstructionError(AdventOfCodeError):
    """
    Raised when an execution is requested without having set an instruction.
    """


class TubeInstruction(Enum):
    NOOP = 1
    ADDX = 2

    def __init__(self, cycles: int):
        self.cycles: int = cycles

    @staticmethod
    def from_string(s: str) -> 'TubeInstruction':
        instruction = s.upper()
        if "NOOP".startswith(instruction):
            return TubeInstruction.NOOP
        elif "ADDX".startswith(instruction):
            return TubeInstruction.ADDX
        else:
            raise ValueError(f"Can't convert {s} to a TubeInstruction.")


class CathodeRayTube:
    def __init__(self):
        self._cycle: int
        self._x: int
        self._execution_counter: int
        self._instruction: Callable[[int], int]

        self._cycle = 1
        self._x = 1
        self._execution_counter = 0
        self._instruction = None

    @property
    def cycle(self) -> int:
        return self._cycle

    @property
    def x(self) -> int:
        return self._x

    def is_ready(self) -> bool:
        """Is the tube ready to receive the next instruction."""
        return self._execution_counter == 0

    def set_next_instruction(self,
                             instruction: TubeInstruction,
                             **kwargs
                             ) -> None:
        """Set the next instruction to be carried out by the tube."""

        if not self.is_ready():
            raise TubeNotReadyError()

        if instruction == TubeInstruction.ADDX:
            if 'x' not in kwargs.keys():
                raise ValueError("No x provided for addx.")
            amount = int(kwargs['x'])
            self._instruction = lambda x: x + amount
        else:
            self._instruction = lambda x: x

        self._execution_counter = instruction.cycles

    def next_cycle(self) -> None:
        """Advance one cycle."""
        if self._instruction is None:
            raise TubeNoInstructionError("Advancing cycle without set "
                                         "instruction")
        self._cycle += 1
        self._execution_counter -= 1

        if self._execution_counter == 0:
            self._x = self._instruction(self._x)
            self._instruction = None


class Day10(DayChallenge):
    """Advent of Code 2022 day 10"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 10

    def run(self, input_data: Path) -> None:
        data: list[str]

        with input_data.open() as file:
            data = file.read().split("\n")

        # PART 1
        # 20th, 60th, 100th, 140th, 180th,
        # and 220th cycles. What is the sum of these six signal strengths?
        print("Part 1:")
        check_at: list[int] = [20, 60, 100, 140, 180, 220]
        signal_strength_at_check: list[int] = list()
        instruction_line: int = 0
        instruction: TubeInstruction
        x_shift_amount: int
        tube: CathodeRayTube = CathodeRayTube()

        while tube.cycle <= check_at[-1]:
            if tube.cycle in check_at:
                signal_strength_at_check.append(tube.x * tube.cycle)
            if tube.is_ready():
                instruction, x_shift_amount = Day10.instruction_from_string(
                    data[instruction_line])
                tube.set_next_instruction(instruction, x=x_shift_amount)
                instruction_line += 1
            tube.next_cycle()

        print(f"sum of signal strengths: {sum(signal_strength_at_check)}")

        # PART 2
        print("\nPart 2:")

    @staticmethod
    def instruction_from_string(line: str) -> tuple[TubeInstruction, int]:
        """Convert a line of input to an instruction for the CathodeRayTube."""
        parts = line.split()
        instruction = TubeInstruction.from_string(parts[0])
        if instruction == TubeInstruction.NOOP:
            return instruction, 0
        else:
            amount = int(parts[1])
            return instruction, amount

