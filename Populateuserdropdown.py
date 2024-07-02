@app.callback(
    Output('user-dropdown', 'options'),
    Input('user-dropdown', 'id')
)
def update_user_dropdown(_):
    user_options = [{'label': row['user_name'], 'value': row['user_id']} for _, row in users_data.iterrows()]
    return user_options
