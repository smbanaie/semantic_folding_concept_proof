import random
from collections import Counter


# Define the list of words
words = [chr(ord('a') + i) * 3 for i in range(26)]  # ['aaa', 'bbb', 'ccc', ..., 'zzz']

# Number of lines and words per line
num_lines = 20
words_per_line = 10

# Generate the sample corpus
sample_corpus = []
phrases = []
for line_number in range(1, num_lines + 1):
    sentence = ' '.join(random.choice(words) for _ in range(words_per_line))
    phrases.extend(sentence.split(" "))
    line = f"{line_number}, {sentence}"
    sample_corpus.append(line)

# Set the filename variable
filename = "corpus.txt"

# Write the sample corpus to the file
with open(filename, 'w') as file:
    for line in sample_corpus:
        file.write(line + '\n')

print(f"Sample corpus written to {filename}")

# Count the occurrences of each phrase
phrase_counts = Counter(phrases)

# Sort phrases by count in descending order
sorted_phrases = sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True)

# Write phrases and their counts to phrases.txt
phrases_filename = "phrases.txt"
with open(phrases_filename, 'w') as phrases_file:
    for phrase, count in sorted_phrases:
        phrases_file.write(f"{phrase.strip()}: {count}\n")

print(f"Phrases and their counts written to {phrases_filename}")