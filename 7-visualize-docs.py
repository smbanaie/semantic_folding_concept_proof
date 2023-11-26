import os
import numpy as np
import matplotlib.pyplot as plt
import spacy
import textwrap



# Function to load document fingerprint matrix from file
def load_doc_fingerprint(doc_filename):
    if not os.path.exists(doc_filename):
        print(f"Document fingerprint file '{doc_filename}' not found.")
        return None
    return np.loadtxt(doc_filename, delimiter='\t', dtype=int)

# Function to visualize a single document fingerprint using a heatmap
def visualize_single_doc_fingerprint(doc_fingerprint, title="Document Fingerprint", comment:str= None, save_path=None):
    fig = plt.figure(figsize=(10, 6))  # Adjust the size as needed
    plt.imshow(doc_fingerprint, cmap='Blues', aspect='auto')
    plt.title(title)
    # plt.xlabel("Phrases")
    # plt.ylabel("Dimensions")
    plt.colorbar(label="Frequency")

    # Add a comment below the plot
    if comment:
         # Wrap the comment text
        wrapped_comment = textwrap.fill(comment, width=80)  # Adjust the width as needed
        plt.text(0.5, -0.10, wrapped_comment, transform=plt.gca().transAxes, fontsize=10, va='center', ha='center')
        # plt.figtext(0.5, 0.02, comment, ha='center', va='center', fontsize=10)


    if save_path:
        plt.savefig(save_path)
    plt.show()

# Function to visualize two document fingerprints side by side using heatmaps
def visualize_two_doc_fingerprints(doc_fingerprint_1, doc_fingerprint_2, title1="Document 1 Fingerprint", title2="Document 2 Fingerprint", comment_1=None, comment_2=None, save_path=None):
    
    plt.figure(figsize=(14, 7))

    # Plot the first document fingerprint
    plt.subplot(1, 2, 1)
    plt.imshow(doc_fingerprint_1, cmap='Blues', aspect='auto')
    plt.title(title1)
    # plt.xlabel("Phrases")
    # plt.ylabel("Dimensions")
    plt.colorbar(label="Frequency")

    if comment_1:
         # Wrap the comment text
        wrapped_comment = textwrap.fill(comment_1, width=80)  # Adjust the width as needed
        plt.text(0.5, -0.10, wrapped_comment, transform=plt.gca().transAxes, fontsize=10, va='center', ha='center')
        # plt.figtext(0.5, 0.02, comment, ha='center', va='center', fontsize=10)



    # Plot the second document fingerprint
    plt.subplot(1, 2, 2)
    plt.imshow(doc_fingerprint_2, cmap='Blues', aspect='auto')
    plt.title(title2)
    # plt.xlabel("Phrases")
    # plt.ylabel("Dimensions")
    plt.colorbar(label="Frequency")

    if comment_2:
         # Wrap the comment text
        wrapped_comment = textwrap.fill(comment_2, width=80)  # Adjust the width as needed
        plt.text(0.5, -0.10, wrapped_comment, transform=plt.gca().transAxes, fontsize=10, va='center', ha='center')
        # plt.figtext(0.5, 0.02, comment, ha='center', va='center', fontsize=10)


    if save_path:
        plt.savefig(save_path)
    plt.show()

# Load the English language model from SpaCy
nlp = spacy.load("en_core_web_sm")

# Function to extract phrases from a sentence using SpaCy
def extract_phrases(sentence):
    doc = nlp(sentence)
    phrases = [chunk.text for chunk in doc.noun_chunks]
    return phrases

# Main function
def main():
    # Input: indices of documents in corpus (adjust as needed)
    doc_indices = [1,2]

    # Load document fingerprints
    doc_fingerprints_folder = "doc_fingerprints"
    corpus_file = "corpus.txt" 
    images_folder = "images"

    # Create the images folder if it doesn't exist
    os.makedirs(images_folder, exist_ok=True)

    # Read the content of the file into an array
    with open(corpus_file, 'r') as file:
        lines = file.readlines()

    if len(doc_indices) == 1:
        doc_index = doc_indices[0]
        print("Current Sentence:")
        print(f"Index: {doc_index}, Sentence: {lines[doc_index-1]}")
        phrases_in_sentence = '__'.join(extract_phrases(lines[doc_index-1]))
        phrases_in_sentence = phrases_in_sentence.replace(',', '').replace('.', '')
        doc_filename = f"doc_{doc_index}_{phrases_in_sentence.replace(' ', '_')}"
        print(f"Doc Filename: {doc_filename}")
        final_doc_filename = os.path.join(doc_fingerprints_folder, f"{doc_filename}_fingerprint.txt")
        print(f"Final Doc Filename: {final_doc_filename}")

        doc_fingerprint = load_doc_fingerprint(final_doc_filename)
        if doc_fingerprint is not None:
            save_path = os.path.join(images_folder, f"doc_fingerprints_{doc_index}.png")
            visualize_single_doc_fingerprint(doc_fingerprint, title=f"Document {doc_index} Fingerprint", comment=lines[doc_index-1].split(',')[1], save_path=save_path)

    elif len(doc_indices) == 2:
        # Handle two documents in one chart
        doc_index_1, doc_index_2 = doc_indices
        print("Current Sentences:")
        print(f"Index: {doc_index_1}, Sentence: {lines[doc_index_1-1]}")
        print(f"Index: {doc_index_2}, Sentence: {lines[doc_index_2-1]}")

        phrases_in_sentence_1 = '__'.join(extract_phrases(lines[doc_index_1-1]))
        phrases_in_sentence_1 = phrases_in_sentence_1.replace(',', '').replace('.', '')
        doc_filename_1 = f"doc_{doc_index_1}_{phrases_in_sentence_1.replace(' ', '_')}"
        final_doc_filename_1 = os.path.join(doc_fingerprints_folder, f"{doc_filename_1}_fingerprint.txt")

        phrases_in_sentence_2 = '__'.join(extract_phrases(lines[doc_index_2-1]))
        phrases_in_sentence_2 = phrases_in_sentence_2.replace(',', '').replace('.', '')
        doc_filename_2 = f"doc_{doc_index_2}_{phrases_in_sentence_2.replace(' ', '_')}"
        final_doc_filename_2 = os.path.join(doc_fingerprints_folder, f"{doc_filename_2}_fingerprint.txt")

        doc_fingerprint_1 = load_doc_fingerprint(final_doc_filename_1)
        doc_fingerprint_2 = load_doc_fingerprint(final_doc_filename_2)

        if doc_fingerprint_1 is not None and doc_fingerprint_2 is not None:
            save_path = os.path.join(images_folder, f"doc_fingerprints_{doc_index_1}_{doc_index_2}.png")
            visualize_two_doc_fingerprints(doc_fingerprint_1, doc_fingerprint_2, title1=f"Document {doc_index_1} Fingerprint", title2=f"Document {doc_index_2} Fingerprint", comment_1= lines[doc_index_1-1].split(',')[1], comment_2= lines[doc_index_2-1].split(',')[1] , save_path=save_path)

    else:
        print("Error: Visualization supports only one or two documents.")

if __name__ == "__main__":
    main()
