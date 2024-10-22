import requests
import csv
from datetime import datetime
import os
from pathlib import Path

# import pdb


class GenericGeminiAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}'
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.explanation_text = None
        self.response_data = None
        self.prompt_in = None

    def define_term(self, prompt='what is color theory?'):
        # Define the payload
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f'{prompt}'
                        }
                    ]
                }
            ]
        }

        # Send the POST request
        response = requests.post(self.url, headers=self.headers, json=data)
        
        # Check if response is valid
        if response.status_code == 200:
            self.response_data = response.json()
            # Extract the explanation text from the response
            self.explanation_text = self.response_data['candidates'][0]['content']['parts'][0]['text']
            # self.append_vars_to_csv('/workspaces/generative-ai-docs/outputs/user_defined_variables.csv') # currently not working
        else:
            print(f"Error: {response.status_code}, {response.text}")
        
        return self.explanation_text

    def write_to_file(self, filename='GenericGeminiAPI_out.txt'):
        if self.explanation_text:
            # Write the explanation text to a file
            with open(filename, 'w') as file:
                file.write(self.explanation_text)
            print(f"AI explanation has been written to '{filename}'")
        else:
            print("No explanation text available to write.")

    def read_prompt_from_file(self, filename='GenericGeminiAPI_prompt_in.txt'):
        try:
            # Read the prompt from the file
            with open(filename, 'r') as file:
                self.prompt_in = file.read().strip()  # Store the content in an instance variable `prompt_in`
        except FileNotFoundError:
            print(f"The file '{filename}' does not exist.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    def set_prompt(self, prompt=None, filename=None):
        if prompt:
            # Set the prompt directly if provided
            self.prompt_in = prompt
            print("Prompt has been set manually.")
        elif filename:
            # If a filename is provided, read the prompt from the file
            self.read_prompt_from_file(filename)
        else:
            print("No prompt provided. Please either pass a prompt or a filename.")

    def get_user_defined_variables(self):
        # Get all the user-defined variables in the current instance
        all_vars = vars(self)
        user_defined_vars = {key: value for key, value in all_vars.items() if not key.startswith("__") and not callable(value)}
        return user_defined_vars

    def get_censored_vars(self, input_vars):
        # Filter out sensitive variables
        censored_vars = {key: value for key, value in input_vars.items() if not 'api' in key and not 'api' in value and not 'key' in key and not 'key' in value}
        return censored_vars

    def append_vars_to_csv(self, csv_filename='user_defined_variables.csv'):
        # Get the user-defined variables
        pdb.set_trace()
        defined_vars = self.get_user_defined_variables()
        censored_vars = self.get_censored_vars(defined_vars)

        out_path = '/workspaces/generative-ai-docs/main_code/outputs/'
        csv_filename = out_path + csv_filename

        file_path = Path(csv_filename)

        if file_path.exists():
            print("File exists")
            file_exists = True
        else:
            print("File does not exist")
            file_exists = False
        
        # Append each variable and its value to the CSV file with a timestamp
        with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write headers only if the file is new
            if not file_exists:  # Check if file is empty
                writer.writerow(['variable_name', 'variable_value', 'timestamp'])
            
            # Set the timestamp (this way all timestamps for a single run are the same)
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            
            # Write each variable and its value with the current timestamp
            for var_name, var_value in censored_vars.items():
                writer.writerow([var_name, var_value, timestamp])
        print(f"Variables have been appended to '{csv_filename}'")

if __name__ == '__main__':
    # Example usage:
    api_key = input("Please enter your API key: ")
    security_plus_api = GenericGeminiAPI(api_key)

    # Define term and write explanation to file
    term = input("Enter term to be defined: ")
    explanation = security_plus_api.define_term(term)
    if explanation:
        print(explanation)
        security_plus_api.write_to_file()

    # Append user-defined variables to CSV
    security_plus_api.append_vars_to_csv()
