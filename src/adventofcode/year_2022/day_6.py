"""
--- Day 6: Tuning Trouble ---

The preparations are finally complete; you and the Elves leave camp on foot
and begin to make your way toward the star fruit grove.

As you move through the dense undergrowth, one of the Elves gives you a
handheld device. He says that it has many fancy features, but the most
important one to set up right now is the communication system.

However, because he's heard you have significant experience dealing with
signal-based systems, he convinced the other Elves that it would be okay to
give you their one malfunctioning device - surely you'll have no problem
fixing it.

As if inspired by comedic timing, the device emits a few colorful sparks.

To be able to communicate with the Elves, the device needs to lock on to
their signal. The signal is a series of seemingly-random characters that the
device receives one at a time.

To fix the communication system, you need to add a subroutine to the device
that detects a start-of-packet marker in the datastream. In the protocol
being used by the Elves, the start of a packet is indicated by a sequence of
four characters that are all different.

The device will send your subroutine a datastream buffer (your puzzle input);
your subroutine needs to identify the first position where the four most
recently received characters were all different. Specifically, it needs to
report the number of characters from the beginning of the buffer to the end
of the first such four-character marker.

For example, suppose you receive the following datastream buffer:

mjqjpqmgbljsphdztnvjfqwrcgsmlb

After the first three characters (mjq) have been received, there haven't been
enough characters received yet to find the marker. The first time a marker
could occur is after the fourth character is received, making the most recent
four characters mjqj. Because j is repeated, this isn't a marker.

The first time a marker appears is after the seventh character arrives. Once
it does, the last four characters received are jpqm, which are all different.
In this case, your subroutine should report the value 7, because the first
start-of-packet marker is complete after 7 characters have been processed.

Here are a few more examples:

    bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 5
    nppdvjthqldpwncqszvftbrmjlhg: first marker after character 6
    nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 10
    zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 11

How many characters need to be processed before the first start-of-packet
marker is detected?

"""

from adventofcode.challenge import DayChallenge, Path


class Day6(DayChallenge):
    """Advent of Code 2022 day 6"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 6

    def run(self, input_data: Path) -> None:
        data: str

        with input_data.open() as file:
            data = file.read()

        # PART 1
        print("Part 1:")
        pos_first_marker: int
        pos_first_marker = Day6.first_pos_all_different(data, 4)
        print(f"{pos_first_marker} characters need to be processed.")


        # PART 2
        print("\nPart 2:")

    @staticmethod
    def all_letters_different(s: str) -> bool:
        """Are all letters in the string s different?"""

        letters: set[str] = set(s)
        return len(letters) == len(s)

    @staticmethod
    def first_pos_all_different(data: str, n: int):
        """
        Determine the position (end) of the first occurrence of a sequence of n
        letters in data where all of them are different.
        If no such position can be found -1 is returned.
        """

        pos: int
        current_seq: str

        pos = n
        current_seq = data[:pos]
        while not Day6.all_letters_different(current_seq):
            pos += 1
            if pos > len(data):
                return -1
            current_seq = data[pos-n:pos]
        return pos
