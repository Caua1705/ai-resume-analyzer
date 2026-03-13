def build_ranking_dataframe(df, supabase_url):

    df = df.copy()

    df["Languages"] = df["languages"].apply(
        lambda x: ", ".join(x) if x else "Not specified"
    )

    df["Strengths"] = df["strengths"].apply(
        lambda x: x[:80] + "..." if len(x) > 80 else x
    )

    df["Weaknesses"] = df["weaknesses"].apply(
        lambda x: x[:80] + "..." if len(x) > 80 else x
    )

    df = df.rename(columns={"score": "Score"})

    df["Resume"] = df["file_path"].apply(
        lambda x: f"{supabase_url}/storage/v1/object/public/curriculos/{x}"
    )
    return df[
        ["Score", "Languages", "Strengths", "Weaknesses", "Resume"]
    ].sort_values(by="Score", ascending=False)


def preparar_top_candidates(df, supabase_url, limit=3):

    if df.empty:
        return df

    df = df.copy()

    df["resume"] = df["file_path"].apply(
        lambda x: f"{supabase_url}/storage/v1/object/public/curriculos/{x}"
    )

    df = df.sort_values("score", ascending=False)

    return df.head(limit)