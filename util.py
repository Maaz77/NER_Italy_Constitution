import json 
import re
import pdfplumber


def extract_dictionaries_from_string(input_string):
    """
    Extracts a list of dictionaries from a given string.
    This function removes all whitespace characters (spaces, newlines, and tabs) from the input string,
    then searches for a JSON array (enclosed in square brackets) within the string. If a JSON array is found,
    it attempts to decode it into a list of dictionaries.
    Args:
        input_string (str): The input string potentially containing a JSON array.
    Returns:
        list[dict] or None: A list of dictionaries if the JSON array is successfully decoded, 
                            None if no JSON array is found or if there is an error in decoding.
    """
    input_string = input_string.replace(" ", "")
    input_string = input_string.replace("\n", "")
    input_string = input_string.replace("\t", "")
    pattern = r'\[.*\]'
    match = re.search(pattern, input_string)
    if match:
        json_str = match.group(0)
        try:
            dictionaries = json.loads(json_str)
            return dictionaries
        
        except json.JSONDecodeError:
            print("Error decoding JSON")
            return None
    else:
        print("No JSON array found in the string")
        return None

def write_json_to_file(json_obj):
    with open("entities_LLM_2.json", "a") as f:
        json.dump(json_obj, f, indent=4)
    
# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path , start_page = None, end_page = None):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(start_page, end_page):
            text += pdf.pages[i].extract_text()
    return text, len(text)

# Function to return the number of pages in a PDF
def get_number_of_pages(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return len(pdf.pages)


#Function to add a number to "span_start" and "span_end" of every memeber in an array of jsons 
def add_number_to_json_array(json_array, number):
    """
    Adds a specified number to the 'span_start' and 'span_end' fields of each JSON object in a given array.

    Args:
        json_array (list of dict): A list of JSON objects, each containing 'span_start' and 'span_end' keys.
        number (int): The number to add to the 'span_start' and 'span_end' fields.

    Returns:
        list of dict: The modified list of JSON objects with updated 'span_start' and 'span_end' values.
    """
    for json_obj in json_array:
        json_obj["span_start"] += number
        json_obj["span_end"] += number
    return json_array
 
