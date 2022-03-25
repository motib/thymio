"""
  Spatial filter for smoothing an image
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA

  A 6 x 10 image is created and then noise is added
  The box filter and then a weighted filter are applied
"""

#  Image with uniform column intensities and increasing row intensities
image = [[row*10 for col in range(10)] for row in range(1,7)]

# Print the image
def print_image(title, image):
    print(title)
    for row in image:
        print(row)
    print()

# Apply box filter
def box_filter(image):
    new_image = [row[:] for row in image] # Make copy
    for row in range(1,5):
        for col in range(1,9):
            new_image[row][col] = \
                (image[row-1][col-1]+image[row-1][col]+image[row-1][col+1]+ \
                 image[row]  [col-1]+image[row]  [col]+image[row]  [col+1]+ \
                 image[row+1][col-1]+image[row+1][col]+image[row+1][col+1]) \
                 // 9
    return new_image

# Apply weighted filter
def weighted_filter(image):
    new_image = [row[:] for row in image] # Make copy
    for row in range(1,5):
        for col in range(1,9):
            new_image[row][col] = \
                (image[row-1][col-1]+  image[row-1][col]+image[row-1][col+1]+ \
                 image[row]  [col-1]+8*image[row]  [col]+image[row]  [col+1]+ \
                 image[row+1][col-1]+  image[row+1][col]+image[row+1][col+1]) \
                 // 16
    return new_image

print_image("Original image", image)

# Add noise to image
image[2][3] = 20
image[3][6] = 10
image[4][4] = 90

print_image("Image with noise", image)

print_image("Smoothed with box filter", box_filter(image))

print_image("Smoothed with weighted filter", weighted_filter(image))
