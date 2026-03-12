import pandas as pd


def build_dashboard_dataframe(df):

    df = df.copy()

    df["created_at"] = pd.to_datetime(df["created_at"])

    return df

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
        "avg": media_scores if pd.notna(media_scores) else 0,
        "best": maior_score if pd.notna(maior_score) else 0,
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

    score_dist = df["score_distribuicao"].value_counts().sort_index()

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