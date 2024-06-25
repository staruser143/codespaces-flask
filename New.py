import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Custom Filtering UI"),
    
    html.Div(id='criteria-container', children=[]),
    
    html.Button('Add Criterion', id='add-criterion', n_clicks=0),
    html.Button('Add Compound Condition', id='add-compound', n_clicks=0),
    
    html.Br(),
    html.Br(),
    
    html.Button('Submit', id='submit', n_clicks=0),
    html.Div(id='output')
])

def create_criterion(idx):
    return html.Div([
        dcc.Dropdown(
            id={'type': 'field-dropdown', 'index': idx},
            options=[
                {'label': 'Field 1', 'value': 'field1'},
                {'label': 'Field 2', 'value': 'field2'},
                # Add more fields as needed
            ],
            placeholder="Select Field"
        ),
        dcc.Dropdown(
            id={'type': 'operator-dropdown', 'index': idx},
            options=[
                {'label': '=', 'value': '='},
                {'label': '!=', 'value': '!='},
                {'label': '>', 'value': '>'},
                {'label': '<', 'value': '<'},
                # Add more operators as needed
            ],
            placeholder="Select Operator"
        ),
        dcc.Input(
            id={'type': 'value-input', 'index': idx},
            placeholder="Enter value",
            type='text'
        ),
        html.Br()
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'})

def create_compound_condition(idx):
    return html.Div([
        dcc.Dropdown(
            id={'type': 'compound-dropdown', 'index': idx},
            options=[
                {'label': 'AND', 'value': 'AND'},
                {'label': 'OR', 'value': 'OR'}
            ],
            placeholder="Select Condition"
        ),
        html.Br()
    ], style={'margin-bottom': '10px'})

@app.callback(
    Output('criteria-container', 'children'),
    Input('add-criterion', 'n_clicks'),
    Input('add-compound', 'n_clicks'),
    State('criteria-container', 'children')
)
def update_criteria(n_clicks_criterion, n_clicks_compound, children):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'add-criterion':
        children.append(create_criterion(len(children)))
    elif button_id == 'add-compound':
        children.append(create_compound_condition(len(children)))
    
    return children

@app.callback(
    Output('output', 'children'),
    Input('submit', 'n_clicks'),
    State('criteria-container', 'children')
)
def process_criteria(n_clicks, children):
    if n_clicks == 0:
        raise dash.exceptions.PreventUpdate
    
    conditions = []
    compound_operators = []
    
    for child in children:
        props_id = child['props'].get('id', {})
        if isinstance(props_id, dict) and 'type' in props_id:
            if 'field-dropdown' in props_id['type']:
                field = child['props']['children'][0]['props'].get('value')
                operator = child['props']['children'][1]['props'].get('value')
                value = child['props']['children'][2]['props'].get('value')
                if field and operator and value:
                    conditions.append(f"{field} {operator} '{value}'")
            elif 'compound-dropdown' in props_id['type']:
                condition = child['props']['children'][0]['props'].get('value')
                if condition:
                    compound_operators.append(condition)
    
    where_clause = ""
    if conditions:
        where_clause = conditions[0]
        for i in range(1, len(conditions)):
            if i-1 < len(compound_operators):
                where_clause += f" {compound_operators[i-1]} {conditions[i]}"
    
    return html.Div([
        html.H4("Constructed WHERE Clause:"),
        html.Pre(where_clause)
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
