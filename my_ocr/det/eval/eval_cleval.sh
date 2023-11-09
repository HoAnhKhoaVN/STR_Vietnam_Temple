source D:/Master/OCR_Nom/fulllow_ocr_temple/.venv/Scripts/activate

cleval -g=ground_truth.zip \
       -s=prediction.zip \
       --E2E \
       -v \
       --DEBUG \
       --PROFILE > profile.txt