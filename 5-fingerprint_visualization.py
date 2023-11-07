import os
import numpy as np
import matplotlib.pyplot as plt

# Function to load fingerprint matrix from file
def load_fingerprint_matrix(phrase):
    fingerprint_filename = os.path.join("fingerprints", f"{phrase.replace(' ', '_')}_fingerprint.txt")
    if not os.path.exists(fingerprint_filename):
        print(f"Fingerprint file for '{phrase}' not found.")
        return None
    with open(fingerprint_filename, "r", encoding="utf-8") as file:
        fingerprint_matrix = [[int(value) for value in line.strip().split("\t")] for line in file]
    return fingerprint_matrix

# Function to plot fingerprint matrix as heatmap
def plot_fingerprint_heatmap(phrase, fingerprint_matrix):
    plt.figure(figsize=(8, 8))
    plt.imshow(fingerprint_matrix, cmap="Blues", interpolation="nearest", aspect="auto")
    plt.colorbar()
    plt.title(f"{phrase} Fingerprint Heatmap")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    plt.xticks(np.arange(len(fingerprint_matrix[0])), np.arange(1, len(fingerprint_matrix[0]) + 1))
    plt.yticks(np.arange(len(fingerprint_matrix)), np.arange(1, len(fingerprint_matrix) + 1))
    plt.gca().invert_yaxis()  # Invert y-axis to match the matrix representation
    plt.grid(color='w', linestyle='-', linewidth=0.5)  # Add grid lines
    plt.gca().set_facecolor('white')  # Set background color to white
    plt.savefig(f"{phrase.replace(' ', '_')}_fingerprint_heatmap.png")
    plt.show()

# Main function
def main():
    phrases = input("Enter one or two phrases (comma separated): ").split(",")
    phrases = [phrase.strip() for phrase in phrases]

    if len(phrases) == 1:
        phrase1 = phrases[0]
        fingerprint_matrix1 = load_fingerprint_matrix(phrase1)
        if fingerprint_matrix1:
            plot_fingerprint_heatmap(phrase1, fingerprint_matrix1)
    elif len(phrases) == 2:
        phrase1, phrase2 = phrases
        fingerprint_matrix1 = load_fingerprint_matrix(phrase1)
        fingerprint_matrix2 = load_fingerprint_matrix(phrase2)
        if fingerprint_matrix1 and fingerprint_matrix2:
            plt.figure(figsize=(16, 8))
            plt.subplot(1, 2, 1)
            plt.imshow(fingerprint_matrix1, cmap="Blues", interpolation="nearest", aspect="auto")
            plt.colorbar()
            plt.title(f"{phrase1} Fingerprint Heatmap")
            plt.xlabel("Columns")
            plt.ylabel("Rows")
            plt.xticks(np.arange(len(fingerprint_matrix1[0])), np.arange(1, len(fingerprint_matrix1[0]) + 1))
            plt.yticks(np.arange(len(fingerprint_matrix1)), np.arange(1, len(fingerprint_matrix1) + 1))
            plt.gca().invert_yaxis()
            plt.grid(color='w', linestyle='-', linewidth=0.5)
            plt.gca().set_facecolor('white')

            plt.subplot(1, 2, 2)
            plt.imshow(fingerprint_matrix2, cmap="Blues", interpolation="nearest", aspect="auto")
            plt.colorbar()
            plt.title(f"{phrase2} Fingerprint Heatmap")
            plt.xlabel("Columns")
            plt.ylabel("Rows")
            plt.xticks(np.arange(len(fingerprint_matrix2[0])), np.arange(1, len(fingerprint_matrix2[0]) + 1))
            plt.yticks(np.arange(len(fingerprint_matrix2)), np.arange(1, len(fingerprint_matrix2) + 1))
            plt.gca().invert_yaxis()
            plt.grid(color='w', linestyle='-', linewidth=0.5)
            plt.gca().set_facecolor('white')

            plt.savefig(f"{phrase1.replace(' ', '_')}_{phrase2.replace(' ', '_')}_fingerprint_heatmap.png")
            plt.show()
    else:
        print("Invalid number of phrases. Please enter one or two phrases.")

if __name__ == "__main__":
    main()
