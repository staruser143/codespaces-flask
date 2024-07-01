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

    return filtered_df.to_dict('records')
