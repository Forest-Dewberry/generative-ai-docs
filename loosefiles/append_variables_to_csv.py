import csv
from datetime import datetime

# Function to filter out user-defined variables
def get_user_defined_variables():
    all_vars = globals()  # You can also use locals() in a function's local scope
    user_defined_vars = {key: value for key, value in all_vars.items() if not key.startswith("__") and not callable(value)}
    return user_defined_vars

# censor these variables
def get_censored_vars(input_vars):
    censored_vars = {key: value for key, value in input_vars.items() if not 'api' in key and not 'api' in value and not 'key' in key and not 'key' in value}
    return censored_vars

# Function to append the variables to a CSV file with a timestamp
def append_vars_to_csv(csv_filename):
    # Get the user-defined variables
    defined_vars = get_user_defined_variables()
    defined_vars = get_censored_vars(defined_vars)
    
    # Append each variable and its value to the CSV file with a timestamp
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # If this is the first time writing, include headers
        writer.writerow(['variable_name', 'variable_value', 'timestamp'])
        
        # Write each variable and its value with the current timestamp
        for var_name, var_value in defined_vars.items():
            writer.writerow([var_name, var_value, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

# Example usage: 
append_vars_to_csv('user_defined_variables.csv')

# After this, you should see a CSV file named 'user_defined_variables.csv' with all your variables.
