import dash
from dash import dcc, html
import dash_table
from dash.dependencies import Input, Output, State
import sqlite3
import pandas as pd

app = dash.Dash(__name__)

# Initialize database connection
def init_db():
    conn = sqlite3.connect('permissions.db')
    return conn

# Fetch users from the database
def fetch_users():
    conn = init_db()
    users_data = pd.read_sql_query("SELECT * FROM USER", conn)
    conn.close()
    return users_data

# Fetch tables from the database
def fetch_tables():
    conn = init_db()
    tables_data = pd.read_sql_query("SELECT * FROM TABLES", conn)
    conn.close()
    return tables_data

# Fetch permissions from the database for a given user
def fetch_permissions(user_id):
    conn = init_db()
    permissions_data = pd.read_sql_query(f"SELECT t.table_name AS tables FROM USER_TABLE ut JOIN TABLES t ON ut.table_id = t.table_id WHERE ut.user_id = {user_id}", conn)
    conn.close()
    return permissions_data

# Insert new permissions into the database
def insert_permissions(user_id, table_ids):
    conn = init_db()
    c = conn.cursor()
    for table_id in table_ids:
        c.execute("INSERT INTO USER_TABLE (user_id, table_id) VALUES (?, ?)", (user_id, table_id))
    conn.commit()
    conn.close()

# Delete permissions from the database
def delete_permissions(user_id, table_ids):
    conn = init_db()
    c = conn.cursor()
    for table_id in table_ids:
        c.execute("DELETE FROM USER_TABLE WHERE user_id = ? AND table_id = ?", (user_id, table_id))
    conn.commit()
    conn.close()

# App layout
app.layout = html.Div([
    html.H1('User Authorization Management'),
    dcc.Dropdown(id='user-dropdown', multi=False, placeholder='Select User'),
    dcc.Dropdown(id='table-dropdown', multi=True, placeholder='Select Tables'),
    html.Button('Add Permission', id='add-permission-btn', n_clicks=0),
    html.Button('Revoke Selected', id='revoke-selected-btn', n_clicks=0),
    dash_table.DataTable(id='permissions-table', columns=[
        {'name': 'Tables', 'id': 'tables', 'editable': False}
    ], row_selectable='multi', selected_rows=[]),
    dcc.ConfirmDialog(
        id='confirm-dialog',
        message='Are you sure you want to revoke the selected permissions?'
    ),
    dcc.Store(id='permissions-data', data=[]),  # Hidden storage for permissions data
    dcc.Store(id='user-data', data=[])  # Hidden storage to trigger user dropdown update
])

# Update user dropdown options
@app.callback(
    Output('user-dropdown', 'options'),
    Input('user-data', 'data')
)
def update_user_dropdown(_):
    users_data = fetch_users()
    user_options = [{'label': row['user_name'], 'value': row['user_id']} for _, row in users_data.iterrows()]
    return user_options

# Load user data to trigger the update of user dropdown options
@app.callback(
    Output('user-data', 'data'),
    Input('user-dropdown', 'id')
)
def load_user_data(_):
    return fetch_users().to_dict('records')

# Manage permissions
@app.callback(
    Output('permissions-table', 'data'),
    Output('permissions-data', 'data'),
    Output('table-dropdown', 'options'),
    Output('confirm-dialog', 'displayed'),
    Input('user-dropdown', 'value'),
    Input('add-permission-btn', 'n_clicks'),
    Input('revoke-selected-btn', 'n_clicks'),
    Input('confirm-dialog', 'submit_n_clicks'),
    State('table-dropdown', 'value'),
    State('permissions-data', 'data'),
    State('permissions-table', 'selected_rows'),
    prevent_initial_call=True
)
def manage_permissions(selected_user, add_clicks, revoke_clicks, confirm_clicks, selected_tables, permissions_data, selected_rows):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Initialize permissions_df with the correct columns if it's empty
    if not permissions_data:
        permissions_df = pd.DataFrame(columns=['user', 'tables'])
    else:
        permissions_df = pd.DataFrame(permissions_data)

    displayed_confirm = False

    if triggered_id == 'user-dropdown':
        # Update table options based on selected user
        if selected_user:
            user_permissions = fetch_permissions(selected_user)
            user_tables = user_permissions['tables'].tolist()
            available_tables = fetch_tables()
            available_tables = available_tables[~available_tables['table_name'].isin(user_tables)]
            table_options = [{'label': row['table_name'], 'value': row['table_id']} for _, row in available_tables.iterrows()]
        else:
            available_tables = fetch_tables()
            table_options = [{'label': row['table_name'], 'value': row['table_id']} for _, row in available_tables.iterrows()]
        
        return user_permissions.to_dict('records'), user_permissions.to_dict('records'), table_options, displayed_confirm

    elif triggered_id == 'add-permission-btn' and selected_user and selected_tables:
        insert_permissions(selected_user, selected_tables)
        permissions_data = fetch_permissions(selected_user).to_dict('records')

    elif triggered_id == 'revoke-selected-btn' and selected_rows:
        displayed_confirm = True
        return dash.no_update, dash.no_update, dash.no_update, displayed_confirm

    elif triggered_id == 'confirm-dialog' and confirm_clicks > 0:
        if selected_rows:
            user_permissions = fetch_permissions(selected_user)
            tables_to_revoke = user_permissions.iloc[selected_rows]['tables'].tolist()
            table_ids_to_revoke = [row['table_id'] for _, row in fetch_tables().iterrows() if row['table_name'] in tables_to_revoke]
            delete_permissions(selected_user, table_ids_to_revoke)
            permissions_data = fetch_permissions(selected_user).to_dict('records')

    # Update table options after add or revoke actions
    if selected_user:
        user_permissions = fetch_permissions(selected_user)
        user_tables = user_permissions['tables'].tolist()
        available_tables = fetch_tables()
        available_tables = available_tables[~available_tables['table_name'].isin(user_tables)]
        table_options = [{'label': row['table_name'], 'value': row['table_id']} for _, row in available_tables.iterrows()]
    else:
        available_tables = fetch_tables()
        table_options = [{'label': row['table_name'], 'value': row['table_id']} for _, row in available_tables.iterrows()]

    return user_permissions.to_dict('records'), user_permissions.to_dict('records'), table_options, displayed_confirm

if __name__ == '__main__':
    app.run_server(debug=True)
