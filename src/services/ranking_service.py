from src.config.settings import TOP_CANDIDATES_LIMIT, SUPABASE_BUCKET


def build_resume_url(file_path: str, supabase_url: str) -> str:
    return f"{supabase_url}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_path}"


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
        lambda x: build_resume_url(x, supabase_url)
    )

    return df[
        ["Score", "Languages", "Strengths", "Weaknesses", "Resume"]
    ].sort_values(by="Score", ascending=False)


def prepare_top_candidates(
    df,
    supabase_url,
    limit=TOP_CANDIDATES_LIMIT
):

    if df.empty:
        return df

    df = df.copy()

    df["resume"] = df["file_path"].apply(
        lambda x: build_resume_url(x, supabase_url)
    )

    df = df.sort_values("score", ascending=False)

    return df.head(limit)