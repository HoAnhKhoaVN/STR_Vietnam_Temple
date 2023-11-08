# import the necessary packages
import argparse
import cv2
ROOT = 'OUTPUT'
import os



if __name__ == "__main__":
    if not os.path.exists(ROOT):
        os.makedirs(ROOT, exist_ok= True)


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


    # region get file name
    fn = args["image"].split('/')[-1].split('.')[0]
    fd_path = os.path.join(ROOT, fn)

    os.makedirs(
        name = fd_path,
        exist_ok= True
    )
    org_path = os.path.join(ROOT,f'{fn}_grayscale.png')
    cv2.imwrite(org_path, gray)





    # endregion


    # region Apply a series of opening operationss
    kernelSizes = [(13,13)]
    # loop over the kernels sizes
    for kernelSize in kernelSizes:
        # construct a rectangular kernel from the current size and then
        # apply an "opening" operation
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelSize)
        # opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel,iterations=200)
        tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel, iterations=200)

        black_hat_fn = os.path.join(fd_path, f"{fn}__Blackhat_{kernelSize[0]}_{kernelSize[1]}.png")
        to_hat_fn = os.path.join(fd_path, f"{fn}Tohat{kernelSize[0]}_{kernelSize[1]}.png")
        cv2.imwrite(black_hat_fn, blackhat)
        cv2.imwrite(to_hat_fn, tophat)
    # endregion