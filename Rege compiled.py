import re
import json

# Precompile regex patterns
patterns = {
    'eq': re.compile(r'^({col_id}) = "(.+)"$'),
    'ne': re.compile(r'^({col_id}) != "(.+)"$'),
    'lt': re.compile(r'^({col_id}) < "(.+)"$'),
    'le': re.compile(r'^({col_id}) <= "(.+)"$'),
    'gt': re.compile(r'^({col_id}) > "(.+)"$'),
    'ge': re.compile(r'^({col_id}) >= "(.+)"$'),
    'contains': re.compile(r'^({col_id}) contains "(.+)"$'),
    'datestartswith': re.compile(r'^({col_id}) datestartswith "(.+)"$')
}

def dash_filter_to_sql(filter_query):
    """
    Convert Dash DataTable filter criteria to an SQL WHERE condition using regex parsing.

    :param filter_query: String containing filter criteria from Dash DataTable
    :return: String representing the SQL WHERE condition
    """
    if not filter_query:
        return "1 = 1"  # No filters applied
    
    conditions = []

    # Split filter query into individual filters
    filters = filter_query.split(' && ')
    
    for filter in filters:
        matched = False
        
        for operator, pattern in patterns.items():
            col_pattern = pattern.pattern.format(col_id=r'([a-zA-Z_][a-zA-Z0-9_]*)')
            match = re.match(col_pattern, filter)
            
            if match:
                col_id = match.group(1)
                value = match.group(2)
                
                # Adjust the operator and value as needed
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
                matched = True
                break
        
        if not matched:
            raise ValueError(f"Could not parse filter: {filter}")
    
    # Join all conditions with AND to form the WHERE clause
    where_clause = " AND ".join(conditions)
    return where_clause

# Example usage
filters = [
    {"column_id": "name", "operator": "contains", "value": "John"},
    {"column_id": "age", "operator": "gt", "value": "30"}
]

filter_query = 'name contains "John" && age > "30"'
sql_where_condition = dash_filter_to_sql(filter_query)
print(sql_where_condition)  # Output: "name LIKE '%John%' AND age > '30'"
