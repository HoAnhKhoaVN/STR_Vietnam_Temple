import argparse
import cv2
ROOT = 'OUTPUT'
import os
APPROVED_PACKAGES ='custome_opening'
B = 20
iterator = 1000
kernelSize = (13,13)

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
    gray = 255 - gray
    # endregion


    # region get file name
    fn = args["image"].split('/')[-1].split('.')[0]
    fd_path = os.path.join(ROOT, f'{fn}__{APPROVED_PACKAGES}__{B}__iter{iterator}__kernel_{kernelSize[0]}_{kernelSize[1]}')

    os.makedirs(
        name = fd_path,
        exist_ok= True
    )
    org_path = os.path.join(ROOT,f'{fn}_grayscale.png')
    cv2.imwrite(org_path, gray)
    # endregion

    # region Apply a series of opening operationss
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelSize)
    eroded = cv2.erode(gray.copy()-B, None, iterations=iterator)
    dilated = cv2.dilate(eroded+B, None, iterations=iterator)
    h = gray- dilated

    eroded_fn = os.path.join(fd_path, f"{fn}__eroded_{kernelSize[0]}_{kernelSize[1]}.png")
    dilated_fn = os.path.join(fd_path, f"{fn}__dilated_{kernelSize[0]}_{kernelSize[1]}.png")
    h_fn = os.path.join(fd_path, f"{fn}__h_{kernelSize[0]}_{kernelSize[1]}.png")

    cv2.imwrite(eroded_fn, eroded)
    cv2.imwrite(dilated_fn, dilated)
    cv2.imwrite(h_fn, h)
