import ast
import os
from radon.raw import analyze
from radon.complexity import cc_visit
from radon.metrics import h_visit

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

def extract_radon_metrics(code):

    complexities = cc_visit(code)
    halstead = h_visit(code)

    if complexities:

        avg_complexity = sum(
            block.complexity
            for block in complexities
        ) / len(complexities)

    else:

        avg_complexity = 0

    metrics = {
    "cyclomatic_complexity": round(avg_complexity, 2),

    "program_length": halstead.total.length,
    "program_vocabulary": halstead.total.vocabulary,
    "halstead_volume": round(halstead.total.volume, 2),
    "difficulty": round(halstead.total.difficulty, 2),
    "effort": round(halstead.total.effort, 2),
    "estimated_bugs": round(halstead.total.bugs, 4),
    "time_required": round(halstead.total.time, 2)
}
    
    return metrics
if __name__ == "__main__":

    file_path = "test_files/sample.py"

    basic_metrics = extract_basic_metrics(file_path)

    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()

    radon_metrics = extract_radon_metrics(code)

    print("Basic Metrics:")
    print(basic_metrics)

    print("\nRadon Metrics:")
    print(radon_metrics)