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
