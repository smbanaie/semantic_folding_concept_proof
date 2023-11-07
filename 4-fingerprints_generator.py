import csv
import os

NUM_DIMENSIONS = 8  # Number of dimensions (can be changed)

# Load context coordinates from context_coordinates.csv
context_coordinates = {}
with open("context_coordinates.csv", "r", encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)
    for row in reader:
        context_id, coordinates = row
        context_coordinates[context_id] = tuple(map(int, coordinates.split(',')))

# Load phrases from phrases.txt and map them to their indices in term_context_matrix header
phrase_indices = {}
phrases = []
with open("phrases.txt", "r", encoding="utf-8") as file:
    for idx, line in enumerate(file):
        phrase = line.strip()
        phrases.append(phrase)
        phrase_indices[phrase] = idx + 1  # Adding 1 because the first column in term_context_matrix is context_id

# Initialize fingerprints directory
if not os.path.exists("fingerprints"):
    os.makedirs("fingerprints")

# Load term-context matrix from term_context_matrix.csv
term_context_matrix = {}
with open("term_context_matrix.csv", "r", encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)
    for row in reader:
        context_id = row[0]
        context_data = list(map(int, row[1:]))
        term_context_matrix[context_id] = context_data

# Generate and save fingerprints for each phrase
for phrase in phrases:
    print("*-"*30)
    print(phrase)
    fingerprint_matrix = [[0 for _ in range(NUM_DIMENSIONS)] for _ in range(NUM_DIMENSIONS)]
    phrase_index = phrase_indices[phrase]
    print(f"Phrase Index:{phrase_index}")
    for context_id, context_data in term_context_matrix.items():
        if phrase_index < len(phrases):
            for i, item in enumerate(context_data[:]):
                if item> 0 :
                    print(phrases[i])
            if context_data[phrase_index] == 1:
                print(f"===========  Phrase Matched, Context ID : {context_id} ==========")
                row, col = context_coordinates[context_id]
                print(f"||>>>> Semantic Coordinates: {row}, {col}")
                fingerprint_matrix[(row+NUM_DIMENSIONS)//2][(col+NUM_DIMENSIONS)//2] += 1
    

    print(fingerprint_matrix)
    # Save fingerprint matrix to a file
    fingerprint_filename = os.path.join("fingerprints", f"{phrase.split(':')[0].replace(' ', '_')}_fingerprint.txt")
    print(f"File Name : {fingerprint_filename}")
    # input()
    with open(fingerprint_filename, "w", encoding="utf-8") as fingerprint_file:
        for row in fingerprint_matrix:
            fingerprint_file.write("\t".join(map(str, row)) + "\n")

print("Fingerprints have been successfully generated and saved in the 'fingerprints' folder.")
