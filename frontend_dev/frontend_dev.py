"""A playground for developing individual segments of the UI."""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..database import data
from datetime import datetime

def scatter_plot()-> go.Figure:
    """Returns a """
    ticker = "GME"
    start = datetime(2021,1,1)
    end = datetime(2021,1,30)
    sentiment = data.chat_volume(ticker, start, end)
    stock = data.price_volume(ticker, start, end)
    scatter = data.lag_join(stock, sentiment, 5)
    fig = px.scatter(scatter, x=stock.name, y=sentiment.name, trendline="ols")
    return fig


content = html.Div([], id="content")

fig = scatter_plot()

app = dash.Dash()
app.layout = html.Div([
    html.P("Graphs:"),
    dcc.Graph(figure=fig)
    ])


if __name__ == '__main__':
    app.run_server(port='8086')
