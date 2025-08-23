import csv
import re
import os

def clean_positional_rank(file_path):
    # Read the original data
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        headers = reader.fieldnames

    # Modify the PositionalRank
    for row in data:
        if row.get('PositionalRank'):
            # Remove all non-digit characters
            row['PositionalRank'] = re.sub(r'\D', '', row['PositionalRank'])

    # Write the modified data back to the file
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

if __name__ == '__main__':
    file_to_clean = r'c:\git\fantasy\fantasy_players.csv'
    clean_positional_rank(file_to_clean)
    print(f"Cleaned {file_to_clean}")
