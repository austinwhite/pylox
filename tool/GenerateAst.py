from typing import List, TextIO, Dict
from sys import argv, stderr
from pathlib import Path


def write_imports(writer: TextIO, imports: Dict) -> None:
    for module, members in imports.items():
        writer.write(f"from {module} import {members}\n")

    writer.write("\n\n")


def write_ast(output_dir: Path, base_name: str, imports: Dict, types: List[str]) -> None:
    path = (output_dir / base_name.lower()).with_suffix(".py")
    writer = open(path, "w", encoding="UTF-8")

    write_imports(writer, imports)
    define_ast(writer, base_name, types)


def define_ast(writer: TextIO, base_name: str, types: List[str]) -> None:
    writer.write("__all__ = [\n")
    writer.write(f"    \"{base_name}Visitor\",\n")
    writer.write(f"    \"{base_name}\",\n")
    for type in types:
        class_name = type.split(":", maxsplit=1)[0].strip()
        writer.write(f"    \"{class_name}\"\n")
    writer.write("]")

    writer.write("\n\n")
    define_visitor(writer, base_name, types)
    writer.write("\n")

    writer.write(f"class {base_name}(ABC):\n")
    writer.write(f"    @abstractmethod\n")
    writer.write(
        f"    def accept(self, visitor: {base_name}Visitor) -> None:\n")
    writer.write(f"        pass\n")

    for type in types:
        writer.write("\n\n")
        class_name = type.split(':', maxsplit=1)[0].strip()
        instance_vars = type.split(':', maxsplit=1)[1].strip()
        define_type(writer, base_name, class_name, instance_vars)


def define_visitor(writer: TextIO, base_name: str, types: List[str]) -> None:
    writer.write(f"class {base_name}Visitor(ABC):\n")

    for type in types:
        type_name = type.split(':', maxsplit=1)[0].strip()
        writer.write(f"    @abstractmethod\n")
        writer.write(
            f"    def visit_{type_name.lower()}_{base_name.lower()}(self, {base_name.lower()}) -> None:\n")
        writer.write(f"        pass\n\n")


def define_type(writer: TextIO, base_name: str, class_name: str, instance_vars: str) -> None:
    writer.write(f"class {class_name}({base_name}):\n")
    writer.write(f"    def __init__(self, {instance_vars}) -> None:\n")

    vars = instance_vars.split(", ")
    for var in vars:
        var = var.split(": ")[0]
        writer.write(f"        self.{var} = {var}\n")

    writer.write("\n")
    writer.write(
        f"    def accept(self, visitor: {base_name}Visitor) -> ExpressionVisitor:\n")
    writer.write(
        f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n")


def main(args) -> None:
    if len(args) > 1:
        stderr.write("Usage: GenerateAst.py <output directory>")
        exit(64)

    output_file = Path(args[0]).resolve()

    write_ast(output_file, "Expression",
              {"abc": "ABC, abstractmethod", "lox.tokens": "Token", "typing": "Any"},
              [
                  'Assign   : name: Token, value: Expression',
                  'Binary   : left: Expression, operator: Token, right: Expression',
                  'Grouping : expression: Expression',
                  'Literal  : value: Any',
                  'Unary    : operator: Token, right: Expression',
                  'Variable : name: Token',
              ])


if __name__ == "__main__":
    main(argv[1:])
