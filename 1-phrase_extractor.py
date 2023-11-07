import spacy
from collections import Counter

# Load the English language model from SpaCy
nlp = spacy.load("en_core_web_sm")

# Read the corpus.txt file and remove line numbers
with open("corpus.txt", "r", encoding="utf-8") as file:
    corpus_text = "\n".join(line.split(",", 1)[1].strip() for line in file.readlines())

# Process the corpus text using SpaCy
doc = nlp(corpus_text)

# Extract noun phrases and verb phrases from the processed text
phrases = []
for chunk in doc.noun_chunks:
    phrases.append(chunk.text)
for chunk in doc:
    if "VP" in chunk.dep_:
        phrases.append(chunk.text)

# Calculate the frequency of each phrase
phrase_counts = Counter(phrases)

# Define a function to filter phrases and remove stop words from single-word phrases
def filter_phrases(phrase_counts):
    filtered_phrases = {}
    for phrase, frequency in phrase_counts.items():
        words = phrase.split()
        if len (phrase) > 1 and len(words) == 1 and not nlp(words[0])[0].is_stop:
            filtered_phrases[phrase] = frequency
        elif len(words) > 1:
            filtered_phrases[phrase] = frequency
    return filtered_phrases

# Filter and sort phrases by frequency in descending order
filtered_phrases = filter_phrases(phrase_counts)
sorted_phrases = sorted(filtered_phrases.items(), key=lambda x: x[1], reverse=True)

# Write the filtered and sorted phrases and their frequencies to phrases.txt
with open("phrases.txt", "w", encoding="utf-8") as output_file:
    for phrase, frequency in sorted_phrases:
        output_file.write(f"{phrase}: {frequency}\n")
