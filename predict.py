import os
import argparse
from main import process
from PIL import Image
from tqdm import tqdm


if __name__ == '__main__':
    # FODLER_IN_PATH = 'input'
    # FODLER_OUT_PATH = 'output_demo'

    # region 1. Args
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True,
        help="Path to folder input")
    
    ap.add_argument("-o", "--output", required=True,
        help="Path to folder output")
    args = vars(ap.parse_args())

    FODLER_IN_PATH = args["input"]
    FODLER_OUT_PATH = args["output"]


    # endregion

    # region 2. Handle folder
    if not os.path.exists(FODLER_IN_PATH):
        os.makedirs(FODLER_IN_PATH, exist_ok= True)
    
    if not os.path.exists(FODLER_OUT_PATH):
        os.makedirs(FODLER_OUT_PATH, exist_ok= True)
    # endregion

    # region 3. Get all image in folder and predict sequentially
    for fn in tqdm(os.listdir(FODLER_IN_PATH), desc= f"Predict image in folder {FODLER_IN_PATH}"):
        # region 3.1. Get image and process
        img_path = os.path.join(FODLER_IN_PATH, fn)
        pil_img_output : Image = process(image_input_file= img_path)
        # endregion

        # region 3.2: Handle output image
        output_img_path = os.path.join(FODLER_OUT_PATH, fn)
        pil_img_output.save(output_img_path)
        # endregion

    # endregion
