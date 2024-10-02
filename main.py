import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
# Add an import for pandas_datareader and datetime
import pandas_datareader.data as web
from datetime import datetime
import yfinance as yf
import pandas as pd

app = dash.Dash()


nsdq=pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
options= []

for tic in nsdq.index:
    mydict={}
    mydict['label']=nsdq.loc[tic]['Name'] + ' '+ tic
    mydict['value']=tic
    options.append(mydict)

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([html.H3('Choose a stock symbol:', style={'paddingRight': '30px'}),
        dcc.Dropdown(
            id='my_ticker_symbol',
            options=options,
            value=['TSLA'],
            multi=True,
              )
              ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width' : '30%'}),
            html.Div([html.H3('Select a start and end date:'),
                      dcc.DatePickerRange(id='my_date_picker',
                                          min_date_allowed=datetime(2015, 1, 1),
                                          max_date_allowed=datetime.today(),
                                          start_date=datetime(2022, 1, 1),
                                          end_date=datetime.today()

        )
    ], style={'display':'inline-block'}),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':24, 'marginLeft':'30px'}
        ),
    ], style={'display':'inline-block'}),
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ]
        }
    )
])

@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'),
     State('my_date_picker', 'start_date'),
     State('my_date_picker', 'end_date')
     ])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    # Use datareader and datetime to define a DataFrame
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    # Change the output data

    traces = []
    for tic in stock_ticker:
        df = yf.download(tic, start=start, end=end)
        traces.append({'x':df.index, 'y':df['Close'], 'name': tic})


    fig = {
        'data': traces,
        'layout': {'title': stock_ticker}
    }
    return fig


if __name__ == '__main__':
    app.run_server()
