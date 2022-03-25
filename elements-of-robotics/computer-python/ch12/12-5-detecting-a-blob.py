"""
  Blob detection
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA

  A 6 x 10 image is created with a blob in the middle and two artifacts
  Compute the average intensity and a threshold
  Zero out pixels below the threshold
  Find a non-zero pixel and grow the blob with non-zero neighbors
"""

import random

    # Random noise to add to background
def r1():
    return 30+random.randint(0,20)

# Random noise to subtract from the blob
def r2():
    return 80-random.randint(0,20)

# Pixel array of the blob
image = [
    [30 for col in range(10)],
    [30, 30, 30, 30, 80, 80, 30, 30, 30, 30],
    [30, 30, 30, 80, 80, 80, 80, 30, 30, 30],
    [30, 30, 30, 80, 80, 80, 80, 30, 30, 30],
    [80, 30, 30, 30, 80, 80, 30, 30, 30, 80],
    [30 for col in range(10)],
    ]

# Pixel array of the blob with noise
image_with_noise = [
    [r1() for col in range(10)],
    [r1(),r1(),r1(),r1(),r2(),r2(),r1(),r1(),r1(),r1()],
    [r1(),r1(),r1(),r2(),r2(),r2(),r2(),r1(),r1(),r1()],
    [r1(),r1(),r1(),r2(),r2(),r2(),r2(),r1(),r1(),r1()],
    [r2(),r1(),r1(),r1(),r2(),r2(),r1(),r1(),r1(),r2()],
    [r1() for col in range(10)]
    ]

# Lists of explored and not explored pixels and blob pixels
explored = []
not_explored = []
blob = []

# Change intensity over the whole image
def change_intensity(image, diff):
    new_image = [[0 for col in image[0]] for row in image]
    for row in range(len(image)):
        for col in range(len(image[row])):
            new_image[row][col] = image[row][col] + diff
    return new_image

# Print the image
def print_image(title, image):
    print(title)
    for row in range(len(image)):
        for col in range(len(image[0])):
            print("{:4d}".format(image[row][col]),end="")
        print()
    print()

# Zero pixels below threshold
def zero_pixels_below_threshold(image, threshold):
    new_image = [[0 for col in image[0]] for row in image]
    for row in range(len(image)):
        for col in range(len(image[0])):
            if image[row][col] > threshold:
                new_image[row][col] = image[row][col]
    return new_image

# Compute average intensity
def average_intensity(image):
    intensity = 0
    for row in range(len(image)):
        for col in range(len(image[row])):
            intensity += image[row][col]
    return intensity // (len(image)*len(image[0]))

# Find first non-zero pixel and append to not_explored
def find_nonzero_pixel(image):
    for row in range(len(image)):
        for col in range(len(image[row])):
            if image[row][col] != 0:
                print("First non-zero pixel = ", (row,col), end='\n\n')
                not_explored.append((row,col))
                return

# Print the image of the blob
def print_blob(title, image):
    global blob
    print(title)
    for r in range(len(image)):
        for c in range(len(image[r])):
            if (r,c) in blob:
                print("{:4d}".format(image[r][c]),end="")
            else:
                print("{:4d}".format(0),end="")
        print()
    print()

# Add a new pixel to the blob as a neighbor of the tuple pixel
#   with delta row and column in the image
def add_new_pixel(pixel, deltar, deltac, image):
    global explored, not_explored, blob

    # Compute coordinates of neighbor
    r = pixel[0]+deltar
    c = pixel[1]+deltac

    # Return if outside image
    if r == -1 or r == len(image) or c == -1 or c == len(image[r]):
        return

    # If pixel (r,c) is not in the blob, add it
    #   and add it to not explored if not already there or in explored
    if image[r][c] != 0 and (r,c) not in blob:
        blob.append((r,c))
        if (r,c) not in not_explored and (r,c) not in explored:
            not_explored.append((r,c))
    return

# Search the neighbors of pixels in not explored until empty
def get_list_of_blob_pixels(image):
    global explored, not_explored, blob

    # Reset lists
    explored = []
    not_explored = []
    blob = []

    # Find first non-zero pixel
    find_nonzero_pixel(image)

    while not_explored:
        # Get some pixel from not_explored and append to explored
        pixel = not_explored.pop()
        explored.append(pixel)

        # Check each of the eight neigbors
        add_new_pixel(pixel, -1, -1, image)
        add_new_pixel(pixel, -1,  0, image)
        add_new_pixel(pixel, -1,  1, image)
        add_new_pixel(pixel,  0, -1, image)
        add_new_pixel(pixel,  0,  1, image)
        add_new_pixel(pixel,  1, -1, image)
        add_new_pixel(pixel,  1,  0, image)
        add_new_pixel(pixel,  1,  1, image)

        # Print lists for debugging
##        print("Explored", explored)
##        print("Not explored", not_explored)
##        print("Blob", blob, end='\n\n')

# Find and print the blob
def find_blob(image):
    # Threshold is average intensity + bias
    threshold = average_intensity(image) + 5
    print("Threshold =", threshold, end='\n\n')

    # Get new image after zeroing pixels below the threshold
    image1 = zero_pixels_below_threshold(image, threshold)
    print_image("Image above threshold", image1)

    # Get the list of blob pixels and print the blob
    get_list_of_blob_pixels(image1)
    print_blob("Image of the blob", image1)

# Print the image with and without the noise
print_image("Image with blob", image)
print_image("Image with blob and noise", image_with_noise)

# Find and print the blob
find_blob(image_with_noise)

print("-------------------------")
print()

# Change intensity and rerun
find_blob(change_intensity(image_with_noise, -20))
