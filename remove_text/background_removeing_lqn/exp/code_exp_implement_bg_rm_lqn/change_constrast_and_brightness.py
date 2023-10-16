# import the required library
import cv2
import numpy as np

# read the input image
# image = cv2.imread('test_sliding_window_numpy/BR_test_sliding_window_numpy.png')
image = cv2.imread('BR_35227268_1442578812555603_8324419005091676160_n_slide_window.png')

# define the alpha and beta
alpha = 3 # Contrast control
beta = 10 # Brightness control

# call convertScaleAbs function
adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

# Save image
cv2.imwrite(
    filename='BR_35227268_1442578812555603_8324419005091676160_n_slide_window_change_constrast.png',
    img = adjusted
)