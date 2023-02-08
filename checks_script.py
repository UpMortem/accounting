import csv
import re
import requests
import time
from categories import INCOME

#OPENAI_API_KEY = "X"
OPENAI_API_KEY = "X"
cache = dict()

# Function to remove lines starting with "Check"
def remove_check(input_str):
    if input_str[:5] == 'Check':
        return ""
    else:
        return input_str

def has_check(input_str):
    if input_str[:5] == 'Check':
        return True
    else:
        return False

# Function to remove extra characters from second column
def remove_extra(input_str):
    return re.sub('[^A-Z]','',input_str)

# Function to get the accounting type from GPT-3
def get_category_type(input_str, error_count):
    if error_count == 3:
      error_count = 0 
      return "Ask My Accountant"
    print("input_str: " + input_str)
    input_str = input_str.upper()
    categories = ",".join(INCOME)
    input_str = ''.join([i for i in input_str if not i.isdigit()])
    if input_str not in cache:
        url = 'https://api.openai.com/v1/engines/davinci/completions'
        headers = {'Authorization': 'Bearer ' + OPENAI_API_KEY}
        data = {'prompt': "The following closed set categories are business income types and only select from this given set:\n\n \"%s\" \n Default to \"Ask My Accountant\" if certainty is less than 50 percent. \n\n \"%s\"\nCategory:"%(categories, input_str), 'max_tokens': 1000, 'top_p': 1.0, 'stream': False, 'temperature': 0.7, 'frequency_penalty': 0.0, 'presence_penalty':0.0}
        #data = {'prompt': "Given the following categories of expense types \"%s\" which category does \"%s\" belong to? Default to \"Ask My Accountant\" if none match."%(categories, input_str), 'max_tokens': 1000, 'top_p': 1.0, 'stream': False, 'temperature': 0, 'frequency_penalty':0.0, 'presence_penalty'=0.0}
        print(data['prompt'])
        time.sleep(1)
        response = requests.post(url, headers=headers, json=data)
        print(response.json())
        if 'error' in response.json():
            error_count += 1
            print("Sleeping 3 seconds")
            time.sleep(3)
            return get_category_type(input_str, error_count)
        sep = '\n'
        stripped = response.json()['choices'][0]['text'].split(sep, 1)[0]
        cache[input_str] = stripped.strip()
        print("Summary: " + cache[input_str])
        error_count = 0 
        return cache[input_str].strip()
    else:
        error_count = 0
        print("Summary: " + cache[input_str])
        return cache[input_str].strip() 


def get_merchant_name(input_str):
    longest = ""
    current = ""
    for char in input_str: 
        if char.isalpha() or char == " ":
            current += char 
            if len(longest) < len(current):
                longest = current 
        else: 
            current = ""
    return longest

# Main program
with open("transactions.csv") as csv_file, open("checks_tab.csv", "w") as output_file:
    csv_reader = csv.reader(csv_file, delimiter=",")

    output_writer = csv.writer(output_file, delimiter=",")

    line_count = 0
    for row in csv_reader:
        if line_count > 8 and float(row[2]) < 0.0:
            row[1] = get_merchant_name(row[1])
            row[3] = float(row[2])
            row[2] = get_category_type(row[1], 0).replace('"','')
            row.append(row[1])
            # Don't include any checks for withdrawals
            if has_check(row[1]):
                output_writer.writerow(row)
            else:
                pass
        line_count += 1
