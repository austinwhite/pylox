from pathlib import Path
from sys import stderr
from lox.scanner import Scanner


class Lox:
    had_error = False

    @staticmethod
    def print_repl_intro() -> str:
        return f"repl intro: placeholder"

    @staticmethod
    def run_file(file_path: str) -> None:
        absolute_path = Path(file_path).resolve()
        source = absolute_path.read_text()

        Lox.run(source)

        if Lox.had_error:
            exit(65)

    @staticmethod
    def run_repl() -> None:
        print(Lox.print_repl_intro())

        while True:
            try:
                print(">>> ", end='')

                source = input()
                Lox.run(source)

                Lox.had_error = False

            except KeyboardInterrupt:
                print("\nKeyboardInterupt")
            except EOFError:
                print("\n")
                exit(1)

    @staticmethod
    def run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    @staticmethod
    def error(line: int, message: str) -> None:
        Lox.report(line, "", message)

    @classmethod
    def report(cls, line: int, where: str, message: str) -> None:
        error_message = "".join([
            "[line ", str(line), "] Error", where, ": ", message])

        stderr.write(error_message)
        cls.had_error = True
