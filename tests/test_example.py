"""Example of how to write tests"""
from ..database import db_stock
#test file must start with 'test_'

def test_answer():
    """Example test"""
    assert True


def test_list():
    print(db_stock.comment_tickers())

if __name__ == "__main__":
    test_list()