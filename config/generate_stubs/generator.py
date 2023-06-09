"""
Generator of stubs for existing lab implementation
"""
import ast
from _ast import alias, stmt
from pathlib import Path
from typing import Optional

import ast_comments
from tap import Tap


class NoDocStringForAMethodError(Exception):
    """
    Error for a method that lacks docstring
    """


def remove_implementation_from_function(original_declaration: ast.stmt,
                                        parent: Optional[ast.ClassDef] = None) -> None:
    """
    Remove reference implementation
    """
    if not isinstance(original_declaration, ast.FunctionDef):
        return
    # print(ast.dump(ast.parse("raise NotImplementedError()"), annotate_fields=False, indent=4))
    expr = original_declaration.body[0]
    if not isinstance(expr, ast.Expr) and \
            (
                    not hasattr(expr, 'value') or
                    not isinstance(getattr(expr, 'value'), ast.Constant)
            ):
        raise NoDocStringForAMethodError(f'You have to provide docstring for a method '
                                         f'{parent.name + "." if parent is not None else ""}'
                                         f'{original_declaration.name}')
    original_declaration.body[1:] = []


# pylint: disable=too-many-branches
def cleanup_code(source_code_path: Path) -> str:
    """
    Removing implementation based on AST parsing of code
    """
    with source_code_path.open(encoding='utf-8') as file:
        data = ast.parse(file.read(), source_code_path.name, type_comments=True)

    with source_code_path.open(encoding='utf-8') as file:
        data_2 = ast_comments.parse(file.read(), source_code_path.name)

    accepted_modules: dict[str, list[str]] = {'typing': ['*']}

    new_decl: list[stmt] = []

    for decl_2 in data_2.body:
        if isinstance(decl_2, ast_comments.Comment):
            data.body.insert(data_2.body.index(decl_2), decl_2)  # type: ignore

    for decl in data.body:
        if isinstance(decl, (ast.Import, ast.ImportFrom)):
            if (module_name := getattr(decl, 'module', None)) is None:
                module_name = decl.names[0].name

            if module_name not in accepted_modules:
                continue

            if isinstance(decl, ast.ImportFrom):
                accepted_names = accepted_modules.get(module_name, [])
                names_to_import = [name for name in decl.names if name.name
                                   in accepted_names or '*' in accepted_names]

                if not names_to_import:
                    continue

                new_decl.append(ast.ImportFrom(module=module_name,
                                               names=[alias(name=name.name)
                                                      for name in names_to_import]))
                continue

        if isinstance(decl, ast.ClassDef):
            if 'Note: remove' in ast.get_docstring(decl):  # type: ignore
                decl = []  # type: ignore
            else:
                for ind, class_decl in enumerate(decl.body):
                    if isinstance(class_decl, ast.FunctionDef) \
                            and 'Note: remove' in ast.get_docstring(class_decl):  # type: ignore
                        decl.body[ind] = []  # type: ignore

        if isinstance(decl, ast.ClassDef) and decl.bases:
            name = decl.bases[0]
            if decl.bases and isinstance(name, ast.Name) and \
                    hasattr(name, 'id') and \
                    getattr(name, 'id') == 'Exception':
                decl = []  # type: ignore

        if isinstance(decl, ast.ClassDef):
            for class_decl in decl.body:
                remove_implementation_from_function(class_decl, parent=decl)
        remove_implementation_from_function(decl)
        new_decl.append(decl)

    data.body = list(new_decl)
    return ast_comments.unparse(data)  # type: ignore


class ArgumentParser(Tap):
    """
    Types for CLI interface of a module
    """
    source_code_path: str
    target_code_path: str


def main() -> None:
    """
    Entrypoint for stub generation
    """
    args = ArgumentParser().parse_args()

    res_stub_path = Path(args.target_code_path)
    res_stub_path.parent.mkdir(parents=True, exist_ok=True)

    source_code = cleanup_code(Path(args.source_code_path))

    with res_stub_path.open(mode='w', encoding='utf-8') as file:
        print(f'Writing to {res_stub_path}')
        file.write(source_code)


if __name__ == '__main__':
    main()
