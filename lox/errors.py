from sys import stderr


class Error:
    had_error = False

    @staticmethod
    def error(line_number: int, message: str) -> None:
        Error.report(line_number, "", message)

    @staticmethod
    def report(line_number: int, where: str, message: str) -> None:
        print("[line " + str(line_number) + "] Error" +
              where + ": " + message, file=stderr)
