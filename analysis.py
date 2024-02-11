"""Does statistical analysis"""
from typing import List, Tuple
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

COMMENTS_DATA = "wallstreetbets-posts-and-comments-for-august-2021-comments.csv"
STOCK_DATA = ""

def get_comment_table():
    """Returns a dataframe of the commment table. It has the timestamp, comment body and sentiment scores.
    Records without a """
    df = pd.read_csv(COMMENTS_DATA)
    df.datetime = pd.to_datetime(df.created_utc) #pick certain columns
    df = df[['datetime', 'body', 'sentiment']] #pick certain columns
    df =  df[df.sentiment.notna()] #extract rows with existing sentiment scores
    return df

def get_market_sentiment(table : pd.DataFrame):#, start_time=None : datetime, end_time=None:datetime) ->  List[Tuple[datetime, int]]:
    """Gets the market sentiment from the given start to end times, and returns a list
    of (timestamp, sentiment) pairs."""
    gme_mentions = table.body.str.contains("GME", case=False)
    gamestop_mentions = table.body.str.contains("gamestop", case=False)
    return table[gamestop_mentions | gme_mentions]
    


def graph_time_series(series1, series2)->None:
    """Graphs 2 """
    plt
    pass

comments : pd.DataFrame = get_market_sentiment(get_comment_table()) 
# comments.created_utc = pd.to_datetime(comments.created_utc)
plt.scatter(comments.datetime, comments.sentiment)
# plt.gca().xaxis.set_major_formatter(mdates.ConciseDateFormatter('%Y-%m-%d'))
plt.show()