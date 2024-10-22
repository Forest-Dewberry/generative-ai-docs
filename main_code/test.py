import requests
import csv
import os

# Define a function to get AI definition for a given term and write it to a CSV
def get_ai_definition(api_key, term, csv_filename):
    # URL for the API call
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'
    
    # API request headers and data
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Define the term '{term}'"
                    }
                ]
            }
        ]
    }

    # Send the POST request to get the definition
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    # Extract the AI-generated definition from the response
    try:
        ai_definition = response_data['candidates'][0]['content']['parts'][0]['text']
    except KeyError:
        print(f"Failed to get a definition for {term}.")
        return
    
    # Check if the CSV file exists; if not, create it with headers
    file_exists = os.path.isfile(csv_filename)
    
    # Write the term and definition to the CSV file
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write header if file doesn't exist
            writer.writerow(['term', 'ai-definition'])
        writer.writerow([term, ai_definition])

    print(f"Definition for '{term}' has been written to '{csv_filename}'.")

# Example usage:
api_key = input("Please enter your API key: ")
terms = ['AI', 'Machine Learning', 'Neural Networks', 'Supervised Learning']

# Call the function for each term and append the result to 'terms_definitions.csv'
for term in terms:
    get_ai_definition(api_key, term, 'terms_definitions.csv')
