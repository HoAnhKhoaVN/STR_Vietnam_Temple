import argparse
import os
# from my_ocr.easyocr import ocr
from my_ocr.pp_ocr.test import ocr
from translate.hvdict import hvdic_translate
# from translate.hcmus_api import hcmus_translate
from my_postprocess.postprocess import _postprocess
import logging
from typing import Text
from PIL import Image
from log.logger import setup_logger
from time import time
setup_logger()

def process(
    image_input_file: Text,
)-> Image:
    start_time = time()
    # region Preprocessing
    # endregion Preprocessing

    # region OCR    
    result = ocr(image_input_file)
    print(f'Result: {result}')

    # endregion OCR
    logging.debug(f"Before: {result}")


    # region Chinese language model
    # endregion

    # region translate to Vietnamese
    list_dict_result = []
    for bbox, han_nom_script, _ in result:
        print(f'bbox: {bbox}')
        print(f'text: {han_nom_script}')
        logging.debug(f"han_nom_script : {han_nom_script}")
        translation_script = hvdic_translate(text = han_nom_script)
        # translation_script = hcmus_translate(text = han_nom_script)
        list_dict_result.append({
            'bbox': bbox,
            'text': translation_script
            }
        )
    # endregion
    print(f'list_dict_result: {list_dict_result}')
    logging.debug(f"After: {list_dict_result}")
    # region postprocessing
    pil_img_output = _postprocess(
        image_fn= image_input_file,
        list_dict_result = list_dict_result,
    )
    # endregion
    end_time = time()
    logging.info(f"Time inference: {(end_time-start_time)}s")
    return pil_img_output


def main():
    # region Input
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True,
        help="Đường dẫn đến ảnh muốn nhận dạng")
    
    ap.add_argument("-o", "--output", required=True,
        help="Đường dẫn đến ảnh kết quả")
    args = vars(ap.parse_args())

    _INPUT = args["input"]
    _OUTPUT = args["output"]
    
    logging.info("================================")
    logging.info(f"Input: {_INPUT}")
    logging.info(f"Output: {_OUTPUT}")
    # endregion Input

    pil_img_output = process(image_input_file=_INPUT)

    # region output
    pil_img_output.save(_OUTPUT)
    pil_img_output.show()
    # endregion
    logging.info("==============END TASK==================")

if __name__ == "__main__":
    # main()

    img: Image = process(
        image_input_file="D:/Master/OCR_Nom/fulllow_ocr_temple/input/365277540_2640178542812959_3109842896588336028_n.jpg"
    )
    img.save('output/365277540_2640178542812959_3109842896588336028_n_pdocr.jpg')



    # img: Image = process(
    #     image_input_file="D:/Master/OCR_Nom/fulllow_ocr_temple/input/vertical_demo.png"
    # )
    # img.save('output/vertical_demo_pdocr.png')