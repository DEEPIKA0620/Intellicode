def map_features(basic_metrics, radon_metrics):

    features = {
        "loc": basic_metrics["loc"],

        "vg": radon_metrics["cyclomatic_complexity"],

        "evg": radon_metrics["cyclomatic_complexity"],

        "ivg": radon_metrics["cyclomatic_complexity"],

        "n": radon_metrics["program_length"],

        "v": radon_metrics["halstead_volume"],

        "l": 0,

        "d": radon_metrics["difficulty"],

        "i": 0,

        "e": radon_metrics["effort"],

        "b": radon_metrics["estimated_bugs"],

        "t": radon_metrics["time_required"],

        "locode": basic_metrics["logical_loc"],

        "locomment": basic_metrics["comment_lines"],

        "loblank": basic_metrics["blank_lines"],

        "loccodecomment": basic_metrics["logical_loc"] + basic_metrics["comment_lines"],

        "uniqop": 0,

        "uniqopnd": 0,

        "totalop": 0,

        "totalopnd": 0,

        "branchcount": radon_metrics["cyclomatic_complexity"]
    }

    return features

if __name__ == "__main__":

    basic_metrics = {
        "loc": 10,
        "blank_lines": 4,
        "comment_lines": 1,
        "logical_loc": 5
    }

    radon_metrics = {
        "cyclomatic_complexity": 1.0,
        "program_length": 6,
        "halstead_volume": 12.0,
        "difficulty": 0.67,
        "effort": 8.0,
        "estimated_bugs": 0.004,
        "time_required": 0.44
    }

    features = map_features(basic_metrics, radon_metrics)

    print(features)