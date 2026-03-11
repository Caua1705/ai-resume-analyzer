import pandas as pd


def build_ranking_dataframe(df):

    df = df.copy()

    df["Languages"] = df["languages"].apply(
        lambda x: ", ".join(x) if x else "Not specified"
    )

    df["Strengths"] = df["strengths"].apply(
        lambda x: x[:80] + "..." if x and len(x) > 80 else x
    )

    df["Weaknesses"] = df["weaknesses"].apply(
        lambda x: x[:80] + "..." if x and len(x) > 80 else x
    )

    df["Created"] = pd.to_datetime(df["created_at"]).dt.strftime("%d/%m/%Y %H:%M")

    df = df.rename(columns={"score": "Score"})

    return df[
        ["Score", "Languages", "Strengths", "Weaknesses", "Created"]
    ].sort_values(by="Score", ascending=False)