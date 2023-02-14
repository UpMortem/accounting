import csv

def count_matching_words(description1, description2):
    # Convert both descriptions to lowercase and split into words
    words1 = description1.lower().split()
    words2 = description2.lower().split()

    # Count the number of matching words
    matching_words = len(set(words1) & set(words2))

    return matching_words

def get_vendor_and_category(description, final_data):
    max_matching_words = 0
    vendor = ''
    category = ''
    for row in final_data:
        matching_words = count_matching_words(description, row[2])
        if matching_words > max_matching_words:
            max_matching_words = matching_words
            vendor = row[1]
            category = row[3]

    if max_matching_words == 0:
        vendor = description[:50] + '...'

    return vendor, category

def generate_output_csv(final_file, current_file, output_file):
    with open(final_file, 'r') as f:
        final_data = list(csv.reader(f))[1:]
        
    with open(current_file, 'r') as f:
        current_data = list(csv.reader(f))[1:]
        
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Vendor', 'Description', 'Category', 'Amount'])
        for row in current_data:
            date = row[0]
            description = row[1]
            amount = row[2]
            vendor, category = get_vendor_and_category(description, final_data)
            if vendor == '':
                vendor = 'Ask My Accountant'
                category = ''
            writer.writerow([date, vendor, description, category, amount])

generate_output_csv('final.csv', 'current.csv', 'output.csv')

