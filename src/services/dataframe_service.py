import pandas as pd

def analyses_to_dataframe(analyses):

    data = [
        {
            "score": a.score,
            "languages": a.languages,
            "strengths": a.strengths,
            "weaknesses": a.weaknesses,
            "opinion": a.opinion,
            "education_level": a.education_level.name,
            "created_at": a.created_at,
            "file_path": a.resume.file_path
        }
        for a in analyses
    ]

    return pd.DataFrame(
        data,
        columns=[
            "score",
            "languages",
            "strengths",
            "weaknesses",
            "opinion",
            "education_level",
            "created_at",
            "file_path"
        ]
    )