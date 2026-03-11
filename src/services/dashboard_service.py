import pandas as pd


def build_dashboard_dataframe(df):

    df = df.copy()

    df["created_at"] = pd.to_datetime(df["created_at"])

    return df