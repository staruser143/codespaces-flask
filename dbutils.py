

def map_operator(dt_operator):
    operators={
        'eq':'=',
        'lt':'<',
        'le':'<=',
        'gt':'>',
        'ge':'>=',
        'ne':'<>',
        'contains':'LIKE',
        'startsWith':'LIKE',
        'endsWith':'LIKE'
    }
    return operators.get(dt_operator)

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

def getPaginatedData(query):
    # Create a connection to your database
    from sqlalchemy import create_engine
    import pandas as pd
    engine = create_engine('sqlite:///my_database.db')
    df = pd.read_sql_query(query, con=engine)
    return df

operators={
        'eq':'=',
        'lt':'<',
        'le':'<=',
        'gt':'>',
        'ge':'>=',
        'ne':'<>',
        'contains':'LIKE',
        'startsWith':'LIKE',
        'endsWith':'LIKE'
    }
def format_value(value,operator):
    try:
        float_value=float(value)
        is_numeric=True
    except ValueError:
        is_numeric=False

    if is_numeric:
        return float_value
    else:
        if operator=='contains':
            return f"'%{value}%'"
        elif operator=='startsWith':
            return f"'{value}%'"
        elif operator=='endsWith':
            return f"'%{value}'"
        else:
            return f"'{value}'"
   
    return sql_query
def generate_where_clauses(filter_query):
    where_clauses=[]
    print('START: generate_where_clauses')
    print(f'filter_query: { filter_query }')


    filtering_expressions = filter_query.split(' && ')
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        print(f'col_name: {col_name}')
        print(f'operator: {operator}')
        print(f'filter_value: {filter_value}')
        sql_operator=map_operator(operator)
        formatted_value=format_value(filter_value,operator)
        print(f'sql_operator: {sql_operator}')
        print(f'formatted_value: {formatted_value}')
        
        clause=f"{col_name} {sql_operator} {formatted_value}"
        print(f'clause: {clause}')
        where_clauses.append(clause)

    return ' AND '.join(where_clauses)

def build_query(filter_model,sort_model,current_row,page_size):
    base_query="SELECT * FROM my_table"
    where_clauses=[]
    order_by_clauses=[]
    print(f'build_query: filter_model:{filter_model} :: sort_model: {sort_model}')
    print(f'current_row: {current_row} , page_size: {page_size}')
    if filter_model:
       where_clauses= convert_dash_to_sql(filter_model)
    
    print(f'where_clauses:{where_clauses}')


    if where_clauses:
        base_query+=" WHERE " + " " + where_clauses

    if sort_model:
        for sort in sort_model:
            print(f'column_id: {sort["column_id"]}')
            print(f'direction: {sort["direction"]}')
            order_by_clauses.append(f"{sort['column_id']}  {sort['direction']}")
            print(f'order_by_clauses: {order_by_clauses}')
    if order_by_clauses:
        base_query+=" ORDER BY " + ", ".join(order_by_clauses)  
    
    print(f'base_query: {base_query}')

    # Add Pagination
    base_query+=f" LIMIT {page_size} OFFSET {current_row * page_size } "
    return base_query


import re

def convert_dash_to_sql(dash_query):
    # Map Dash operators to SQL operators
    operator_mapping = {
        ' eq ': ' = ',
        ' ne ': ' != ',
        ' lt ': ' < ',
        ' le ': ' <= ',
        ' gt ': ' > ',
        ' ge ': ' >= ',
        ' and ': ' AND ',
        ' or ': ' OR ',
        ' scontains ': ' LIKE ',
        ' slt ': ' < ',
        ' sle ': ' <= ',
        ' sgt ': ' > ',
        ' sge ': ' >= ',
        ' sne ': ' != ',
        ' seq ': ' = ',
    }

    # Replace the operators in the query
    for dash_operator, sql_operator in operator_mapping.items():
        dash_query = dash_query.replace(dash_operator, sql_operator)

    # Handle special cases for LIKE operator
    dash_query = re.sub(r"LIKE '(.+?)'", r"LIKE '%%\1%%'", dash_query)

    return dash_query
#dash_query = "{name eq 'John Doe' and age ge 21}"
dash_query="{name} scontains SF"
#dash_query="{age} ne 30"
print(convert_dash_to_sql(dash_query))
