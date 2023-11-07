import csv
from collections import defaultdict

# Read phrases from phrases.txt and store them in a list
with open("phrases.txt", "r", encoding="utf-8") as phrases_file:
    phrases = [line.split(":")[0].strip() for line in phrases_file.readlines()]

# Read contexts from corpus.txt and store them in a list
with open("corpus.txt", "r", encoding="utf-8") as corpus_file:
    contexts = [line.split(",", 1)[0].strip() for line in corpus_file.readlines()]

# Initialize a term-context matrix as a defaultdict of defaultdicts
term_context_matrix = defaultdict(lambda: defaultdict(int))

# Read the processed corpus text
with open("corpus.txt", "r", encoding="utf-8") as corpus_file:
    corpus_lines = corpus_file.readlines()

# Process the corpus and populate the term-context matrix
for idx, line in enumerate(corpus_lines):
    context_id, context_text = line.split(",", 1)
    context_id = context_id.strip()
    context_text = context_text.strip()
    for phrase in phrases:
        term_context_matrix[context_id][phrase] = context_text.count(phrase)

# Write the term-context matrix to a CSV file
with open("term_context_matrix.csv", "w", encoding="utf-8", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write the header row with phrase names
    csv_writer.writerow(["Context ID"] + phrases)
    
    # Write data rows with context IDs and phrase occurrences
    for context_id in contexts:
        row_data = [term_context_matrix[context_id][phrase] for phrase in phrases]
        csv_writer.writerow([context_id] + row_data)

print("Term-context matrix has been successfully created and saved to term_context_matrix.csv.")
