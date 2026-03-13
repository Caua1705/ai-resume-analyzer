import pandas as pd


def analyses_to_dataframe(analyses):

    columns = [
        "score",
        "languages",
        "strengths",
        "weaknesses",
        "opinion",
        "education_level",
        "created_at",
        "file_path",
    ]

    data = [
        {
            "score": a.score,
            "languages": a.languages,
            "strengths": a.strengths,
            "weaknesses": a.weaknesses,
            "opinion": a.opinion,
            "education_level": a.education_level.name if a.education_level else None,
            "created_at": a.created_at,
            "file_path": a.resume.file_path if a.resume else None,
        }
        for a in analyses
    ]

    return pd.DataFrame(data, columns=columns)