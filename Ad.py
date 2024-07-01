import dash
from dash import dcc, html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd

app = dash.Dash(__name__)

# Sample data for users and tables
users_data = pd.DataFrame({'user_id': [1, 2, 3], 'user_name': ['Alice', 'Bob', 'Charlie']})
tables_data = ['Table1', 'Table2', 'Table3']

# DataFrame to hold permissions
permissions_df = pd.DataFrame(columns=['user', 'tables'])

app.layout = html.Div([
    html.H1('User Authorization Management'),
    dcc.Dropdown(id='user-dropdown', multi=False, placeholder='Select User'),
    dcc.Dropdown(id='table-dropdown', multi=True, placeholder='Select Tables'),
    html.Button('Add Permission', id='add-permission-btn', n_clicks=0),
    html.Button('Revoke Selected', id='revoke-selected-btn', n_clicks=0),
    dash_table.DataTable(id='permissions-table', columns=[
        {'name': 'User', 'id': 'user', 'editable': False},
        {'name': 'Tables', 'id': 'tables', 'editable': False},
        {'name': 'Revoke', 'id': 'revoke', 'type': 'boolean'}
    ], row_selectable='multi', selected_rows=[]),
    dcc.ConfirmDialog(id='confirm-dialog')
])

if __name__ == '__main__':
    app.run_server(debug=True)
