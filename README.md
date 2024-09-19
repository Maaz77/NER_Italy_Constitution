# NER_Italy_Constitution
The repo demonstrates the implementations of the solution for finding some administrative entities inside the text of the Italy constitution.
You can find the PDF file of the Italy Constitution here: http://www.senato.it/sites/default/files/media-documents/Costituzione_ITALIANO.pdf. Make sure to download it, and copy it in the same directory of the codes. 

For executing the file "NER_LLM.py" you need to have "Groq cloud" API key(https://console.groq.com/keys).

NER_Classic.py contains methods to extract text from a PDF file and perform Named Entity Recognition (NER) using custom rules defined with spaCy's Matcher.

NER_LLM.py file contains a function to generate a prompt for a named entity recognition (NER) task on the text of the Italian Constitution and send it to a language model for processing(llama3-70b). 

The two JSON files are the output of two Python files.
