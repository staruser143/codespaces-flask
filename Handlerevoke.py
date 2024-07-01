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
