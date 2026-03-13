import pandas as pd


def calcular_metricas_dashboard(df):

    if df.empty:
        return {
            "total": 0,
            "avg": 0,
            "best": 0,
            "qualified": 0
        }

    total_candidatos = len(df)
    media_scores = df["score"].mean()
    maior_score = df["score"].max()
    qualificados = len(df[df["score"] >= 70])

    return {
        "total": total_candidatos,
        "avg": media_scores,
        "best": maior_score,
        "qualified": qualificados
    }


def calcular_score_distribution(df):

    bins = [0, 30, 50, 70, 85, 100]

    labels = [
        "Very Weak",
        "Weak",
        "Moderate",
        "Good",
        "Excellent"
    ]

    df = df.copy()

    df["score_distribuicao"] = pd.cut(
        df["score"],
        bins=bins,
        labels=labels
    )

    score_dist = (
        df["score_distribuicao"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    score_dist.columns = ["score_category", "count"]

    return score_dist


def calcular_media_por_educacao(df):

    media = (
        df[df["education_level"] != "Not Informed"]
        .groupby("education_level")["score"]
        .mean()
        .reset_index()
        .sort_values("score", ascending=False)
    )

    return media