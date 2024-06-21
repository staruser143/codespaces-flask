import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
from sqlalchemy import create_engine, inspect

# Database connection
DATABASE_URI = 'postgresql+psycopg2://user:password@host:port/dbname'
engine = create_engine(DATABASE_URI)

# Fetch the list of tables
def get_table_list():
    inspector = inspect(engine)
    return inspector.get_table_names()

# Fetch table structure
def get_table_structure(table_name):
    query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'"
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Database Table Viewer"),
    dcc.Dropdown(
        id='table-dropdown',
        options=[{'label': table, 'value': table} for table in get_table_list()],
        placeholder="Select a table"
    ),
    dash_table.DataTable(
        id='table-structure',
        columns=[
            {"name": "Column Name", "id": "column_name"},
            {"name": "Data Type", "id": "data_type"}
        ],
        data=[]
    )
])

@app.callback(
    Output('table-structure', 'data'),
    [Input('table-dropdown', 'value')]
)
def update_table_structure(selected_table):
    if selected_table:
        df = get_table_structure(selected_table)
        return df.to_dict('records')
    return []

if __name__ == '__main__':
    app.run_server(debug=True)
