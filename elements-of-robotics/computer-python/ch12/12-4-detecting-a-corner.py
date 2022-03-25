"""
  Edge detection
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA

  A 6 x 6 image is created with an edge halfway from the top
  Vertical and horizontal Sobel filters are used to detect the
    horizontal but not a vertical edge
  A diagonal image shows that both filters give a non-zero output
"""

image = [
    [30 for col in range(10)],
    [30 for col in range(10)],
    [30, 30, 30, 60, 60, 60, 60, 30, 30, 30],
    [30, 30, 30, 60, 60, 60, 60, 30, 30, 30],
    [30, 30, 30, 60, 60, 60, 60, 30, 30, 30],
    [30, 30, 30, 60, 60, 60, 60, 30, 30, 30],
    ]

# Print the image
def print_image(title, image):
    print(title)
    for row in range(len(image)):
        for col in range(len(image[0])):
            print("{:4d}".format(image[row][col]),end="")
        print()
    print()

# Print corners
def print_corners(corners):
    print("Corners")
    for c in corners:
        print(c)

# Compute vertical diffs
def vertical_diffs(image):
    diffs = [[0 for col in image[0]] for row in image]
    for row in range(1,len(image)-1):
        for col in range(1,len(image[0])-1):
            diffs[row][col] = abs(image[row+1][col] - image[row-1][col])
    return diffs

# Compute horizontal diffs
def horizontal_diffs(image):
    diffs = [[0 for col in image[0]] for row in image]
    for row in range(1,len(image)-1):
        for col in range(1,len(image[0])-1):
            diffs[row][col] = abs(image[row][col+1] - image[row][col-1])
    return diffs

# Find corners
def find_corners(h_diffs, v_diffs, threshold):
    corners = []
    for row in range(1,len(image)-1):
        for col in range(1,len(image[0])-1):
            if h_diffs[row][col] > threshold and \
               v_diffs[row][col] > threshold:
                corners.append([row,col])
    return corners

print_image("Image with corner", image)

h_diffs = horizontal_diffs(image)
v_diffs = vertical_diffs(image)
print_image("Horizontal diffs", h_diffs)
print_image("Vertical diffs",   v_diffs)

print_corners(find_corners(h_diffs, v_diffs, 10))
print()

# Compute similar neighbors
def similar_neighbors(image, threshold):
    counts = [[0 for col in image[0]] for row in image]
    for row in range(1,len(image)-1):
        for col in range(1,len(image[0])-1):
            n = 0
            if abs(image[row][col] - image[row+1][col-1]) < threshold: n += 1
            if abs(image[row][col] - image[row+1][col])   < threshold: n += 1
            if abs(image[row][col] - image[row+1][col+1]) < threshold: n += 1
            if abs(image[row][col] - image[row]  [col-1]) < threshold: n += 1
            if abs(image[row][col] - image[row]  [col+1]) < threshold: n += 1
            if abs(image[row][col] - image[row-1][col-1]) < threshold: n += 1
            if abs(image[row][col] - image[row-1][col])   < threshold: n += 1
            if abs(image[row][col] - image[row-1][col+1]) < threshold: n += 1
            counts[row][col] = n
    return counts

# Corners have a minimum number of similar neighbors
def minimum_similar(counts):
    minimum = 9
    for row in range(1,len(image)-1):
        for col in range(1,len(image[0])-1):
            if counts[row][col] < minimum: minimum = counts[row][col]
    corners = []
    for row in range(1,len(image)-1):
        for col in range(1,len(image[0])-1):
            if counts[row][col] == minimum:
                corners.append([row,col])
    return corners

counts = similar_neighbors(image, 10)
print_image("Similar neighbors", counts)

print_corners(minimum_similar(counts))

