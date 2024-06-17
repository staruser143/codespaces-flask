import dash
from dash import Dash, dcc, html, dash_table,  Input, Output, callback
import pandas as pd
from sqlalchemy import create_engine
import re
from dbutils import build_query, getPaginatedData


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
        page_size=3,
        page_action='custom',
        filter_action='custom'  # Enable filtering
    ),
])

@callback(
    Output('datatable-paging', 'data'),
    [Input('datatable-paging', "page_current"),
     Input('datatable-paging', "page_size"),    
     Input('datatable-paging', 'sort_by'),
     Input('datatable-paging', "filter_query")])  
def update_table(page_current, page_size, sort_by,filter_query):
    print(f"page_current: {page_current}")
    print(f"page_size: {page_size}")
    print(f"sort_by: {sort_by}")
    print(f"filter_query: {filter_query}")
    print(f"filter_query type: {type(filter_query)}")

    query=build_query(filter_query,sort_by, page_current, page_size)
    print(f"query: {query}")
    df = getPaginatedData(query)
    return df.to_dict("records")

@app.callback(
    dash.dependencies.Output('datatable-paging', 'page_count'),
    [dash.dependencies.Input('datatable-paging', "page_size")])
def update_page_count(page_size):
    count = pd.read_sql_query('SELECT COUNT(*) FROM my_table', con=engine).values[0][0]
    return int(count / page_size) + (count % page_size > 0)

def parse_filter_query(filter_query):
    # Define a translation dictionary
    translate_dict = {
        ' eq ': ' = ',
        ' contains ': ' LIKE ',
        ' lt ': ' < ',
        ' le ': ' <= ',
        ' gt ': ' > ',
        ' ge ': ' >= ',
    }

    # Translate the filter query
    for dash_op, sql_op in translate_dict.items():
        filter_query = filter_query.replace(dash_op, sql_op)

    # Handle the 'LIKE' operator (add '%' around the value)
    filter_query = re.sub(r'LIKE\s\'(.+?)\'', lambda m: f"LIKE '%{m.group(1)}%'", filter_query)

    return filter_query

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8051)