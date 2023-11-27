import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load fingerprint matrix from file
def load_fingerprint_matrix(phrase):
    fingerprint_filename = os.path.join("fingerprints", f"{phrase.replace(' ', '_')}_fingerprint.txt")
    if not os.path.exists(fingerprint_filename):
        print(f"Fingerprint file for '{phrase}' not found.")
        return None
    with open(fingerprint_filename, "r", encoding="utf-8") as file:
        fingerprint_matrix = [[int(value) for value in line.strip().split("\t")] for line in file]
    return fingerprint_matrix

# Function to plot fingerprint matrix as heatmap using Seaborn for a single phrase
def plot_single_phrase_heatmap(phrase, fingerprint_matrix):
    plt.figure(figsize=(8, 8))
    sns.heatmap(fingerprint_matrix, annot=True, fmt="d", cmap="Blues", cbar=False, xticklabels=True, yticklabels=True)
    plt.title(f"{phrase} Fingerprint Heatmap")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    
    # Save the plot
    plt.savefig(f"./images/phrase_fingerprint_heatmap_{phrase.replace(' ', '_')}.png")
  
    plt.show()

# Function to plot fingerprint matrices as side-by-side heatmaps using Seaborn for two phrases
def plot_two_phrases_heatmaps(phrase1, fingerprint_matrix1, phrase2, fingerprint_matrix2):
    plt.figure(figsize=(16, 8))
    
    plt.subplot(1, 2, 1)
    sns.heatmap(fingerprint_matrix1, annot=True, fmt="d", cmap="Blues", cbar=False, xticklabels=True, yticklabels=True)
    plt.title(f"{phrase1} Fingerprint Heatmap")
    plt.xlabel("Columns")
    plt.ylabel("Rows")

    plt.subplot(1, 2, 2)
    sns.heatmap(fingerprint_matrix2, annot=True, fmt="d", cmap="Blues", cbar=False, xticklabels=True, yticklabels=True)
    plt.title(f"{phrase2} Fingerprint Heatmap")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    
    # Save the plot
    plt.savefig(f"./images/phrase_fingerprint_heatmap_{phrase1.replace(' ', '_')}_{phrase2.replace(' ', '_')}.png")

    plt.show()

# Main function
def main():
    phrases = input("Enter one or two phrases (comma separated): ").split(",")
    phrases = [phrase.strip() for phrase in phrases]

    if len(phrases) == 1:
        phrase1 = phrases[0]
        fingerprint_matrix1 = load_fingerprint_matrix(phrase1)
        if fingerprint_matrix1:
            plot_single_phrase_heatmap(phrase1, fingerprint_matrix1)
        else:
            print(f"Fingerprint matrix not found for '{phrase1}'.")
    elif len(phrases) == 2:
        phrase1, phrase2 = phrases
        fingerprint_matrix1 = load_fingerprint_matrix(phrase1)
        fingerprint_matrix2 = load_fingerprint_matrix(phrase2)
        if fingerprint_matrix1 and fingerprint_matrix2:
            plot_two_phrases_heatmaps(phrase1, fingerprint_matrix1, phrase2, fingerprint_matrix2)
        else:
            print(f"Fingerprint matrix not found for one or both phrases.")
    else:
        print("Invalid number of phrases. Please enter one or two phrases.")

if __name__ == "__main__":
    main()
