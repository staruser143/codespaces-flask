import dash
from dash import dcc, html
import dash_table
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('User Authorization Management'),
    dcc.Dropdown(id='user-dropdown', multi=False, placeholder='Select User'),
    dcc.Dropdown(id='table-dropdown', multi=True, placeholder='Select Tables'),
    html.Button('Add Permission', id='add-permission-btn', n_clicks=0),
    html.Button('Revoke Permission', id='revoke-permission-btn', n_clicks=0),
    dash_table.DataTable(id='permissions-table', columns=[
        {'name': 'User', 'id': 'user'},
        {'name': 'Tables', 'id': 'tables'}
    ]),
    dcc.ConfirmDialog(id='confirm-dialog')
])

if __name__ == '__main__':
    app.run_server(debug=True)
