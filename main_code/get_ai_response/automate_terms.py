import pdb
import time
import SecurityPlusTermAPI
user_input_key = input("api key: ")
myAPIobj = SecurityPlusTermAPI.SecurityPlusTermAPI(user_input_key)

import GenericGeminiAPI
user_input_key = input("api key: ")
myGenAPIobj = GenericGeminiAPI.GenericGeminiAPI(user_input_key)

import subprocess

# Start a persistent Bash process
process = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Function to send commands to the process
def send_command(command):
    process.stdin.write(f"{command}\n")
    process.stdin.flush()

def failure_resist_define_term(myAPIobj, term_in):
    attempt = 0
    success = False
    max_retries = 10
    while attempt < max_retries and not success:
        try:
            # Your operation here (e.g., define_term)
            myAPIobj.define_term(term_in)
            # Mark as success if no exceptions occurred
            success = True
        except Exception as e:
            attempt += 1
            print(f"Error on item {term_in}: {e}")
            print(f"Retrying... ({attempt}/{max_retries})")
            # Optional: delay between retries
            time.sleep(1)
    if not success:
        print(f"Failed to process item {item} after {max_retries} retries.")


import csv

# Open the file with the relative path
file_path = '../inputs/shortListSecurityPlus701Terms.csv'

with open(file_path, mode='r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for i,row in enumerate(csv_reader):
        print(row[1])  # Each row is a list of values
        acronym, ac_spelled_out = row
        # make resistant to failure
        failure_resist_define_term(myAPIobj,ac_spelled_out) # myAPIobj.define_term(ac_spelled_out)
        myAPIobj.write_to_file('asdf.tmp')
        myGenAPIobj.read_prompt_from_file('asdf.tmp')
        genApiDefTerm = ('Please shorten the following text while retaining its core meaning and clarity, eliminating empty lines and minimizing line breaks and keeping the information but writing in paragraph form:\n' \
        + myGenAPIobj.prompt_in )
        failure_resist_define_term(myGenAPIobj,genApiDefTerm) #myGenAPIobj.define_term
        myGenAPIobj.write_to_file('asdf.tmp')
        afterTerm = ';afterTerm;'
        afterCard = ';afterCard;'
        send_command(f'echo "{acronym}" >> terms_and_defs.txt \n')
        send_command(f'echo "{afterTerm}" >> terms_and_defs.txt \n')
        send_command('cat asdf.tmp >> terms_and_defs.txt \n')
        send_command(f'echo "\n{afterCard}" >> terms_and_defs.txt \n')
        # pdb.set_trace()
        # if i > 2:
        #     break




process.stdin.write("exit\n")  # Exit the shell when done

# print a newline
print('')

# Get the output
output, error = process.communicate()

print(f"Output: {output}")
if error:
    print(f"Error: {error}")

