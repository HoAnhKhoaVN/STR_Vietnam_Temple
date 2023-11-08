import os
import pandas as pd
from tqdm import tqdm
from numpy import nan

def process(
    path : str,
    output_dir : str,
    debug: bool = True
)-> None:
    if debug:
        print(f'Path : {path}')
        print(f'Output folder : {output_dir}')

    # region Read file xlsx
    df = pd.read_excel(io = path)
    if debug:
        print(f'DF: {df}')
        print(f'Df columns: {df.columns}')
        print(f"First line: {df['Line'][0]}")
    df.replace(
        {nan: 0},
        inplace= True
    )

    df.replace(
        {' ': ''},
        inplace = True
    )

    if debug:
        print(f'DF after replace NaN to zero')
        print(df)
    # endregion

    # region get Nom script
    dict_nom_script = {}
    start = 0
    end = 0
    next_count = 2
    for idx in tqdm(range(len(df)), desc = 'Get Nom script: '):
        if df['Line'][idx] and int(df['Line'][idx]) == next_count:
            end = idx
            tmp = []
            for j in range(start, end -1):
                tmp.append(df['Nom_script'][j])
            dict_nom_script[str(next_count-1)] = tmp
            start = end
            next_count+=1
        # if debug and idx == 100:
        #     break
    # endregion


    # region get last page
    tmp = []
    for j in range(start, len(df)):
        tmp.append(df['Nom_script'][j])
    dict_nom_script[str(next_count-1)] = tmp

    if debug:
        print(f'First page: {dict_nom_script[list(dict_nom_script.keys())[0]]}')
        print(f'Last page: {dict_nom_script[list(dict_nom_script.keys())[-1]]}')
    # endregion

    # region merge line and delete puncation
    for k, v in dict_nom_script.items():
        try:
            tmp = ''.join(v)
            tmp = tmp.replace('，', '').replace('。', '').replace('：', '').replace('；', '').replace('！', '')
            dict_nom_script[k] = tmp
        except Exception as e:
            print(f'Error: {e} - value : {v} -- key : {k}')
    if debug:
        print(f'\n*** Merge line and delete puncation *** \n')
        print(f'First page: {dict_nom_script[list(dict_nom_script.keys())[0]]}')
        print(f'Last page: {dict_nom_script[list(dict_nom_script.keys())[-1]]}')

    # endregion

    # region Origazation folder
    if debug: 
        print(f'\n*** Origazation folder: {output_dir} *** \n')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok= True)

    for k, v in tqdm(dict_nom_script.items(), desc = 'Write output to txt file:'):
        with open(os.path.join(output_dir, f'{k}.txt'), 'w', encoding= 'utf-8') as f:
            f.write(v)
    # endregion 

if __name__ == '__main__':
    PD_PATH =  'D:/Master/OCR_Nom/fulllow_ocr_temple/dataset/labeling/sac_phong/sac_phong_digitilization'
    OUT_PATH = 'D:/Master/OCR_Nom/fulllow_ocr_temple/dataset/labeling/sac_phong/sac_phong_digitilization_KHOA'
    LST_EXCEL_FILE = [
        # "CHẾ PHONG.xlsx",
        'SẮC PHONG.xlsx',
        'CHIẾU.xlsx'
    ]
    LST_FD_PATH = [
        # 'che_phong',
        'sac_phong',
        'chieu'
    ]
    DEBUG = True
    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH, exist_ok= True)

    for input_path, output_name in zip(LST_EXCEL_FILE, LST_FD_PATH):
        process(
            path = os.path.join(PD_PATH,input_path),
            output_dir= os.path.join(OUT_PATH, output_name)
        )
    


