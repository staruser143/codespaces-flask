from dash import Dash, dash_table, html, Input, Output
import pandas as pd
import sqlite3
import json

# Sample data for demonstration
data = pd.DataFrame({
    'name': ['John Doe', 'Jane Smith', 'Alice Johnson', 'Bob Lee'],
    'age': [28, 34, 45, 23]
})

# Write sample data to SQLite database
conn = sqlite3.connect(':memory:')
data.to_sql('people', conn, index=False, if_exists='replace')

app = Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in data.columns],
        filter_action='custom',
        filter_query=''
    ),
    html.Div(id='output')
])

@app.callback(
    Output('table', 'data'),
    Input('table', 'filter_query')
)
def update_table(filter_query):
    if not filter_query:
        query = "SELECT * FROM people"
    else:
        where_clause = dash_filter_to_sql(filter_query)
        query = f"SELECT * FROM people WHERE {where_clause}"
    
    df = pd.read_sql(query, conn)
    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
