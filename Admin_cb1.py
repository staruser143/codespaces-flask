import pandas as pd

def get_users():
    # Replace with actual DB call
    return pd.DataFrame({'user_id': [1, 2, 3], 'user_name': ['Alice', 'Bob', 'Charlie']})

def get_tables():
    # Replace with actual DB call
    return ['Table1', 'Table2', 'Table3']

@app.callback(
    Output('user-dropdown', 'options'),
    Output('table-dropdown', 'options'),
    Input('user-dropdown', 'id')
)
def update_dropdowns(_):
    users = get_users()
    tables = get_tables()
    user_options = [{'label': user_name, 'value': user_id} for user_id, user_name in zip(users['user_id'], users['user_name'])]
    table_options = [{'label': table, 'value': table} for table in tables]
    return user_options, table_options
