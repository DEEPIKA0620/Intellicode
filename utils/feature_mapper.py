def map_features(basic_metrics, radon_metrics):

    features = {

        # Size Metrics
        "loc": basic_metrics["loc"],
        "locode": basic_metrics["logical_loc"],
        "locomment": basic_metrics["comment_lines"],
        "loblank": basic_metrics["blank_lines"],
        "loccodecomment": basic_metrics["logical_loc"] + basic_metrics["comment_lines"],

        # Complexity Metrics
        "vg": radon_metrics["cyclomatic_complexity"],

        # NASA JM1 doesn't provide these directly.
        # We approximate them using Cyclomatic Complexity.
        "evg": radon_metrics["cyclomatic_complexity"],
        "ivg": radon_metrics["cyclomatic_complexity"],

        # Halstead Metrics
        "n": radon_metrics["program_length"],
        "v": radon_metrics["halstead_volume"],
        "l": radon_metrics["program_level"],
        "d": radon_metrics["difficulty"],
        "i": radon_metrics["intelligence"],
        "e": radon_metrics["effort"],
        "b": radon_metrics["estimated_bugs"],
        "t": radon_metrics["time_required"],

        # Operators / Operands
        "uniqop": radon_metrics["unique_operators"],
        "uniqopnd": radon_metrics["unique_operands"],
        "totalop": radon_metrics["total_operators"],
        "totalopnd": radon_metrics["total_operands"],

        # Branching
        "branchcount": radon_metrics["cyclomatic_complexity"]

    }

    return features