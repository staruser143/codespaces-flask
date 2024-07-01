# Assuming a DataFrame or similar structure to hold permissions
permissions_df = pd.DataFrame(columns=['user', 'tables'])

@app.callback(
    Output('permissions-table', 'data'),
    Input('add-permission-btn', 'n_clicks'),
    Input('revoke-permission-btn', 'n_clicks'),
    State('user-dropdown', 'value'),
    State('table-dropdown', 'value'),
    State('permissions-table', 'data')
)
def manage_permissions(add_clicks, revoke_clicks, selected_user, selected_tables, current_data):
    global permissions_df

    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if not selected_user or not selected_tables:
        return current_data

    if button_id == 'add-permission-btn':
        # Add permissions
        for table in selected_tables:
            permissions_df = permissions_df.append({'user': selected_user, 'tables': table}, ignore_index=True)

    elif button_id == 'revoke-permission-btn':
        # Revoke permissions
        permissions_df = permissions_df[~((permissions_df['user'] == selected_user) & (permissions_df['tables'].isin(selected_tables)))]

    # Convert DataFrame to a list of dictionaries for DataTable
    data = permissions_df.to_dict('records')
    return data

# Confirm dialog for revoking permissions
@app.callback(
    Output('confirm-dialog', 'displayed'),
    Input('revoke-permission-btn', 'n_clicks')
)
def display_confirm(n_clicks):
    if n_clicks > 0:
        return True
    return False

if __name__ == '__main__':
    app.run_server(debug=True)
