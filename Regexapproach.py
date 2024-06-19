import re

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

def dash_filter_to_sql_regex(filter_query):
    """
    Convert Dash DataTable filter criteria to an SQL WHERE condition using regex parsing.
    """
    if not filter_query:
        return "1 = 1"
    
    conditions = []
    filters = filter_query.split(' && ')
    
    for filter in filters:
        matched = False
        
        for operator, pattern in patterns.items():
            col_pattern = pattern.pattern.format(col_id=r'([a-zA-Z_][a-zA-Z0-9_]*)')
            match = re.match(col_pattern, filter)
            
            if match:
                col_id = match.group(1)
                value = match.group(2)
                
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
    
    where_clause = " AND ".join(conditions)
    return where_clause

filter_query = 'name contains "John" && age > "30"'
