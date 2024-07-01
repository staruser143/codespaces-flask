import dash
from dash import dcc, html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd

app = dash.Dash(__name__)

# Sample data for users and tables
users_data = pd.DataFrame({'user_id': [1, 2, 3], 'user_name': ['Alice', 'Bob', 'Charlie']})
tables_data = ['Table1', 'Table2', 'Table3']

app.layout = html.Div([
    html.H1('User Authorization Management'),
    dcc.Dropdown(id='user-dropdown', multi=False, placeholder='Select User'),
    dcc.Dropdown(id='table-dropdown', multi=True, placeholder='Select Tables'),
    html.Button('Add Permission', id='add-permission-btn', n_clicks=0),
    html.Button('Revoke Selected', id='revoke-selected-btn', n_clicks=0),
    dash_table.DataTable(id='permissions-table', columns=[
        {'name': 'User', 'id': 'user', 'editable': False},
        {'name': 'Tables', 'id': 'tables', 'editable': False},
        {'name': 'Revoke', 'id': 'revoke', 'presentation': 'markdown'}
    ], row_selectable='multi', selected_rows=[]),
    dcc.ConfirmDialog(id='confirm-dialog'),
    dcc.Store(id='permissions-data', data=[])  # Hidden storage for permissions data
])

@app.callback(
    Output('user-dropdown', 'options'),
    Input('user-dropdown', 'id')
)
def update_user_dropdown(_):
    user_options = [{'label': row['user_name'], 'value': row['user_id']} for _, row in users_data.iterrows()]
    return user_options

@app.callback(
    Output('table-dropdown', 'options'),
    Input('user-dropdown', 'value'),
    State('permissions-data', 'data')
)
def update_table_dropdown(selected_user, permissions_data):
    if selected_user is None:
        return [{'label': table, 'value': table} for table in tables_data]

    permissions_df = pd.DataFrame(permissions_data)
    user_tables = permissions_df[permissions_df['user'] == selected_user]['tables'].tolist()
    available_tables = [table for table in tables_data if table not in user_tables]

    return [{'label': table, 'value': table} for table in available_tables]

@app.callback(
    Output('permissions-table', 'data'),
    Input('user-dropdown', 'value'),
    State('permissions-data', 'data')
)
def update_permissions_table(selected_user, permissions_data):
    permissions_df = pd.DataFrame(permissions_data)
    if selected_user:
        filtered_df = permissions_df[permissions_df['user'] == selected_user]
    else:
        filtered_df = permissions_df

    # Add checkboxes to 'revoke' column
    filtered_df['revoke'] = filtered_df.apply(lambda row: '[ ]', axis=1)
    return filtered_df.to_dict('records')

@app.callback(
    Output('permissions-table', 'data'),
    Output('permissions-data', 'data'),
    Output('table-dropdown', 'options'),
    Input('add-permission-btn', 'n_clicks'),
    State('user-dropdown', 'value'),
    State('table-dropdown', 'value'),
    State('permissions-data', 'data')
)
def add_permissions(add_clicks, selected_user, selected_tables, permissions_data):
    if not selected_user or not selected_tables:
        return permissions_data, permissions_data, [{'label': table, 'value': table} for table in tables_data]

    permissions_df = pd.DataFrame(permissions_data)
    if add_clicks > 0:
        for table in selected_tables:
            if not ((permissions_df['user'] == selected_user) & (permissions_df['tables'] == table)).any():
                permissions_df = permissions_df.append({'user': selected_user, 'tables': table}, ignore_index=True)

    user_tables = permissions_df[permissions_df['user'] == selected_user]['tables'].tolist()
    available_tables = [table for table in tables_data if table not in user_tables]
    table_options = [{'label': table, 'value': table} for table in available_tables]

    return permissions_df.to_dict('records'), permissions_df.to_dict('records'), table_options

@app.callback(
    Output('confirm-dialog', 'displayed'),
    Input('revoke-selected-btn', 'n_clicks'),
    State('permissions-table', 'selected_rows')
)
def display_confirm(n_clicks, selected_rows):
    if n_clicks > 0 and selected_rows:
        return True
    return False

@app.callback(
    Output('permissions-table', 'data'),
    Output('permissions-data', 'data'),
    Output('table-dropdown', 'options'),
    Input('confirm-dialog', 'submit_n_clicks'),
    State('permissions-table', 'data'),
    State('permissions-table', 'selected_rows'),
    State('user-dropdown', 'value'),
    State('permissions-data', 'data')
)
def revoke_permissions(confirm_clicks, current_data, selected_rows, selected_user, permissions_data):
    if confirm_clicks > 0 and selected_rows:
        permissions_df = pd.DataFrame(permissions_data)
        indices_to_drop = [current_data[i]['index'] for i in selected_rows]
        permissions_df = permissions_df.drop(indices_to_drop).reset_index(drop=True)

    if selected_user is not None:
        user_tables = permissions_df[permissions_df['user'] == selected_user]['tables'].tolist()
        available_tables = [table for table in tables_data if table not in user_tables]
    else:
        available_tables = tables_data

    table_options = [{'label': table, 'value': table} for table in available_tables]

    return permissions_df.to_dict('records'), permissions_df.to_dict('records'), table_options

if __name__ == '__main__':
    app.run_server(debug=True)
