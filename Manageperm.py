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

    permissions_df = pd.DataFrame(permissions_data)
    displayed_confirm = False

    if triggered_id == 'user-dropdown':
        pass  # User selection changed, no action needed yet

    elif triggered_id == 'add-permission-btn' and selected_user and selected_tables:
        for table in selected_tables:
            if not ((permissions_df['user'] == selected_user) & (permissions_df['tables'] == table)).any():
                permissions_df = permissions_df.append({'user': selected_user, 'tables': table}, ignore_index=True)
        selected_tables = []

    elif triggered_id == 'revoke-selected-btn' and selected_rows:
        displayed_confirm = True

    elif triggered_id == 'confirm-dialog' and confirm_clicks > 0:
        if selected_rows:
            indices_to_drop = [permissions_df.index[i] for i in selected_rows]
            permissions_df = permissions_df.drop(indices_to_drop).reset_index(drop=True)

    # Update table options
    if selected_user:
        user_tables = permissions_df[permissions_df['user'] == selected_user]['tables'].tolist()
        available_tables = [table for table in tables_data if table not in user_tables]
    else:
        available_tables = tables_data

    table_options = [{'label': table, 'value': table} for table in available_tables]

    # Filter permissions data for the selected user
    if selected_user:
        filtered_df = permissions_df[permissions_df['user'] == selected_user]
    else:
        filtered_df = permissions_df

    # Add checkboxes to 'revoke' column
    filtered_df['revoke'] = '[ ]'

    return filtered_df.to_dict('records'), permissions_df.to_dict('records'), table_options, displayed_confirm
