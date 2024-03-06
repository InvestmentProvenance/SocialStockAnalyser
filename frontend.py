import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import datetime
from datetime import date
from datetime import timedelta
from database import data
import pandas as pd

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

controls = dbc.FormGroup(
    [
        html.P('Ticker', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='ticker_1',
            options=[{
                'label': 'GME',
                'value': 'GME'
            }, {
                'label': 'NIO',
                'value': 'NIO'
            },
            {
                "label":"AMC",
                "value":"AMC"
            }
            ],
            value='GME',  # default value
            multi=False
        ),
        html.Br(),
        html.P('Ticker', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='ticker_2',
            options=[{
                'label': 'GME',
                'value': 'GME'
            }, {
                'label': 'NIO',
                'value': 'NIO'
            },
            {
                "label":"AMC",
                "value":"AMC"
            }
            ],
            value='AMC',  # default value
            multi=False
        ),
        html.Br(),
        html.P('Time range', style={
            'textAlign': 'center'
        }),
        dcc.DatePickerRange(id="time_range",month_format='MMM Do, YY',end_date_placeholder_text='MMM Do, YY',start_date=date(2020, 2, 1),end_date=date(2022, 2, 1), with_portal=True, style={
                'margin': 'auto'
            }),
        html.Br(),
        html.P('Ticker 1 options', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='stock_options',
            options=[{
                'label': 'absolute percentage return',
                'value': 'abs_ln_percentage_return'
            },
                {
                    'label': 'percentage return',
                    'value': 'ln_percentage_return'
                },
                {
                    'label': 'volume',
                    'value': 'volume'
                },
                {
                    'label': 'average transaction value',
                    'value': 'average_transaction_value'
                }
            ],
            value= 'abs_ln_percentage_return',
            style={
                'margin': 'auto'
            }
        )]),
        html.P('Ticker 2 options', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='sns_options',
            options=[{
                'label': 'Chat volume',
                'value': 'chat_volume'
            }, {
                'label': 'aggregate sentiment',
                'value': 'sentiment_difference'
            },
            {
                'label': 'average sentiment',
                'value': 'average_sentiment_score'
            }
            ],
            value='chat_volume',
            style={
                'margin': 'auto'
            }
        )]),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Add graph',
            color='primary',
            block=True
        ),
    ]
)

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['GME stock'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_1', children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4('Calculations info', className='card-title', style=CARD_TEXT_STYLE),
                        html.P('Price change - |log(price_N-1/price_N)| ...', style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    )
])





content = html.Div(
    [
        html.H2('Analytics Dashboard', style=TEXT_STYLE),
        html.Hr(),
        content_first_row
    ],
    style=CONTENT_STYLE,
    id="content"
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])


def scatter_plot(series1 : pd.Series, series2 : pd.Series, col1 : str, col2 : str, 
                 series2_lag : int)-> go.Figure:
    """Returns a pair of objects that can then be used to make a scatter plot.
    You will need to call this function: 
    `px.scatter(scatter_plot(), x=<series1>.name, y=<series2>.name, 
                                                                    trendline="ols")`,
    replacing <series1> with the first arg to scatter_plot, 
         and <series2> with the second arg to scatter_plot.
    """
    series1.name = col1.name
    series2.name = col2.name
    pairs = data.lag_join(series1, series2, series2_lag)
    return pairs

@app.callback(
    Output('content', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('content','children'), State('ticker_1','value'), State('ticker_2','value'), State('stock_options','value'), State('sns_options','value'), State('time_range','start_date'), State('time_range','end_date')
        ])
def add_graph(n_clicks,layout_content, ticker_option_1, ticker_option_2,stock_options, sns_options, start_date, end_date):
    print(ticker_option_1)
    print(start_date)
    print(end_date)
    # Need to get data for each ticker first
    ticker1_stock_data = data.get_data(ticker_option_1, start_date, end_date)
    ticker2_sns_data = data.get_sns_data(ticker_option_2, start_date, end_date)

    df1 = None
    df2 = None

    if stock_options == "abs_ln_percentage_return":
        df1 = data.calculate_abs_ln_percentage_return(ticker1_stock_data)
    elif stock_options == "ln_percentage_return":
        df1 = data.calculate_ln_percentage_return(ticker1_stock_data)
    elif stock_options == "average_transaction_value":
        df1 = data.calculate_average_transaction_value(ticker1_stock_data)
    elif stock_options == "volume":
        df1 = data.get_volume(ticker1_stock_data)
    if sns_options == "chat_volume":
        df2 = data.get_sns_chat_volume(ticker2_sns_data)
    elif sns_options == "sentiment_difference":
        df2 = data.get_sampled_sentiment(ticker2_sns_data)
        df2 = data.calculate_sentiment_difference(ticker2_sns_data)
    elif sns_options == "average_sentiment_score":
        df2 = data.get_average_sentiment_score(ticker2_sns_data)

    df1 = pd.DataFrame(df1)
    corr_lag = data.calculate_correlation_series(df1[stock_options], df2[sns_options])

    trace1 = go.Scatter(x=df1.index, y=df1[stock_options], name=stock_options)
    trace2 = go.Line(x=df2.index,y=df2[sns_options], name=sns_options)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(trace1)
    fig.add_trace(trace2,secondary_y=True)

    print("head: ",corr_lag.head())
    fig2 = px.line(corr_lag,x='Shift', y='Correlation',title='Lag correlation', labels={'Shift':'Lag in minutes', 'Correlation':'Pearson correlation value'})

    layout_content.append(dbc.Row(
    [
        dbc.Col(
            dcc.Graph(figure = fig), md=12
        ),
        dbc.Col(
            dcc.Graph(figure = fig2), md=12
        )
        ])
        )
    print("added layout")
    return layout_content

"""
@app.callback(
    Output('graph_1', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('ticker_1', 'value'), State('time_range', 'value'), State('stock_options', 'value'),
     State('sns_options', 'value')
     ])
def update_graph_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print("n clikcs:", n_clicks)
    print("dropdown:", dropdown_value)
    end_date = datetime.datetime(2022, 4,29)
    start_date = end_date - timedelta(days=600)  # 30 days per month approximation
    prices = data.get_data(ticker='GME',start_time=start_date, end_time=end_date)
    df = prices['open'].pct_change().to_frame()
    df = df.dropna()
    fig = px.line(df)

    return fig
"""


@app.callback(
    Output('card_title_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('ticker_1', 'value'), State('range_slider', 'value'), State('stock_options', 'value'),
     State('sns_options', 'value')
     ])
def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    return dropdown_value[0]


@app.callback(
    Output('card_text_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('ticker_1', 'value'), State('range_slider', 'value'), State('stock_options', 'value'),
     State('sns_options', 'value')
     ])
def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    return 'info about ' + dropdown_value[0]


if __name__ == '__main__':
    app.run_server(port='8085')