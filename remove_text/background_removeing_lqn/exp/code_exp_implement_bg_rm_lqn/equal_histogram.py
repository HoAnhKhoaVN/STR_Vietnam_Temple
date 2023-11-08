import cv2
import argparse
import numpy as np


if __name__ == '__main__':
    print(f'Code preprocess')
    
    # region construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
    help="path to input image")
    args = vars(ap.parse_args())
    # endregion


    # region load the image, convert it to grayscale, and display it to our screen
    image = cv2.imread(args["image"])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # endregion

    # region Image enhancement
    # denoised_image = cv2.fastNlMeansDenoisingColored(gray, None, 10, 10, 7, 21)
        
    # Remove noise using a median filter 
    filtered_image = cv2.medianBlur(src = gray, ksize = 3)

    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) 
    sharpened_image = cv2.filter2D(filtered_image, -1, kernel=kernel)


    # Equalize the histogram 
    equalized_image = cv2.equalizeHist(sharpened_image) 


    cv2.imshow('Image', image)
    # cv2.imshow('denoised_image', denoised_image)
    cv2.imshow('sharpened_image', sharpened_image)
    cv2.imshow('filtered_image', filtered_image)
    cv2.imshow('equalized_image', equalized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # endregion