from typing import Any
from lox.tokens import Token

class Environment:
    def __init__(self) -> None:
        self._values = {}

    @property
    def values(self) -> None:
        return self._values

    @values.setter
    def values(self, name: Token, value: Any) -> None:
        self._values[name] = value

    @values.deleter
    def values(self, name: Token) -> None:
        del self._values[name]

    @values.getter
    def values(self, name: Token) -> Any:
        try:
            return self._values[name]
        except RuntimeError:
            raise RuntimeError(f"Undefined varible '{name.lexeme} '.")
