import requests

# Prompt the user for the API key
api_key = input("Please enter your API key: ")

# For testing. Define term
term_to_be_defined = input("Enter term to be defined: ")
if not term_to_be_defined:
    term_to_be_defined = 'ACL'

# Define the URL with the user's API key
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'
headers = {
    'Content-Type': 'application/json'
}
data = {
    "contents": [
        {
            "parts": [
                {
                    "text": f' Give definition, significance, context, and related terms, related to security+ 701 objectives: {term_to_be_defined}'
                }
            ]
        }
    ]
}

# Send the POST request
response = requests.post(url, headers=headers, json=data)

# Print the response (you may want to handle the response as needed)
print(response.json())

# Parse the JSON response
response_data = response.json()

# Extract the explanation text from the response
explanation_text = response_data['candidates'][0]['content']['parts'][0]['text']

# Write the explanation text to a file
with open('ai_explanation.txt', 'w') as file:
    file.write(explanation_text)

print("AI explanation has been written to 'ai_explanation.txt'")

print('')
print(locals())







# write to csv
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
