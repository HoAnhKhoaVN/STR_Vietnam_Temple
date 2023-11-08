source D:/Master/OCR_Nom/fulllow_ocr_temple/.venv/Scripts/activate

IMG_PATH='che_phong/img'
JSON_PATH='pred_ppocr_original.json'

python get_pred.py -ip $IMG_PATH -jp $JSON_PATH
