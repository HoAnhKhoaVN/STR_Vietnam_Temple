source D:/Master/OCR_Nom/fulllow_ocr_temple/.venv/Scripts/activate

# cleval -g=input/ground_truth/ground_truth.zip \
#        -s=input/dectection_results/dectection_results.zip

cleval -g=che_phong/gt/gt.zip -s=che_phong/bg_rm_lqn_pred/bg_rm_lqn_pred.zip --E2E -v --DEBUG --PROFILE > che_phong/profile__rm_bg_lqn__che_phong.txt