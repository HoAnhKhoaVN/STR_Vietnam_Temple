# I
# ROOT='eval_img_click_next'
# url='https://www.facebook.com/photo/?fbid=1048393872167069&set=g.1087253598032345'
# ttp='13_01_2020'
# root_dir=$ROOT
# number=500

# II
# ROOT='eval_img_click_next'
# url='https://www.facebook.com/photo/?fbid=645975612241128&set=g.1087253598032345'
# ttp='19_01_2017'
# root_dir=$ROOT
# number=500

#III
# ROOT='eval_img_click_next'
# url='https://www.facebook.com/photo/?fbid=1175204195956510&set=g.1087253598032345'
# ttp='23_08_2017'
# root_dir=$ROOT
# number=2000

#IV
# ROOT='eval_img_click_next'
# url='https://www.facebook.com/photo/?fbid=1898950713754894&set=g.1087253598032345'
# ttp='22_11_2017'
# root_dir=$ROOT
# number=2000

#V
ROOT='eval_img_click_next'
url='https://www.facebook.com/photo/?fbid=456868081332383&set=g.1087253598032345'
ttp='29_04_2017'
root_dir=$ROOT
number=500

source d:/Master/OCR_Nom/fulllow_ocr_temple/.venv/Scripts/activate
# output_dir=log/$root_dir
# mkdir -p "$output_dir"
# log_file=$output_dir/cmd_$root_dir.log
# echo "Log into $log_file"

python click_next_to_download.py \
    -url $url \
    -ttp $ttp \
    -r $root_dir \
    -n $number
    # > $log_file 2>&1

echo Check log in: $ttp
