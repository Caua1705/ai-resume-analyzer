import pandas as pd

from src.config.settings import QUALIFIED_SCORE_THRESHOLD


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
    qualified = len(df[df["score"] >= QUALIFIED_SCORE_THRESHOLD])

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

    if df.empty:
        return pd.DataFrame({
            "education_level": [],
            "score": []
        })

    df = df.copy()

    df["score"] = pd.to_numeric(df["score"], errors="coerce")

    return (
        df[df["education_level"] != "Not Informed"]
        .groupby("education_level")["score"]
        .mean()
        .reset_index()
        .sort_values("score", ascending=False)
    )