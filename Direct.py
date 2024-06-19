import json

def dash_filter_to_sql_direct(filters):
    """
    Convert Dash DataTable filter criteria to an SQL WHERE condition using direct mapping.
    """
    conditions = []
    
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
        elif operator == 'contains':
            condition = f"{col_id} LIKE '%{value}%'"
        elif operator == 'datestartswith':
            condition = f"{col_id} LIKE '{value}%'"
        else:
            raise ValueError(f"Unknown operator: {operator}")
        
        conditions.append(condition)
    
    where_clause = " AND ".join(conditions)
    return where_clause

filters = [
    {"column_id": "name", "operator": "contains", "value": "John"},
    {"column_id": "age", "operator": "gt", "value": "30"}
]
