import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Custom Filtering UI"),
    
    html.Div(id='criteria-container', children=[]),
    
    html.Button('Add Criterion', id='add-criterion', n_clicks=0),
    html.Button('Add Compound Condition', id='add-compound', n_clicks=0),
    
    html.Br(),
    html.Br(),
    
    html.Button('Submit', id='submit', n_clicks=0),
    html.Div(id='output')
])

if __name__ == '__main__':
    app.run_server(debug=True)
