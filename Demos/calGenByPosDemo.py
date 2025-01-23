import time
import os

def get_neighbors(pos):
    """Return the 8 neighbors of the given position (row, col)."""
    row, col = pos
    neighbors = [(row + dr, col + dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if not (dr == 0 and dc == 0)]
    return neighbors

def next_generation(live_cells):
    """Compute the next generation of live cells."""
    from collections import defaultdict

    # Dictionary to count live neighbors for each cell
    neighbor_count = defaultdict(int)

    # Count neighbors for each live cell and its neighbors
    for cell in live_cells:
        for neighbor in get_neighbors(cell):
            neighbor_count[neighbor] += 1

    new_live_cells = set()

    for cell, count in neighbor_count.items():
        if count == 3 or (count == 2 and cell in live_cells):
            new_live_cells.add(cell)

    return new_live_cells

# Example usage:
live_cells = {(1, 2), (1, 3), (2, 4), (4, 3), (4, 2), (3, 1)}
generations = 20

for y in range(10):
    for x in range(10):
        if (x,y) in live_cells:
            print(1, end = "")
        else:
            print("_", end="")
    print()

for _ in range(generations):
    os.system("cls")
    live_cells = next_generation(live_cells)

    print()
    for y in range(10):
        for x in range(10):
            if (x,y) in live_cells:
                print(1, end = "")
            else:
                print("_", end="")
        print()
    time.sleep(0.3)