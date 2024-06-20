import dash
from dash import dcc, html, Input, Output, State
import dash_ag_grid as dag
import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div([
    dag.AgGrid(
        id='data-grid',
        columnDefs=[
            {'headerName': 'ID', 'field': 'id'},
            {'headerName': 'Name', 'field': 'name'},
            # Add more columns as needed
        ],
        pagination=True,
        paginationPageSize=10,  # Number of rows per page
        rowModelType='pagination',  # Use pagination model
    )
])

@app.callback(
    Output('data-grid', 'rowData'),
    Input('data-grid', 'paginationChanged'),
    State('data-grid', 'paginationPageSize'),
)
def update_table(pagination, page_size):
    if not pagination:
        return []

    current_page = pagination['currentPage']
    start_row = current_page * page_size

    session = Session()

    # Fetch the required data from the database
    query = session.execute(f"""
        SELECT * FROM your_table
        ORDER BY id
        LIMIT {page_size} OFFSET {start_row}
    """)
    data = query.fetchall()

    # Convert data to list of dicts
    row_data = [dict(row) for row in data]
    
    session.close()
    return row_data

if __name__ == '__main__':
    app.run_server(debug=True)
  
