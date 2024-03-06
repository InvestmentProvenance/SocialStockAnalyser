"""Example of how to write tests"""
from datetime import datetime
from ..database import db_stock
from ..database import data

#test file must start with 'test_'

def test_answer():
    """Example test"""
    assert True


def test_list():
    print(db_stock.comment_tickers())

def test_scatter_graph():
    ticker = "GME"
    start = datetime(2021,1,1)
    end = datetime(2021,1,30)
    sentiment = data.chat_volume(ticker, start, end)
    stock = data.price_volume(ticker, start, end)
    scatter = data.lag_join(stock, sentiment, 5)
    print("blah")

if __name__ == "__main__":
    test_scatter_graph()
