import csv
from collections import defaultdict
import re

# Read in the final.csv file and store the data in a dictionary
final_data = defaultdict(list)
with open('final.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        final_data[row['Description']].append(row)

# Helper function to extract the account number from a description
def extract_account_number(description):
    match = re.search(r'XXXXXX(\d+)', description)
    if match:
        return match.group(1)
    return None

# Read in the current.csv file and generate the output.csv file
with open('current.csv', 'r') as f, open('output.csv', 'w', newline='') as out_file:
    reader = csv.DictReader(f)
    writer = csv.DictWriter(out_file, fieldnames=['Date', 'Vendor', 'Description', 'Category', 'Amount'])
    writer.writeheader()

    for row in reader:
        # Find the final.csv entry that matches the most number of words
        # in the current.csv description
        description_words = row['Description'].lower().split()
        matching_entry = None
        for desc, entries in final_data.items():
            desc_words = desc.lower().split()
            num_matches = sum(1 for word in description_words if word in desc_words)
            if matching_entry is None or num_matches > matching_entry['num_matches']:
                matching_entry = {'num_matches': num_matches, 'entry': entries[0]}

        # Use the matching final.csv entry to populate the output.csv row
        if matching_entry['num_matches'] > 0:
            output_row = {
                'Date': row['Date'],
                'Description': row['Description'],
                'Amount': row['Amount'],
            }

            # If the vendor starts with "ONLINE TRANSFER", extract the account number
            vendor = matching_entry['entry']['Vendor']
            if vendor.startswith('ONLINE TRANSFER'):
                account_number = extract_account_number(row['Description'])
                if account_number is not None:
                    vendor = f"ONLINE TRANSFER {account_number}"

            output_row['Vendor'] = vendor
            output_row['Category'] = matching_entry['entry']['Category']
        else:
            # If there is no matching entry, use "Ask My Accountant" as a placeholder
            output_row = {
                'Date': row['Date'],
                'Vendor': 'UNKNOWN',
                'Description': row['Description'],
                'Category': 'Ask My Accountant',
                'Amount': row['Amount'],
            }

        writer.writerow(output_row)

