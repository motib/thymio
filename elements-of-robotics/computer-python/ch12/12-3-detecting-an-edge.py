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
    [30 for col in range(6)],
    [30 for col in range(6)],
    [30 for col in range(6)],
    [50 for col in range(6)],
    [50 for col in range(6)],
    [50 for col in range(6)]
    ]

diagonal_image = [
    [30, 30, 30, 30, 30, 30],
    [50, 30, 30, 30, 30, 30],
    [50, 50, 30, 30, 30, 30],
    [50, 50, 50, 30, 30, 30],
    [50, 50, 50, 50, 30, 30],
    [50, 50, 50, 50, 50, 30],
    ]

# Print the image
def print_image(title, image):
    print(title)
    for row in range(len(image)):
        for col in range(len(image[0])):
            print("{:4d}".format(image[row][col]),end="")
        print()
    print()

# Apply the vertical Sobel filter
def sobel_vertical(image):
    new_image = [[0 for col in image[0]] for row in image]
    for row in range(1,len(image)-1):
        for col in range(1,len(image[0])-1):
            new_image[row][col] = \
                -image[row-1][col-1]-2*image[row-1][col]-image[row-1][col+1]+ \
                 image[row+1][col-1]+2*image[row+1][col]+image[row+1][col+1]
    return new_image

# Apply the horizontal Sobel filter
def sobel_horizontal(image):
    new_image = [[0 for col in image[0]] for row in image]
    for row in range(1,len(image)-1):
        for col in range(1,len(image[0])-1):
            new_image[row][col] = \
                -image[row-1][col-1]+image[row-1][col+1]+ \
                -2*image[row][col-1]+2*image[row][col+1]+ \
                -image[row+1][col-1]+image[row+1][col+1]
    return new_image

print_image("Original image", image)

# Edge detection of horizontal edge
print_image("Sobel vertical edge detector", sobel_vertical(image))

print_image("Sobel horizontal edge detector", sobel_horizontal(image))

# Edge detection of diagonal edge
print_image("Sobel vertical edge detector (diagonal)", sobel_vertical(diagonal_image))

print_image("Sobel horizontal edge detector (diagonal)", sobel_horizontal(diagonal_image))
