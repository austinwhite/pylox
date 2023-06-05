from pathlib import Path
from sys import stderr
from lox.scanner import Scanner
from lox.parser import Parser
from lox.interpreter import Interpreter, LoxRuntimeError
from lox.ast_printer import AstPrinter


class Lox:
    interpreter = Interpreter()
    had_error = False
    had_runtime_error = False

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

        if Lox.had_runtime_error:
            exit(70)

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

    @classmethod
    def run(cls, source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()

        if cls.had_error:
            return None

        Lox.interpreter.interpret(expression)

        print(AstPrinter().print(expression))

    @staticmethod
    def error(line: int, message: str) -> None:
        Lox.report(line, "", message)

    @staticmethod
    def runtime_error(error: LoxRuntimeError) -> None:
        stderr.write(f"{error}\n[line {error.token.line}]")
        Lox.had_runtime_error = True

    @classmethod
    def report(cls, line: int, where: str, message: str) -> None:
        error_message = "".join([
            "[line ", str(line), "] Error", where, ": ", message])

        stderr.write(error_message)
        cls.had_error = True
