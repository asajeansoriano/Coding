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
import re


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
        
        # Skip any text and data table within doc
        # Then extract data table from doc
        table = content.find('table')

        # Initialize new string data to insert data table extraction from table
        data = ""

        # Iterates through each row and prints each cell
        for row in table.find_all('tr'):
            # Extract raw text from each cell in row and insert into data
            data = [cell.get_text().strip() for cell in row.find_all('td')]

            # Print row
            print(data)

        # Return parsed data
        #return document_text.strip()
        return data
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


# Testing
test_URL = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
parsed_text = google_doc_parser(test_URL)
#print("Parsed text: " + parsed_text)