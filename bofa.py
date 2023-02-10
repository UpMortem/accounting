import csv
import re

def read_csv(file_name):
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        return list(reader)

def write_csv(file_name, data):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def clean_description(description):
    # remove all symbols
    description = re.sub(r'[^\w\s]', '', description)
    # remove everything after "DES"
    description = re.sub(r'\bDES.*', '', description)
    return description.strip()

def get_category(description, final_data):
    # find the longest substring match
    max_length = 0
    match = None
    for row in final_data:
        final_description = clean_description(row[1])
        if description in final_description and len(final_description) > max_length:
            match = row[2]
            max_length = len(final_description)
    if match:
        return match
    else:
        return "Ask My Accountant"

final_data = read_csv("final.csv")
current_data = read_csv("current.csv")

output_data = []
for row in final_data:
    output_data.append(row[:4])

for row in current_data[1:]:
    date = row[0]
    description = clean_description(row[1])
    amount = row[2]
    category = get_category(description, final_data)
    output_data.append([date, description, category, amount])

write_csv("output.csv", output_data)

