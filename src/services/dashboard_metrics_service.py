import pandas as pd


def calculate_dashboard_metrics(df):

    if df.empty:
        return {
            "total": 0,
            "avg": 0,
            "best": 0,
            "qualified": 0,
        }

    total_candidates = len(df)
    avg_score = df["score"].mean()
    best_score = df["score"].max()
    qualified = len(df[df["score"] >= 70])

    return {
        "total": total_candidates,
        "avg": avg_score,
        "best": best_score,
        "qualified": qualified,
    }


def calculate_score_distribution(df):

    bins = [0, 30, 50, 70, 85, 100]

    labels = [
        "Very Weak",
        "Weak",
        "Moderate",
        "Good",
        "Excellent",
    ]

    df = df.copy()

    df["score_category"] = pd.cut(
        df["score"],
        bins=bins,
        labels=labels,
    )

    score_dist = (
        df["score_category"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    score_dist.columns = ["score_category", "count"]

    return score_dist


def calculate_average_score_by_education(df):

    return (
        df[df["education_level"] != "Not Informed"]
        .groupby("education_level")["score"]
        .mean()
        .reset_index()
        .sort_values("score", ascending=False)
    )