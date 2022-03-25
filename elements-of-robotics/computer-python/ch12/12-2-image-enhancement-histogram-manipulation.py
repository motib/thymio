"""
  Histogram manipulation
  Copyright 2017 Moti Ben-Ari
  CreativeCommons BY-SA

  A 6 x 10 image is created and then random noise is added
  The histogram is computed
  A threshold is computed so that a given fraction of the pixels
    are in the background
  A binary image is created using the threshold
"""
import random

# Random noise to add to background
def r1():
    return 10+random.randint(0,40)

# Random noise to subtract from background
def r2():
    return 90-random.randint(0,40)

# Original image with light rectangle on dark background
image = [
    [10 for col in range(10)],
    [10 for col in range(10)],
    [10,10,10,90,90,90,90,90,10,10],
    [10,10,10,90,90,90,90,90,10,10],
    [10,10,10,90,90,90,90,90,10,10],
    [10 for col in range(10)]
    ]

image_with_noise = [
    [r1() for col in range(10)],
    [r1() for col in range(10)],
    [r1(),r1(),r1(),r2(),r2(),r2(),r2(),r2(),r1(),r1()],
    [r1(),r1(),r1(),r2(),r2(),r2(),r2(),r2(),r1(),r1()],
    [r1(),r1(),r1(),r2(),r2(),r2(),r2(),r2(),r1(),r1()],
    [r1() for col in range(10)]
    ]

# Print the image
def print_image(title, image):
    print(title)
    for row in image:
        print(row)
    print()

# Compute the histogram
# Assumes values are in the range 0--99
# Divide by 10 to get 10 bins
def compute_histogram(image):
    h = [0 for i in range(10)]
    for row in image:
        for pixel in row:
            h[pixel//10] += 1
    return h

# Compute the bin of the threshold for a given
#   fraction of the image size
def threshold_bin(hist, size, fraction):
    sum = 0
    i = 0
    while sum/size < fraction / 100.0:
        sum += hist[i]
        i += 1
    return i

# Compute the binary image by splitting on the threshold
def compute_binary_image(image, threshold):
    new_image = [row[:] for row in image] # Make copy
    for row in range(len(image)):
        for col in range(len(image[row])):
            if image[row][col] < threshold:
                new_image[row][col] = 10
            else:
                new_image[row][col] = 90
    return new_image


print_image("Original image", image)

print_image("Image with noise", image_with_noise)

# Compute histogram
hist = compute_histogram(image_with_noise)

print("Histogram")
print(hist)
print()

# For convenience, save size of image
size = len(image)*len(image[0])

# Try out various fractions for threshold
# Negative number to stop loop
while True:
    fraction = int(input("Background fraction: "))
    print()
    if fraction < 0:
        break
    # Compute bin and multiply by 10 for intensity
    threshold = threshold_bin(hist, size, fraction) * 10
    binary_image = compute_binary_image(image_with_noise, threshold)
    print_image("Binary image", binary_image)
