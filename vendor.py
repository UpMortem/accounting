import csv

# Read in the final.csv file and create a dictionary mapping descriptions to categories
final_mapping = {}
with open('final.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        description = row['Description'].replace('&amp;', '').replace('&amp;', '')
        category = row['Category']
        final_mapping[description] = category

# Read in the current.csv file and create a list of output rows
output_rows = []
with open('current.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Clean up the description
        description = row['Description'].replace('&amp;', '').replace('&amp;', '').replace('DES', '').split(' ')[0]
        
        # Find the longest matching description in the final_mapping dictionary
        matched_description = ''
        for final_description in final_mapping:
            if final_description in description:
                if len(final_description) > len(matched_description):
                    matched_description = final_description
        
        # Determine the category for the output row
        if matched_description:
            category = final_mapping[matched_description]
        else:
            category = 'Ask My Accountant'
        
        # Determine the vendor for the output row
        vendor = ''
        for final_description in final_mapping:
            if final_description in row['Description']:
                vendor = row['Description'].split('REF')[0].replace('DES', '').replace('&amp;', '').strip()
        if not vendor:
            vendor = row['Description'].replace('&amp;', '').strip()
        
        # Add the output row to the list
        output_rows.append({
            'Date': row['Date'],
            'Vendor': vendor,
            'Description': matched_description or description,
            'Category': category,
            'Amount': row['Amount']
        })

# Write the output rows to a new CSV file
with open('output.csv', 'w', newline='') as f:
    fieldnames = ['Date', 'Vendor', 'Description', 'Category', 'Amount']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in output_rows:
        writer.writerow(row)

