
import dash
from dash import Dash, dcc, html,dash_table
#import dash_table
import pandas as pd
from sqlalchemy import create_engine

# Create a connection to your database
engine = create_engine('sqlite:///my_database.db')

app = Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-paging',
        columns=[
            {"name": i, "id": i} for i in pd.read_sql_query('SELECT * FROM my_table LIMIT 1', con=engine).columns
        ],
        page_current=0,
        page_size=10,
        page_action='custom'
    ),
])

@app.callback(
    dash.dependencies.Output('datatable-paging', 'data'),
    [dash.dependencies.Input('datatable-paging', "page_current"),
     dash.dependencies.Input('datatable-paging', "page_size")])
def update_table(page_current, page_size):
    df = pd.read_sql_query('SELECT * FROM my_table LIMIT {} OFFSET {}'.format(page_size, page_current * page_size), con=engine)
    return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8051)
# Create a connection to your database
engine = create_engine('sqlite:///my_database.db')

app = Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-paging',
        columns=[
            {"name": i, "id": i} for i in pd.read_sql_query('SELECT * FROM my_table ', con=engine).columns
        ],
        page_current=0,
        page_size=10,
        page_action='custom'
    ),
])

@app.callback(
    dash.dependencies.Output('datatable-paging', 'data'),
    [dash.dependencies.Input('datatable-paging', "page_current"),
     dash.dependencies.Input('datatable-paging', "page_size")])
def update_table(page_current, page_size):
    df = pd.read_sql_query('SELECT * FROM my_table LIMIT {} OFFSET {}'.format(page_size, page_current * page_size), con=engine)
    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8051)