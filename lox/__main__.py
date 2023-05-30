from sys import argv
from lox import Lox


def main(args) -> None:
    if len(args) > 1:
        Lox.usage(64)
    elif len(args) == 1:
        Lox.run_file(args[0])
    else:
        Lox.run_prompt()


main(argv[1:])
