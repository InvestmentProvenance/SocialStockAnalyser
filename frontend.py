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


labels = {'abs_ln_percentage_return':'absolute % return', 'ln_percentage_return':'% return', 'volume':'volume', 'average_transaction_value':'average transaction value $','chat_volume':'chat volume','sentiment_difference':'absolute sentiment', 'average_sentiment_score':'average sentiment'}

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

LINK_STYLE = {
    'textAlign': 'center',
    'color': '#264ADA'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': 'a'
}

controls = dbc.FormGroup(
    [
        html.P('Ticker 1', style={
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
        html.P('Ticker 2', style={
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
        html.Br(),
        dbc.Button(
            id='clear_button',
            n_clicks=0,
            children='Clear graphs',
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
                        html.H4(id='card_title_1', children=['Feature calculations'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_1', children=['All the information about calculating features can be found in ', html.A(href='https://github.com/InvestmentProvenance/SocialStockAnalyser/blob/main/Descriptions.md', children=["descriptions.md"], style=LINK_STYLE)], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=5
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

"""
@app.callback(
    Output('content', 'children'),
    [Input('clear_button', 'n_clicks')],
    [State('content','children')
        ])
def clear_graphs(n_clicks, layout_content):
    cont = [
        html.H2('Analytics Dashboard', style=TEXT_STYLE),
        html.Hr(),
        content_first_row
    ]
    return cont
"""

def scatter_plot(series1 : pd.Series, series2 : pd.Series, col1 : str, col2 : str, 
                 series2_lag : int)-> go.Figure:
    """Returns a pair of objects that can then be used to make a scatter plot.
    You will need to call this function: 
    `px.scatter(scatter_plot(), x=<series1>.name, y=<series2>.name, 
                                                                    trendline="ols")`,
    replacing <series1> with the first arg to scatter_plot, 
         and <series2> with the second arg to scatter_plot.
    """
    series1.name = col1
    series2.name = col2
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
        extra = data.get_sampled_sentiment(ticker2_sns_data)
        df2 = data.calculate_sentiment_difference(extra)
    elif sns_options == "average_sentiment_score":
        df2 = data.get_average_sentiment_score(ticker2_sns_data)

    df1 = pd.DataFrame(df1)
    corr_lag = data.calculate_correlation_series(df1[stock_options], df2[sns_options])
    #Create dual bar chart
    trace1 = go.Scattergl(x=df1.index, y=df1[stock_options],mode='markers', name=ticker_option_1+" "+labels[stock_options], opacity=0.3)
    trace2 = go.Scattergl(x=df2.index,y=df2[sns_options], mode='markers', name=ticker_option_2+" "+ labels[sns_options], opacity=0.3)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(trace1)
    fig.add_trace(trace2,secondary_y=True)
    fig.update_yaxes(title_text=f"{labels[stock_options]}", secondary_y=False)
    fig.update_yaxes(title_text=f"{labels[sns_options]}", secondary_y=True)
    fig.update_layout()
    #Create Lag correlation graph
    print("head: ",corr_lag.head())

    spikes = []
    for time, corr in zip(corr_lag.Shift, corr_lag.Correlation):
        spikes.append( #Constructor information for each spike
            {'type':'line', 'xref':'x', 'yref':'y', 'x0':time, 'y0':0,
            'x1':time, 'y1':corr, 'line':{'color':'#636EFA', 'width':1}}
        )   

        #Add error bars to corr_lag
    get_confidence_interval = lambda corr : data.confidence_interval(corr, min(len(df1), len(df2)))
    intervals_obj = corr_lag.Correlation.apply(get_confidence_interval)
    abs_intervals = pd.DataFrame(list(intervals_obj), columns=['abs_lower', 'abs_upper'])
    rel_intervals = pd.concat([corr_lag.Correlation - abs_intervals.abs_lower,
                               abs_intervals.abs_upper - corr_lag.Correlation],
                               keys=['rel_lower', 'rel_upper'], axis=1)
    corr_lag = pd.concat([corr_lag, rel_intervals], axis=1)
    fig2 = px.scatter(corr_lag,x='Shift', y='Correlation',title='Lag correlation',
                      error_y="rel_upper", error_y_minus="rel_lower",
                      labels={'Shift':'Lag in minutes', 'Correlation':'Pearson correlation value'})
    fig2.update_layout(shapes=spikes) #Add spikes to scatter plot
    #Create phase space scatter graph with line of best fit
    fig3 = px.scatter(scatter_plot(df1,df2,stock_options,sns_options,0), x=df1.name, y=df2.name, trendline="ols", labels={stock_options:labels[stock_options], sns_options:labels[sns_options]}, title="Correlation at 0 lag")
    
    layout_content.append(dbc.Row(
    [
        dbc.Col(
            dcc.Graph(figure = fig), md=12
        ),
        dbc.Col(
            dcc.Graph(figure = fig2), md=12
        ),
        dbc.Col(
            dcc.Graph(figure = fig3), md=12
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


if __name__ == '__main__':
    app.run_server(port='8085')