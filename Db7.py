import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd
from sqlalchemy import create_engine, inspect

# Define connection details separately for Amazon Redshift
db_config = {
    'dialect': 'redshift+redshift_connector',
    'username': 'your_username',
    'password': 'your_password',
    'host': 'your_redshift_cluster_endpoint',
    'port': '5439',  # Default Redshift port
    'database': 'your_database_name'
}

# Construct the DATABASE_URI based on the db_config
DATABASE_URI = (
    f"{db_config['dialect']}://{db_config['username']}:{db_config['password']}"
    f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Fetch the list of schemas
def get_schema_list():
    query = "SELECT schema_name FROM information_schema.schemata"
    with engine.connect() as conn:
        schemas = pd.read_sql(query, conn)
    return schemas['schema_name'].tolist()

# Fetch the list of tables for a given schema
def get_table_list(schema_name):
    query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}'"
    with engine.connect() as conn:
        tables = pd.read_sql(query, conn)
    return tables['table_name'].tolist()

# Fetch table structure
def get_table_structure(schema_name, table_name):
    query = f"""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = '{schema_name}' AND table_name = '{table_name}'
    """
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

# Fetch table contents
def get_table_contents(schema_name, table_name):
    query = f"""
    SELECT *
    FROM {schema_name}.{table_name}
    LIMIT 100
    """
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Database Table Viewer"),
    dcc.Dropdown(
        id='schema-dropdown',
        options=[{'label': schema, 'value': schema} for schema in get_schema_list()],
        placeholder="Select a schema"
    ),
    dcc.Dropdown(
        id='table-dropdown',
        placeholder="Select a table"
    ),
    html.H2("Table Structure"),
    dash_table.DataTable(
        id='table-structure',
        columns=[
            {"name": "Column Name", "id": "column_name"},
            {"name": "Data Type", "id": "data_type"}
        ],
        data=[]
    ),
    html.H2("Table Contents"),
    dash_table.DataTable(
        id='table-contents',
        data=[],
        page_size=10,
    )
])

@app.callback(
    Output('table-dropdown', 'options'),
    [Input('schema-dropdown', 'value')]
)
def update_table_dropdown(selected_schema):
    if selected_schema:
        tables = get_table_list(selected_schema)
        return [{'label': table, 'value': table} for table in tables]
    return []

@app.callback(
    Output('table-structure', 'data'),
    [Input('table-dropdown', 'value')],
    [State('schema-dropdown', 'value')]
)
def update_table_structure(selected_table, selected_schema):
    if selected_schema and selected_table:
        df = get_table_structure(selected_schema, selected_table)
        return df.to_dict('records')
    return []

@app.callback(
    Output('table-contents', 'columns'),
    Output('table-contents', 'data'),
    [Input('table-dropdown', 'value')],
    [State('schema-dropdown', 'value')]
)
def update_table_contents(selected_table, selected_schema):
    if selected_schema and selected_table:
        df = get_table_contents(selected_schema, selected_table)
        columns = [{"name": i, "id": i} for i in df.columns]
        data = df.to_dict('records')
        return columns, data
    return [], []

if __name__ == '__main__':
    app.run_server(debug=True)
