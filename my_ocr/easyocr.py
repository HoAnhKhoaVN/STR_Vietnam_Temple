from easyocr import Reader
from typing import Text, List, Any

reader = Reader(["ch_tra", "en"])
def ocr(
    img_filename: Text
)-> List[Any]:
    return reader.readtext(img_filename)
