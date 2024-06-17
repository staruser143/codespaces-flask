import dash
from dash import dcc, html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3
import re

# Sample data and SQLite setup
def create_sample_db():
    conn = sqlite3.connect('example.db')
    df = pd.DataFrame({
        "age": [25, 35, 45, 30, 22, 38, 40, 27, 36, 50],
        "country": ["USA", "Canada", "USA", "UK", "USA", "Canada", "UK", "USA", "UK", "Canada"]
    })
    df.to_sql('people', conn, if_exists='replace', index=False)
    return conn

conn = create_sample_db()

# Initialize Dash app
app = dash.Dash(__name__)

# Define columns
columns = [
    {"name": "Age", "id": "age"},
    {"name": "Country", "id": "country"}
]

# Layout with DataTable and output Div
app.layout = html.Div([
    dash_table.DataTable(
        id='datatable',
        columns=columns,
        filter_action='native',
        sort_action='native',
        page_action='native',
        page_current=0,
        page_size=5
    ),
    html.Div(id='query-output')  # To display SQL query for debugging
])

# Function to parse filter query
def parse_filter_query(filter_query):
    if not filter_query:
        return {"filters": [], "logic": "AND"}
    
    filter_query = filter_query.strip().lstrip('{').rstrip('}')
    conditions = re.split(r' (&| \|) ', filter_query)
    
    parsed_filters = []
    for condition in conditions:
        match = re.match(r'({[^}]+}) (==|!=|>|>=|<|<=|in|not in|contains|not contains) (.+)', condition)
        if match:
            column = match.group(1).strip('{}')
            operator = match.group(2)
            value = match.group(3).strip('"')
            parsed_filters.append({"column_id": column, "operator": operator, "value": value})
    
    logic = 'AND' if ' & ' in filter_query else 'OR'
    
    return {"filters": parsed_filters, "logic": logic}

# Function to convert parsed filters to SQL
def convert_dash_filter_to_sql(dash_filter, sort_by, table_name, page_current, page_size):
    operators_map = {
        "==": "=",
        "!=": "!=",
        ">": ">",
        ">=": ">=",
        "<": "<",
        "<=": "<=",
        "in": "IN",
        "not in": "NOT IN",
        "contains": "LIKE",
        "not contains": "NOT LIKE"
    }

    conditions = []
    for filter in dash_filter["filters"]:
        column = filter["column_id"]
        operator = operators_map[filter["operator"]]
        value = filter["value"]

        if operator in ["LIKE", "NOT LIKE"]:
            value = f"'%{value}%'"
        elif operator in ["IN", "NOT IN"]:
            value = f"({value})"
        else:
            value = f"'{value}'" if isinstance(value, str) else value

        condition = f"{column} {operator} {value}"
        conditions.append(condition)

    logic = dash_filter["logic"]
    where_clause = f" {logic} ".join(conditions) if conditions else "1=1"

    # Handle sorting
    sort_clause = ""
    if sort_by:
        sort_clauses = []
        for sort in sort_by:
            sort_clauses.append(f"{sort['column_id']} {'ASC' if sort['direction'] == 'asc' else 'DESC'}")
        sort_clause = " ORDER BY " + ", ".join(sort_clauses)

    offset = page_current * page_size
    limit_clause = f" LIMIT {page_size} OFFSET {offset}"

    sql_query = f"SELECT * FROM {table_name} WHERE {where_clause}{sort_clause}{limit_clause};"
    return sql_query

# Callback to fetch data from the database
@app.callback(
    [Output('datatable', 'data'),
     Output('query-output', 'children')],  # Also output the query for debugging
    [Input('datatable', 'filter_query'),
     Input('datatable', 'sort_by'),
     Input('datatable', 'page_current'),
     Input('datatable', 'page_size')]
)
def update_table_data(filter_query, sort_by, page_current, page_size):
    table_name = "people"
    parsed_filter = parse_filter_query(filter_query) if filter_query else {"filters": [], "logic": "AND"}
    sql_query = convert_dash_filter_to_sql(parsed_filter, sort_by, table_name, page_current, page_size)
    
    # Fetch data from the database
    conn = sqlite3.connect('example.db')
    df = pd.read_sql_query(sql_query, conn)
    
    return df.to_dict('records'), f"SQL Query: {sql_query}"

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
