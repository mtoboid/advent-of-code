"""
--- Day 7: No Space Left On Device ---

You can hear birds chirping and raindrops hitting leaves as the expedition
proceeds. Occasionally, you can even hear much louder sounds in the distance;
how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its
communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the
resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

The filesystem consists of a tree of files (plain data) and directories (
which can contain other directories or files). The outermost directory is
called /. You can navigate around the filesystem, moving into or out of
directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you
executed, very much like some modern computers:

    cd means change directory. This changes which directory is the current
    directory, but the specific result depends on the argument:

        cd x moves in one level: it looks in the current directory for the
        directory named x and makes it the current directory.

        cd .. moves out one level: it finds the directory that contains the
        current directory, then makes that directory the current directory.

        cd / switches the current directory to the outermost directory, /.

    ls means list. It prints out all of the files and directories immediately
    contained by the current directory:

        123 abc means that the current directory contains a file named abc
        with size 123.

        dir xyz means that the current directory contains a directory named
        xyz.

Given the commands and output in the example above, you can determine that
the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

Here, there are four directories: / (the outermost directory), a and d (which
are in /), and e (which is in a). These directories also contain files of
various sizes.

Since the disk is full, your first step should probably be to find
directories that are good candidates for deletion. To do this, you need to
determine the total size of each directory. The total size of a directory is
the sum of the sizes of the files it contains, directly or indirectly. (
Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

    The total size of directory e is 584 because it contains a single file i
    of size 584 and no other directories.

    The directory a has total size 94853 because it contains files f (size
    29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a
    contains e which contains i).

    Directory d has total size 24933642.

    As the outermost directory, / contains every file. Its total size is
    48381165, the sum of the size of every file.

To begin, find all of the directories with a total size of at most 100000,
then calculate the sum of their total sizes. In the example above,
these directories are a and e; the sum of their total sizes is 95437 (94853 +
584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the
sum of the total sizes of those directories?


--- Part Two ---

Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least 30000000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

    Delete directory e, which would increase unused space by 584.
    Delete directory a, which would increase unused space by 94853.
    Delete directory d, which would increase unused space by 24933642.
    Delete directory /, which would increase unused space by 48381165.

Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from itertools import chain
from re import Pattern, compile

from adventofcode.challenge import DayChallenge, Path
from adventofcode.errors import AdventOfCodeError


class InputParsingError(AdventOfCodeError):
    pass


class FilesystemNode(ABC):
    """A node in a filesystem such as a file or a directory"""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the node."""
        pass

    @property
    @abstractmethod
    def size(self) -> int:
        """The size occupied in the filesystem."""
        pass

    @property
    @abstractmethod
    def parent(self) -> 'FilesystemNode' | None:
        """The parent of the node."""
        pass

    @property
    @abstractmethod
    def children(self) -> dict[str, 'FilesystemNode'] | None:
        """Children of the node"""
        pass

    @property
    @abstractmethod
    def has_children(self) -> bool:
        """Does this node have any children?"""
        pass


class File(FilesystemNode):
    """A file in a filesystem."""

    def __init__(self, name: str, size: int, parent: FilesystemNode):
        self._name: str
        self._size: int
        self._parent: FilesystemNode

        self._name = name
        self._size = size
        self._parent = parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        return self._size

    @property
    def parent(self) -> FilesystemNode:
        return self._parent

    @property
    def children(self) -> None:
        return None

    @property
    def has_children(self) -> bool:
        return False


class Directory(FilesystemNode):
    def __init__(self, name: str, parent: FilesystemNode):
        self._name: str
        self._parent: FilesystemNode
        self._children: dict[str, FilesystemNode]

        self._name = name
        self._parent = parent
        self._children = dict()

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        if not self.has_children:
            return 0
        return sum([x.size for x in self._children.values()])

    @property
    def parent(self) -> FilesystemNode:
        return self._parent

    @property
    def children(self) -> dict[str, FilesystemNode]:
        return self._children

    @property
    def has_children(self) -> bool:
        return len(self._children) > 0


class FilesystemRoot(Directory):
    def __init__(self):
        super().__init__(name="/", parent=self)

    @property
    def parent(self) -> None:
        return None


class Filesystem:
    def __init__(self):
        self._root: FilesystemRoot
        self._pwd: Directory

        self._root = FilesystemRoot()
        self._pwd = self._root

    @property
    def root(self) -> FilesystemRoot:
        return self._root

    @property
    def pwd(self) -> Directory:
        return self._pwd

    def mkdir(self, name: str) -> None:
        """Create a directory at the current location."""
        pwd = self._pwd
        if name in pwd.children.keys():
            raise ValueError(f"Node with name {name} already exists")
        pwd.children[name] = Directory(name=name, parent=pwd)

    def mkfile(self, name: str, size: int) -> None:
        """Create a file in the current directory."""
        if name in self.pwd.children.keys():
            raise ValueError(f"File with name {name} already exists.")
        self._pwd.children[name] = File(name=name, size=size, parent=self._pwd)

    def cd(self, location: str) -> None:
        """Change the pwd"""
        if location == '/':
            self._pwd = self._root

        elif location == '..':
            self._pwd = self._pwd.parent

        elif location in self.pwd.children.keys():
            loc = self.pwd.children[location]
            if not isinstance(loc, Directory):
                raise ValueError(f"{location} is not a directory.")
            self._pwd = loc

        else:
            raise ValueError(f"No such directory {location}")

    @staticmethod
    def get_all_subdirs(d: Directory) -> list[Directory]:
        """Get a list with all directories in the Filesystem."""
        child_dirs: list[Directory]
        child_dirs = [x for x in d.children.values()
                      if isinstance(x, Directory)]
        if len(child_dirs) < 1:
            return list()
        else:
            children = [Filesystem.get_all_subdirs(x) for x in child_dirs]
            child_dirs.extend(chain(*children))
            return child_dirs


class Day7(DayChallenge):
    """Advent of Code 2022 day 7"""

    @property
    def year(self) -> int:
        return 2022

    @property
    def day(self) -> int:
        return 7

    def run(self, input_data: Path) -> None:
        data: list[str]
        fs: Filesystem

        with input_data.open() as file:
            data = file.read().split("\n")

        # Build the Filesystem
        fs = Day7.filesystem_from_input(data)

        # PART 1
        print("Part 1:")
        # sum of directories <= 100000
        all_dirs = fs.get_all_subdirs(fs.root)
        all_dirs.sort(key=lambda x: x.size)
        dirs_of_interest = [x for x in all_dirs if x.size <= 100_000]
        total_size = sum([x.size for x in dirs_of_interest])
        print(f"The total sizes of dirs <= 100,000 is: {total_size}")

        # PART 2
        print("\nPart 2:")

    @staticmethod
    def filesystem_from_input(data: list[str]) -> Filesystem:
        """Parse input to a filesystem object."""
        cmd_pattern: Pattern = compile(r'\s*\$\s*(?P<cmd>\S+)'
                                       r'(?:\s+(?P<arg>\S+))?')

        fs: Filesystem = Filesystem()
        nodes_to_create: list[str]
        line_no: int = 0

        while line_no < len(data):
            m = cmd_pattern.match(data[line_no])
            if m is None:
                raise InputParsingError(f"No command found in line {line_no}")
            # cd
            if m.group("cmd") == 'cd':
                fs.cd(m.group("arg"))
                line_no += 1
            # ls
            elif m.group("cmd") == 'ls':
                nodes_to_create = list()
                line_no += 1
                ls_end: int = line_no
                while ls_end < len(data) and\
                      cmd_pattern.match(data[ls_end]) is None:
                    ls_end += 1
                Day7.create_nodes_in_pwd(data[line_no:ls_end], fs)
                line_no = ls_end
            else:
                raise InputParsingError(f"unknown command: {m.group('cmd')}")

        return fs

    @staticmethod
    def create_nodes_in_pwd(actions: list[str], fs: Filesystem) -> None:
        """Create files and directories specified in data in the pwd."""
        dir_pattern: Pattern = compile(r'\s*dir\s*(?P<name>\S+)')
        file_pattern: Pattern = compile(r'\s*(?P<size>\d+)\s*(?P<name>\S+)')

        for action in actions:
            if action == '':
                continue
            d = dir_pattern.match(action)
            f = file_pattern.match(action)
            if d is not None:
                fs.mkdir(name=d.group("name"))
            elif f is not None:
                fs.mkfile(name=f.group("name"), size=int(f.group("size")))
            else:
                raise InputParsingError(
                    f"Error parsing create action: {action}")

