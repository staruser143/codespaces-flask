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
