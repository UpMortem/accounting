import csv

# Open the input and output files
inFile = open('transactions.csv', 'r')
outFile = open('checks_tab.csv', 'w')

# Create a reader and writer object 
reader = csv.reader(inFile)
writer = csv.writer(outFile, delimiter='\t')

# Skip the first 8 lines
next(reader) # Skips the header row
for i in range(7):
    next(reader)

# Iterate through the rows
for row in reader:
    # Check if the row is a check
    if row[1].startswith('Check'):
        # If it is a check, store the values
        date = row[0]
        description = row[1][6:] # Removes 'Check' from the description
        amount = row[3]
        # Write the row to the output file
        writer.writerow([date, '', '', amount, description])

# Close the files
inFile.close()
outFile.close()
