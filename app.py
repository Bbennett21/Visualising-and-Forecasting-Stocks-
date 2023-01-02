import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from datetime import datetime as dt
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


app = dash.Dash(__name__, external_stylesheets=['assets\styles.css'])
server = app.server



item1 = html.Div(
    [
        html.P("Welcome to the Stock Dash App!", className="start"),

        html.Div([
            # stock code input
            dcc.Input(id='stock-code', type='text', placeholder='Enter stock code'),
            html.Button('Submit', id='submit-button')
        ], className="stock-input"),

        html.Div([
            # Date range picker input
            dcc.DatePickerRange(
                id='date-range', start_date=dt(2020, 1, 1).date(), end_date=dt.now().date(), className= 'date-input')
        ]),
        html.Div([
            # Stock price button
            html.Button('Get Stock Price', id='stock-price-button'),

            # Indicators button
            html.Button('Get Indicators', id='indicators-button'),

            # Number of days of forecast input
            dcc.Input(id='forecast-days', type='number', placeholder='Enter number of days'),

            # Forecast button
            html.Button('Get Forecast', id='forecast-button')
        ], className="selectors")
    ],
    className="nav")

item2 = html.Div(
    [
        html.Div(
            [   
                html.Img(id='logo', className='logo'),
                html.H1(id='company-name', className='company-name')
            ],
            className="header"),
        html.Div(id="description"),
        html.Div([], id="graphs-content"),
        html.Div([], id="main-content"),
        html.Div([], id="forecast-content")
    ],
    className="content")

app.layout = html.Div(className='container', children=[item1, item2])

# callback for company info
@app.callback([
    Output("description", "children"),
    Output("logo", "src"),
    Output("company-name", "children"),
    Output("stock-price-button", "n_clicks"),
    Output("indicators-button", "n_clicks"),
    Output("forecast-button", "n_clicks")
], [Input("submit-button", "n_clicks")], [State("stock-code", "value")])

def update_data(n, val):  # input parameter(s)
    if n == None:
        return None, None, None, None, None, None
        # raise PreventUpdate
    else:
        if val == None:
            raise PreventUpdate
        else:
            ticker = yf.Ticker(val)
            inf = ticker.info
            df = pd.DataFrame().from_dict(inf, orient="index").T
            df[['logo_url', 'shortName', 'longBusinessSummary']]
            return df['longBusinessSummary'].values[0], df['logo_url'].values[0], df['shortName'].values[0], None, None, None

# callback for stocks graphs
@app.callback([
    Output("graphs-content", "children"),
], [
    Input("stock-price-button", "n_clicks"),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
], [State("stock-code", "value")])

def stock_price(n, start_date, end_date, val):
    if n == None:
        return [""]
        #raise PreventUpdate
    if val == None:
        raise PreventUpdate
    else:
        if start_date != None:
            df = yf.download(val, str(start_date), str(end_date))
        else:
            df = yf.download(val)

    df.reset_index(inplace=True)
    fig = px.line(df, x="Date", y=["Close", "Open"], title="Closing and Openning Price vs Date")
    return [dcc.Graph(figure=fig)]


# callback for indicators
@app.callback([Output("main-content", "children")], [
    Input("indicators-button", "n_clicks"),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
], [State("stock-code", "value")])

def indicators(n, start_date, end_date, val):
    if n == None:
        return [""]

    if val == None:
        return [""]

    if start_date == None:
        df_more = yf.download(val)

    else:
        df_more = yf.download(val, str(start_date), str(end_date))

    df_more.reset_index(inplace=True)
    fig = get_more(df_more)
    return [dcc.Graph(figure=fig)]

def get_more(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df, x="Date", y="EWA_20", title="Exponential Moving Average vs Date")
    fig.update_traces(mode='lines+markers')
    return fig    

if __name__ == '__main__':
    app.run_server(debug=True)
