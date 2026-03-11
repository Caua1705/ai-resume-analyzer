import pandas as pd

def analyses_to_dataframe(analyses):

    data = [
        {
            "score": a.score,
            "languages": a.languages,
            "strengths": a.strengths,
            "weaknesses": a.weaknesses,
            "opinion": a.opinion,
            "created_at": a.created_at
        }
        for a in analyses
    ]

    return pd.DataFrame(data)