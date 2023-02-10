import csv
import re

def clean_description(desc):
    # Clean up the description by removing symbols
    return re.sub(r'[^\w\s]', '', desc).strip()

def get_category(description, categories_map):
    # Get the longest substring match for the description
    clean_desc = clean_description(description)
    match = max(categories_map, key=lambda x: len(x) if clean_desc.find(x) != -1 else 0)
    return categories_map[match] if match else 'Ask My Accountant'

# Read the final.csv file
with open('final.csv', 'r') as f:
    reader = csv.reader(f)
    categories_map = {clean_description(row[1]): row[2] for row in reader if row[0] != 'Date'}

# Read the current.csv file and write to the output.csv file
with open('current.csv', 'r') as f_in, open('output.csv', 'w', newline='') as f_out:
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)
    
    # Write the header row to the output file
    writer.writerow(['Date', 'Description', 'Category', 'Amount'])
    
    for row in reader:
        if row[0] == 'Card':
            # Skip the header row
            continue
        
        # Get the date, description, and amount
        date = row[1]
        desc = row[3]
        amount = row[6]
        
        # Clean up the description and remove "DES" and everything after it
        clean_desc = clean_description(desc)
        desc = re.sub(r'DES.*', '', clean_desc).strip()
        
        # Get the category using the categories map
        category = get_category(desc, categories_map)
        
        # Write the row to the output file
        writer.writerow([date, desc, category, amount])

