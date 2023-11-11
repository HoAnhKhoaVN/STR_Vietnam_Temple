# source D:/Master/OCR_Nom/deploy/azure/str_vietnam_temple/.venv/Scripts/activate
source D:/Master/OCR_Nom/fulllow_ocr_temple/.venv/Scripts/activate

INPUT='input'
OUTPUT='output/111123_08_33'

mkdir -p $OUTPUT

python predict.py -i $INPUT -o $OUTPUT