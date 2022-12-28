import dash
from dash import dcc
from dash import html
from datetime import datetime as dt

app = dash.Dash(__name__, external_stylesheets=['assets\styles.css'])
server = app.server

item1 = html.Div(
    [
        html.P("Welcome to the Stock Dash App!", className="start"),

        html.Div([
            # stock code input
            dcc.Input(id='stock-code', type='text', placeholder='Enter stock code'),
            html.Button('Submit', id='submit-button')
        ], className='stock-input'),
        
        html.Div([
            # Date range picker input
            dcc.DatePickerRange(
                id='date-range', start_date=dt(2020, 1, 1), end_date=dt.now())
        ]),
        html.Div([
            # Stock price button
            html.Button('Get stock price', id='stock-price-button'),

            # Indicators button
            html.Button('Get indicators', id='indicators-button'),

            # Number of days of forecast input
            dcc.Input(id='forecast-days', type='number', placeholder='Enter number of days'),

            # Forecast button
            html.Button('Get forecast', id='forecast-button')
        ])
    ],
    className="nav")

item2 = html.Div(
    [
        html.Div(
            [  # Logo
                html.Img(src='/path/to/logo.png',
                         alt='logo', className='logo'),
                # Company Name
                html.H1('Company Name', className='company-name')
            ],
            className="header"),
        html.Div(  # Description
            id="description", className="decription_ticker"),
        html.Div([
            # Stock price plot

        ], id="graphs-content"),
        html.Div([
            # Indicator plot

        ], id="main-content"),
        html.Div([
            # Forecast plot

        ], id="forecast-content")
    ],
    className="content")

app.layout = html.Div(className='container', children=[item1, item2])


if __name__ == '__main__':
    app.run_server(debug=True)
