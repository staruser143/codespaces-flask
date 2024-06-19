import timeit

# Define the setup code for timeit
setup_code = '''
from __main__ import dash_filter_to_sql_direct, dash_filter_to_sql_regex, filters, filter_query
'''

# Define the code to be executed for the direct approach
test_code_direct = '''
dash_filter_to_sql_direct(filters)
'''

# Define the code to be executed for the regex approach
test_code_regex = '''
dash_filter_to_sql_regex(filter_query)
'''

# Measure the execution time of both approaches
time_direct = timeit.timeit(stmt=test_code_direct, setup=setup_code, number=10000)
time_regex = timeit.timeit(stmt=test_code_regex, setup=setup_code, number=10000)

print(f"Direct mapping approach time: {time_direct:.6f} seconds")
print(f"Regex parsing approach time: {time_regex:.6f} seconds")
