from cProfile import Profile
from pstats import Stats, SortKey

from adventofcode.year_2022 import CHALLENGES_2022


def main():
    #with Profile() as profile:
    CHALLENGES_2022.run(16)

    # summary = Stats(profile)
    # summary.sort_stats(SortKey.TIME)
    # summary.print_stats()
    # summary.dump_stats("day_12_a-star.prof")


if __name__ == '__main__':
    main()
