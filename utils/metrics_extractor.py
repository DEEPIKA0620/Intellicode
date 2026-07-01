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
    if complexities:
          avg_cc = sum(block.complexity for block in complexities) / len(complexities)
    else:
         avg_cc = 0
    halstead = h_visit(code)

    if complexities:

        avg_complexity = sum(
            block.complexity
            for block in complexities
        ) / len(complexities)

    else:

        avg_complexity = 0

    metrics = {
    "cyclomatic_complexity": avg_cc,

    "program_length": h.total.length,

    "program_vocabulary": h.total.vocabulary,

    "halstead_volume": h.total.volume,

    "difficulty": h.total.difficulty,

    "effort": h.total.effort,

    "estimated_bugs": h.total.bugs,

    "time_required": h.total.time,

    "unique_operators": h.total.h1,

    "unique_operands": h.total.h2,

    "total_operators": h.total.N1,

    "total_operands": h.total.N2,

    "program_level": h.total.level,

    "intelligence": h.total.volume / h.total.difficulty if h.total.difficulty else 0
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