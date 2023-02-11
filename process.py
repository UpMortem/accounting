import csv

def remove_symbols(description):
    symbols = ['.', ',', '-', '(', ')', '$']
    for symbol in symbols:
        description = description.replace(symbol, '')
    return description

def find_category(description, mappings):
    max_len = 0
    category = 'Ask My Accountant'
    for k, v in mappings.items():
        if k in description and len(k) > max_len:
            max_len = len(k)
            category = v
    return category

def remove_DES(description):
    if 'DES' in description:
        return description[:description.index('DES')].strip()
    return description

def process_current_file(mappings):
    with open('current.csv', 'r') as current_file, open('output.csv', 'w', newline='') as output_file:
        current_reader = csv.reader(current_file)
        output_writer = csv.writer(output_file)

        header = ['Date', 'Description', 'Category', 'Amount']
        output_writer.writerow(header)

        next(current_reader)
        for row in current_reader:
            date = row[0]
            description = remove_symbols(row[1])
            category = find_category(description, mappings)
            description = remove_DES(description)
            amount = row[2]

            output_writer.writerow([date, description, category, amount])

def get_mappings():
    mappings = {}
    with open('final.csv', 'r') as final_file:
        final_reader = csv.reader(final_file)
        next(final_reader)
        for row in final_reader:
            description = remove_symbols(row[1])
            category = row[2]
            mappings[description] = category
    return mappings

if __name__ == '__main__':
    mappings = get_mappings()
    process_current_file(mappings)

