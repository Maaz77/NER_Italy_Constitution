from PyPDF2 import PdfReader
import spacy
from spacy.matcher import Matcher
import json
nlp = spacy.load("it_core_news_sm")


def get_pdf_text(path_pdf):
    
    text = ""
    
    pdf_reader = PdfReader(path_pdf)
    #print(len(pdf_reader.pages))
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Step 2: Use spaCy NER with Custom Matcher for Specific Entities
def perform_ner_with_custom_rules(text):
    doc = nlp(text)  # Apply spaCy's model to the text
    matcher = Matcher(nlp.vocab)
    
    # Define patterns to match the specific entities you want
    patterns = [
            [
                {"LOWER": {"IN": ["la", "il", "della", "nella", "di", "alla", "le", "al", "Ciascuna"]}, "OP": "?"},
                {"LOWER": "camera"},
                {"LOWER": "dei", "OP": "?"},  # Optional "dei"
                {"LOWER": "deputati", "OP": "?"}  # Optional "deputati"
                ],

            [   {"LOWER": {"IN": ["il", "del", "nel", "al", "dal", "sul"]}, "OP": "?"},
                {"LOWER": "senato"},
                {"LOWER": "della", "OP": "?"},  # Optional "della"
                {"LOWER": "repubblica", "OP": "?"}
                ],  # Optional "Repubblica"

            [
                {"LOWER": {"IN": ["la", "il", "della", "nella", "di", "alla", "le", "al"]}, "OP": "?"},
                {"LOWER": "presidente"}, {"LOWER": "della"}, {"LOWER": "repubblica"}
                ] ,  # Match "Presidente della Repubblica"

            [
                {"LOWER": {"IN": ["la", "il", "della", "nella", "di", "alla", "le", "al"]}, "OP": "?"},
                {"LOWER": "governo"}
                ],  # Match "Governo"

            [
                {"LOWER": {"IN": ["la", "il", "della", "nella", "di", "alla", "le", "al"]}, "OP": "?"},
                {"LOWER": "regione"}
                ],  # Match "Regione"

            [
                {"LOWER": {"IN": ["la", "il", "della", "nella", "di", "alla", "le", "al"]}, "OP": "?"},
                {"LOWER": "parlamento"}
                ],  # Match "Parlamento"
            [
                {"LOWER": {"IN": ["la", "il", "della", "nella", "di", "alla", "le", "al"]}, "OP": "?"},
                {"LOWER": "consiglio"}, {"LOWER": "superiore"}, {"LOWER": "della"}, {"LOWER": "magistratura"}
                ],  # Match "Consiglio superiore della magistratura"
            [
                {"LOWER": {"IN": ["la", "il", "della", "nella", "di", "alla", "le", "al"]}, "OP": "?"},
                {"LOWER": "consiglio"}
                ]  # Match "Consiglio"
    ]

    Labels = ["Camera dei Deputati", "Senato della Repubblica", "Presidente della Repubblica", "Governo", "Regione", "Parlamento", "Consiglio superiore della magistratura", "Consiglio"]    
    # Add the patterns to the matcher
    for label, pattern in zip(Labels, patterns):
        matcher.add(label, [pattern] , greedy="FIRST")
    
    # Apply the matcher to the doc
    matches = matcher(doc)
    
    # Collect matched entities and their spans
    entities = []
    for match_id, start, end in matches:
        span = doc[start:end]
        thelable = nlp.vocab.strings[match_id]
        entities.append({
            "iri": thelable.lower().replace(" ", "_"),
            "label": thelable,
            "span_start": span.start_char,
            "span_end": span.end_char,
            
        })
    
    return entities




def main():

    pdf_path = 'Costituzione_ITALIANO.pdf' 
    
    text = get_pdf_text(pdf_path)
    entities = perform_ner_with_custom_rules(text)

    # Print the entities in a JSON file format
    with open('entities.json', 'w', encoding='utf-8') as f:
        json.dump(entities, f, ensure_ascii=False, indent=4)






   







if __name__ == "__main__":
    main()