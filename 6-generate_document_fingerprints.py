import os
import spacy
import numpy as np
from collections import Counter

# Load the English language model from SpaCy
nlp = spacy.load("en_core_web_sm")

# Function to extract phrases from a sentence using SpaCy
def extract_phrases(sentence):
    doc = nlp(sentence)
    phrases = [chunk.text for chunk in doc.noun_chunks]
    print("Processing Sentence : ")
    print(f"\t{phrases}")
    print(f"Phrases : ")
    print(",".join(phrases))
    return phrases

# Function to load fingerprint matrix from file
def load_fingerprint_matrix(phrase):
    fingerprint_filename = os.path.join("fingerprints", f"{phrase.replace(' ', '_')}_fingerprint.txt")
    if not os.path.exists(fingerprint_filename):
        print(f"Fingerprint file for '{phrase}' not found.")
        return None
    with open(fingerprint_filename, "r", encoding="utf-8") as file:
        fingerprint_matrix = np.array([[int(value) for value in line.strip().split("\t")] for line in file])
    return fingerprint_matrix

# Function to generate document fingerprint by summing phrase fingerprints
def generate_doc_fingerprint(sentence, phrase_fingerprints):
    # doc_fingerprint = np.zeros_like(phrase_fingerprints[0])
    doc_fingerprint = np.zeros_like(next(iter(phrase_fingerprints.values())))

    phrases = extract_phrases(sentence)
    print("|||>>>>>>> Doc Fingerprints ")
    for phrase in phrases:
        if phrase in phrase_fingerprints:
            doc_fingerprint += phrase_fingerprints[phrase]
            print(doc_fingerprint)

    return doc_fingerprint


# Main function
def main():
    # Create a new folder for document fingerprints if it doesn't exist
    doc_fingerprints_folder = "doc_fingerprints"
    os.makedirs(doc_fingerprints_folder, exist_ok=True)

    # Load phrase fingerprints into a dictionary
    phrase_fingerprints = {}
    for phrase_filename in os.listdir("fingerprints"):
        phrase = phrase_filename.split("_fingerprint")[0].replace('_', ' ')
        fingerprint_matrix = load_fingerprint_matrix(phrase)
        if fingerprint_matrix is not None:
            phrase_fingerprints[phrase] = fingerprint_matrix

    # Read the corpus.txt file and generate document fingerprints
    with open("corpus.txt", "r", encoding="utf-8") as corpus_file:
        for line_number, sentence in enumerate(corpus_file, start=1):
            sentence = sentence.strip()
            doc_fingerprint = generate_doc_fingerprint(sentence, phrase_fingerprints)

             # Save document fingerprint to file
            phrases_in_sentence = '__'.join(extract_phrases(sentence))
            phrases_in_sentence = phrases_in_sentence.replace(',', '').replace('.', '')
            phrase_name = f"doc_{line_number}_{phrases_in_sentence.replace(' ', '_')}"
            doc_filename = os.path.join(doc_fingerprints_folder, f"{phrase_name}_fingerprint.txt")
            np.savetxt(doc_filename, doc_fingerprint, delimiter='\t', fmt='%d')
            # if line_number == 2 :
            #     break
    print("Document fingerprints have been generated and saved in the 'doc_fingerprints' folder.")

if __name__ == "__main__":
    main()
