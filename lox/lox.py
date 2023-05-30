from pathlib import Path
from sys import stderr

from lox.scanner import Scanner
from lox.errors import Error


class Lox:
    @staticmethod
    def run_file(filename: str) -> None:
        path = Path(filename).absolute()
        source = path.read_text()

        Lox.run(source)

        if Error.had_error:
            exit(65)

    @staticmethod
    def run_prompt() -> None:
        while True:
            try:
                print("> ", end='')

                source = input()

                if not source:
                    break

                Lox.run(source)
                Error.had_error = False
            except KeyboardInterrupt:
                exit(0)

    @staticmethod
    def run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    @staticmethod
    def usage(error_code: int) -> None:
        print("Usage: lox [script]", file=stderr)
        exit(error_code)
