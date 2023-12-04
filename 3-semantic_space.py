import networkx as nx
import matplotlib.pyplot as plt
import csv
import seaborn as sns
import numpy as np


NUM_DIMENSIONS = 8  # Number of dimensions (can be changed)
NUM_CONTEXT = 20

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
            # weight = sum((1 if c1 > 0 else 0 ) * (1 if c2 > 0 else 0 ) for c1, c2 in zip(context_data, neighbor_data))
            weight_normalized = weight / 20
            if weight_normalized > 0.1:
                G.add_edge(context_id, neighbor_id, weight=weight)

# Use force-directed layout to position the nodes based on edge weights
pos = nx.spring_layout(G, seed=200, center=(0.0, 0.0), k=NUM_DIMENSIONS / 2, weight='weight')

# Calculate figsize based on the number of dimensions
figsize = (10, 6)

# Extract edge weights to set edge widths
edge_weights = [data['weight'] for _, _, data in G.edges(data=True)]

plt.figure(figsize=figsize)
nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1500, font_size=10, font_weight="bold",
        width=edge_weights, edge_cmap=plt.cm.YlGnBu, edge_color=edge_weights, font_color="black", alpha=0.9)


# edge_cmap=plt.cm.PuRd
# edge_cmap=plt.cm.RdYlBu
# edge_cmap=plt.cm.magma

# Add edge labels (weights)
# edge_labels = {(edge[0], edge[1]): f'{edge[2]["weight"]:.2f}' for edge in G.edges(data=True)}
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.title("Semantic Matrix Mapping")
# Save the plot
plt.savefig(f"./images/graph.png")
 
plt.show()



context_context_matrix = np.zeros((NUM_CONTEXT, NUM_CONTEXT), dtype=int)
for context_id, context_data in term_context_matrix.items():
    for neighbor_id, neighbor_data in term_context_matrix.items():
        if context_id != neighbor_id:
            weight = sum(c1 * c2 for c1, c2 in zip(context_data, neighbor_data))
            weight_normalized = weight / 20
            if weight_normalized > 0.1:
                context_context_matrix[int(context_id) - 1, int(neighbor_id) - 1] = int(weight)

# Adjusting the matrix for display
adjusted_matrix = np.flipud(context_context_matrix)

# Create the heatmap
plt.figure(figsize=(10, 8))  # You can adjust the figure size as per your preference
sns.heatmap(adjusted_matrix, annot=True, fmt="d", cmap="YlGnBu",
            xticklabels=list(range(1, NUM_CONTEXT + 1)), yticklabels=list(range(NUM_CONTEXT, 0, -1)))  

# Adding title and labels if needed
plt.title('Context-Context Matrix Heatmap')
plt.xlabel('Context ID')
plt.ylabel('Neighbor ID')

# # Save the plot
plt.savefig(f"./images/context_context_heatmap.png")
# Show the plot
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

# Extract row and column coordinates from context_coordinates
rows = []
cols = []
for coordinates in context_coordinates.values():
    row, col = map(int, coordinates.split(','))
    rows.append(row)
    cols.append(col)

# Create a NumPy array for the matrix
matrix_data = np.zeros((NUM_DIMENSIONS, NUM_DIMENSIONS), dtype=int)
# Adjusting the matrix for display
adjusted_matrix_data = np.flipud(matrix_data)


for row, col in zip(rows, cols):
    matrix_data[row, col] += 1
plt.figure(figsize=(8, 6))
# Create a heatmap using seaborn
sns.heatmap(adjusted_matrix_data, annot=True, fmt="d", cmap="YlGnBu", cbar=True,
            xticklabels=list(range(1, NUM_DIMENSIONS + 1)), yticklabels=list(range(NUM_DIMENSIONS, 0, -1)))
# plt.scatter(cols, rows, marker='s', color='red', label='Contexts')  # Add red squares for context positions
plt.title("Semantic Matrix Mapping - Heatmap")
plt.xlabel("Column")
plt.ylabel("Row")
plt.legend()
plt.savefig(f"./images/semantic_space_heatmap.png")
plt.show()


import plotly.graph_objs as go

context_text_mapping = {}

with open("corpus.txt", "r", encoding="utf-8") as file:
    for line in file:
        # Assuming each line is in the format: "line_number,context_text"
        line_number, context_text = line.strip().split(',', 1)
        context_text_mapping[line_number] = line # context_text

# Create an empty array for the line numbers
line_numbers = [["" for _ in range(NUM_DIMENSIONS)] for _ in range(NUM_DIMENSIONS)]
# Create an empty array for the heatmap
context_texts = [["" for _ in range(NUM_DIMENSIONS)] for _ in range(NUM_DIMENSIONS)]

# Populate the array with line numbers and context texts
for context_id, coordinates in context_coordinates.items():
    row, col = map(int, coordinates.split(','))
    current_lines = line_numbers[row][col]
    new_line = context_id  # Using context_id as the line number

    # Concatenate if there's already a line number in this cell
    if current_lines:
        line_numbers[row][col] = current_lines + ", " + new_line
    else:
        line_numbers[row][col] = new_line

    # Assign context text to the corresponding cell
    current_text = context_texts[row][col]
    new_text = context_text_mapping.get(context_id, "")

    # Concatenate if there's already text in this cell
    if current_text:
        context_texts[row][col] = current_text + " || " + new_text
    else:
        context_texts[row][col] = new_text

# Adjust the matrices for display
adjusted_line_numbers = np.flipud(line_numbers)

adjusted_context_texts = np.flipud(context_texts)

# Create a figure for line numbers using Seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(np.zeros_like(adjusted_matrix_data), annot=adjusted_line_numbers, fmt="", cmap="YlGnBu", cbar=False,
            xticklabels=list(range(1, NUM_DIMENSIONS + 1)), yticklabels=list(range(1, NUM_DIMENSIONS + 1)))
plt.title("Semantic Matrix Mapping - Line Numbers")
plt.xlabel("Column")
plt.ylabel("Row")
plt.savefig(f"./images/semantic_space_heatmap_context_id.png")

plt.show()



trace = go.Heatmap(
    z=adjusted_matrix_data, 
    x=list(range(1, NUM_DIMENSIONS + 1)),
    y=list(range(NUM_DIMENSIONS, 0, -1)),
    text=adjusted_line_numbers,  # Display line numbers in each cell
    hovertext=adjusted_context_texts,  # Show context information on hover
    hoverinfo="text",
    colorscale="YlGnBu" 
)

# Layout configuration
layout = go.Layout(
    title="Semantic Matrix Mapping - Heatmap",
    xaxis=dict(title="Column"),
    yaxis=dict(title="Row"),
    hovermode='closest'
)

print(adjusted_line_numbers)
# Create figure
fig = go.Figure(data=[trace], layout=layout)

# Show the figure
fig.show()