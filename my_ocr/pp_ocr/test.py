from paddleocr import PaddleOCR
from typing import List
pdocr = PaddleOCR(use_angle_cls=True, lang='ch')
def ocr(
    img_path : str
)-> List:
    result = pdocr.ocr(img_path, cls=True)[0]

    res= []
    # region Postprocessing
    for line in result:
        _bbox, (text, prop) = line
        bbox = [[int(bb[0]), int(bb[1])] for bb in _bbox]
        res.append([bbox, text, prop])
    # endregion
    return res
    


if __name__ == "__main__":
    img_path = "D:/Master/OCR_Nom/fulllow_ocr_temple/input/demo_img.png"
    result = ocr(img_path)
    bbox, text, prop = result[0]
    print(f'bbox: {bbox}')
    print(f'text: {text} - prop: {prop}')
        

