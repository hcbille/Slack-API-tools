import csv

input_str = input("Enter row to remove (e.g. 'row 50'): ")

# Parse input string to determine row to remove
row_to_remove = int(input_str.split()[1])

# Remove specified rows from CSV file
with open('users_channels.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader) # save header row
    rows = list(reader)
    
with open('users_channels.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header) # write header row
    if row_to_remove > 1:
        writer.writerows(rows[row_to_remove-2:])