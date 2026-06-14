# Data Annotation Coding Exercise 
# Decoding a Secret Message 
# By: Asa Jean Soriano
#
# A Google Doc contains a list of Unicode characters and 2D grid positions 
# This program writes a function taking in a Google Doc URL as an argument.
# Then it parses data from the doc.
# The external library used for this project is BeautifulSoup
# from the bs4 module used for parsing the Google Doc without API concerns.

import requests
from bs4 import BeautifulSoup


# Cleanly prints data table with formatting
def print_data_table(table: str):
    # Find max string length in all cells in table
    max_cell_len = max(len(str(col)) for row in table for col in row)

    # Default to 16 character width limit if all cells are shorter
    # otherwise scale up to fit longest text +2 for padding
    col_width = max(16, max_cell_len + 2)

    for row in table:
        for col in row:
            print(f"{col:<{col_width}}", end = "")
        print()


# Function to parse a Google Doc taking a Google Doc URL as argument
# Retrieves and parses unicode characters in the grid
# and the x-y coords for each character
# Returns a string of parsed data
def google_doc_parser(URL: str) -> str:

    # Standard header browsers to prevent issues with webpage requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # Get raw HTML content from URL
        response = requests.get(URL)
        
        # Throw error if unable to fetch document from URL.
        if response.status_code != 200:
            return f"Error: Unable to fetch document. Status code {response.status_code}"
        
        # Parse HTML content 
        content = BeautifulSoup(response.text, 'html.parser')
        
        # Skip any text and go straight to data table within doc
        # Then extract data table from doc
        table = content.find('table')

        # Initialize new list data to insert data table extraction from table
        data = []

        # Iterates through each row and prints each cell
        for row in table.find_all('tr'):
            #Initalize temporary current row
            row_data = []

            # Extract data from each cell in this row
            for cell in row.find_all('td'):
                cell_data = cell.get_text().strip()
                row_data.append(cell_data) # Add to current row list
                #print(cell_data)

            # Append if row contains cells
            if row_data:
                data.append(row_data)

        # Cleanly print data table with helper function
        #print_data_table(data)


        # Return parsed data
        return data
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


# Print unicode characters in given x-y coords from data table
def print_grid_characters(table: list):

    coords_and_chars = []
    max_x = 0
    max_y = 0

    for row in table:
        # Skip header row
        if not row or any(c.isalpha() for c in str(row[0])):
            continue

        # Convert coords to ints and get char
        x = int(row[0])
        char = row[1]
        y = int(row[2])

        coords_and_chars.append((x, char, y))

        # Get largest coords for grid size
        if x > max_x: max_x = x
        if y > max_y: max_y = y

    # Initialize 2D grid and fill with spaces using max dimensions + 1
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Populate grid with characters
    for x, char, y in coords_and_chars:
        grid[y][x] = char

    # Print grid
    for row in grid:
        print("".join(row))


# Testing
test_URL = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
table = google_doc_parser(test_URL)
#print("Parsed text:")
#print(parsed_text)

print_grid_characters(table)