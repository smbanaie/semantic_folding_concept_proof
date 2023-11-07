import networkx as nx
import matplotlib.pyplot as plt
import csv

NUM_DIMENSIONS = 8  # Number of dimensions (can be changed)

# Read the term-context matrix from the CSV file
term_context_matrix = {}
with open("term_context_matrix.csv", "r", encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)
    for row in reader:
        context_id = row[0]
        context_data = list(map(int, row[1:]))
        term_context_matrix[context_id] = context_data

# Create a graph for the contexts based on phrase overlap
G = nx.Graph()
for context_id, context_data in term_context_matrix.items():
    G.add_node(context_id)
    for neighbor_id, neighbor_data in term_context_matrix.items():
        if context_id != neighbor_id:
            weight = sum(c1 * c2 for c1, c2 in zip(context_data, neighbor_data))
            G.add_edge(context_id, neighbor_id, weight=weight)

# Use force-directed layout to position the nodes based on edge weights
pos = nx.spring_layout(G, seed=200, center=(0.0, 0.0), k=NUM_DIMENSIONS/2)

# Draw the graph to visualize the mapping

# Calculate figsize based on the number of dimensions
figsize = (NUM_DIMENSIONS, NUM_DIMENSIONS)

plt.figure(figsize=figsize)
nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1500, font_size=10, font_weight="bold")
plt.title("Semantic Matrix Mapping")
plt.show()

# Generate a dictionary to store context IDs and their corresponding cell coordinates
context_coordinates = {}
for context_id, position in pos.items():
    row, col = int(position[1] * NUM_DIMENSIONS / 2), int(position[0] * NUM_DIMENSIONS / 2)
    context_coordinates[context_id] = f"{row},{col}"

# Write context IDs and their cell coordinates to a CSV file
with open("context_coordinates.csv", "w", encoding="utf-8", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Context ID", "Cell Coordinates"])
    for context_id, coordinates in context_coordinates.items():
        csv_writer.writerow([context_id, coordinates])

print("Context coordinates have been successfully saved to context_coordinates.csv.")
