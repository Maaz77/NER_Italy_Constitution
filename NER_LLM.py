import os
import json
from groq import Groq
from util import *




def prompt_llm(context):
    # Prompt to identify the specific entities and provide an example for one-shot learning
    prompt = f"""
    You are a named entity recognition system. 
    I will provide you with the text of the Italian Constitution, and I want you to identify the following administrative entities and their positions in the text:
    - Camera, Camera dei Deputati
    - Senato, Senato della Repubblica
    - Presidente della Repubblica
    - Governo
    - Regione
    - Parlamento
    - Consiglio superiore della magistratura
    - Consiglio

    For each entity, provide the start and end positions (character indices) in the text. Do it for all occurrences of these entities in the whole text.
    Return the result only as a JSON array where each object has the following structure:
    [
        {{
            "iri": "iri_of_entity",      
            "label": "label_of_entity",  
            "span_start": start_index,   
            "span_end": end_index        
        }},
        ...
    ]

    Here is an example:
    [
        {{
            "iri": "camera_deputati",
            "label": "Camera dei Deputati",
            "span_start": 42,
            "span_end": 61
        }}
    ]
    Now, here is the text of the Italian Constitution:
    {context}
    """

    # Write the prompt to a text file
    with open("prompt.txt", "w") as f:
        f.write(prompt)

    # Make the request to the LLM
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-70b-8192",
        temperature=0.1,
        max_tokens= 8191,
        top_p=1,
    )
    result_raw = chat_completion.choices[0].message.content

    # Write the response to a text file
    with open("LLM_response.txt", "w") as f:
        f.write(result_raw)

    return result_raw

def main():

    # Initialize the LLM client
    global client
    client = Groq(
    api_key="YOUR_API_KEY",
    )


    # Path to the PDF file
    pdf_path = "Costituzione_ITALIANO.pdf"

    page_numbers = get_number_of_pages(pdf_path)

    #a for loop over number of pages jumps every 5 pages
    last_index = 0 
    for i in range(0, page_numbers, 5):
        # Extract the text from the PDF
        pdf_text , lenght = extract_text_from_pdf(pdf_path , start_page=i, end_page=i+5) 

        

        # Prompt the LLM with the text
        result_raw = prompt_llm(pdf_text)
        # Extract the dictionaries from the LLM response
        entities = extract_dictionaries_from_string(result_raw)

        entities = add_number_to_json_array(entities, last_index)

        last_index += lenght

        # Write the entities to a JSON file
        write_json_to_file(entities)
    
    
    if (page_numbers % 5 != 0):
        pdf_text , lenght = extract_text_from_pdf(pdf_path , start_page=page_numbers - (page_numbers % 5), end_page=page_numbers) 
        result_raw = prompt_llm(pdf_text)
        entities = extract_dictionaries_from_string(result_raw)
        entities = add_number_to_json_array(entities, last_index)
        write_json_to_file(entities)



if __name__ == "__main__":

    main()
