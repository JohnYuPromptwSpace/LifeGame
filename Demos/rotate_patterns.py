def rotate_indices_counter_clockwise(indices, size):
    rotated_indices = []
    for i, j in indices:
        rotated_indices.append([size - 1 - j, i])
    return rotated_indices

# Given indices and size of the matrix
indices = [[2, 0], [1, 1], [0, 2], [1, 3]]
size = 4

# Get the rotated indices
rotated_indices = rotate_indices_counter_clockwise(indices, size)

# Print the rotated indices
print("Original indices:")
print(indices)

print("\nRotated indices:")
print(rotated_indices)