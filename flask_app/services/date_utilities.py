from datetime import datetime, timedelta
import pandas as pd


def get_week_start(dt):
    return dt - timedelta(days=dt.weekday())


def get_month_start(dt):
    return dt.replace(day=1)


def add_dates_to_df(df):
    df["date"] = pd.to_datetime(df['date'])
    df["week"] = df["date"].apply(lambda x: get_week_start(x))
    df["month"] = df["date"].apply(lambda x: get_month_start(x))
    return df
