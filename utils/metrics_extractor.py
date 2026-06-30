import ast


def extract_basic_metrics(file_path):
    """
    Extract basic software metrics from a Python file.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()

    lines = code.splitlines()

    # Total Lines of Code
    loc = len(lines)

    # Blank lines
    blank_lines = sum(
        1 for line in lines
        if line.strip() == ""
    )

    # Comment lines
    comment_lines = sum(
        1 for line in lines
        if line.strip().startswith("#")
    )

    # Logical LOC
    logical_loc = (
        loc
        - blank_lines
        - comment_lines
    )

    tree = ast.parse(code)

    functions = sum(
        isinstance(node, ast.FunctionDef)
        for node in ast.walk(tree)
    )

    classes = sum(
        isinstance(node, ast.ClassDef)
        for node in ast.walk(tree)
    )

    imports = sum(
        isinstance(node, (ast.Import, ast.ImportFrom))
        for node in ast.walk(tree)
    )

    metrics = {
        "loc": loc,
        "blank_lines": blank_lines,
        "comment_lines": comment_lines,
        "logical_loc": logical_loc,
        "functions": functions,
        "classes": classes,
        "imports": imports
    }

    return metrics
if __name__ == "__main__":

    metrics = extract_basic_metrics(
        "test_files/sample.py"
    )

    print(metrics)