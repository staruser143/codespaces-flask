import json

def dash_filter_to_sql(filter_query):
    """
    Convert Dash DataTable filter criteria to an SQL WHERE condition.

    :param filter_query: String containing filter criteria from Dash DataTable
    :return: String representing the SQL WHERE condition
    """
    if not filter_query:
        return "1 = 1"  # No filters applied
    
    conditions = []
    filters = json.loads(filter_query)
    
    for filter in filters:
        col_id = filter['column_id']
        operator = filter['operator']
        value = filter['value']
        
        if operator == 'eq':
            condition = f"{col_id} = '{value}'"
        elif operator == 'ne':
            condition = f"{col_id} != '{value}'"
        elif operator == 'lt':
            condition = f"{col_id} < '{value}'"
        elif operator == 'le':
            condition = f"{col_id} <= '{value}'"
        elif operator == 'gt':
            condition = f"{col_id} > '{value}'"
        elif operator == 'ge':
            condition = f"{col_id} >= '{value}'"
        elif operator == 'contains' or operator == 'scontains':
            condition = f"{col_id} LIKE '%{value}%'"
        elif operator == 'datestartswith' or operator == 'sdatestartswith':
            condition = f"{col_id} LIKE '{value}%'"
        else:
            raise ValueError(f"Unknown operator: {operator}")
        
        conditions.append(condition)
    
    # Join all conditions with AND to form the WHERE clause
    where_clause = " AND ".join(conditions)
    return where_clause

# Example usage
filters = [
    {"column_id": "name", "operator": "scontains", "value": "John"},
    {"column_id": "age", "operator": "gt", "value": "30"}
]

sql_where_condition = dash_filter_to_sql(json.dumps(filters))
print(sql_where_condition)  # Output: "name LIKE '%John%' AND age > '30'"
