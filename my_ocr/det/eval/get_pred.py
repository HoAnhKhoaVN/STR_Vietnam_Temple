from constant import IMAGE_CHIEU_PATH, LABEL_CHIEU_PATH, LABEL_NAME, JSON_NAME
from typing import Any, Text, List
from paddleocr import PaddleOCR
import os
import json
from tqdm import tqdm
import argparse

class PredictionPPOCR(object):
    def __init__(
        self, 
        image_path: Text,
        json_name: Text,
        debug: bool = True
    ) -> None:
        self.image_path = image_path
        self.out_path = json_name
        print(f'out_path: {self.out_path}')
        self.model = PaddleOCR(use_angle_cls=True, lang='ch')
        self.debug = debug
        self.data = self.read_data()

        if self.debug:
            print(f'**** INIT *****')
            print(f'image_path: {image_path}')
            print(f'json_name: {json_name}')

    def ocr(
        self,
        img_path : Text,
        img_name: Text
    )-> list:
        result = self.model.ocr(img_path, cls=True)[0]
        res= []
        # region Postprocessing
        for line in result:
            _bbox, (text, prob) = line
            bbox = [[int(bb[0]), int(bb[1])] for bb in _bbox]
            res.append({
                'transcription': text,
                'points': bbox,
                'prob': prob
            })
        # endregion
        if self.debug:
            print(f'Result inference {img_name} : {res}')
        return res

    
    def predict(self):
        res = {}
        if self.debug:
            count = 0
        for img_name in tqdm(os.listdir(self.image_path), desc = 'Progress predict image:'):
            if '.' not in img_name: # folder
                if self.debug:
                    print(f'{img_name} is a folder!!!')
                continue
            _ , ext= img_name.split('.')
            if ext.lower() not in ['jpg', 'jpeg', 'png']:
                if self.debug:
                    print(f'{img_name} is not image!!!')

                continue

            img_path = os.path.join(self.image_path, img_name)
            res[img_name] = self.ocr(img_path, img_name)
            if self.debug:
                count+=1
                if count == 1:
                    break
                

        # region save to json format
        print(f'Output file: {self.out_path}')
        with open(self.out_path, 'w', encoding='UTF-8-sig') as f:
            json.dump(
                obj= res,
                fp = f,
                indent=4
            )
        # endregion

    def read_data(self):
        if not os.path.exists(self.out_path):
            if self.debug:
                print(f"D not exist {self.out_path} => Process convert .txt file to .json file!!!")
            self.predict()

        with open(self.out_path, 'r', encoding= 'UTF-8-sig') as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def get_file_name_without_extension(file_path: Text):
        return os.path.splitext(os.path.basename(file_path))[0]  

    def convert_to_format_mAP(self, path):
        for k, v in tqdm(self.data.items(), desc="Progress convert to format calculate mAP: "):
            if self.debug:
                print(f'key: {self.get_file_name_without_extension(k)}')
                for _v in v:
                    transcription = _v['transcription']
                    points = _v['points']
                    prob = _v['prob']
                    tl_br = points[0]+ points[2]
                    print(f'{transcription} {str(prob)} {" ".join(list(map(str,tl_br)))}')
                break
            else:
                output_file = os.path.join(
                        path,
                        self.get_file_name_without_extension(k)
                    )
                with open(f'{output_file}.txt', 'w', encoding='UTF-8-sig') as f:
                    for _v in v:
                        transcription = _v['transcription']
                        points = _v['points']
                        prob = _v["prob"]
                        tl_br = points[0]+ points[1]+ points[2]+points[3]
                        f.write(f'{",".join(list(map(str,tl_br)))},{transcription}\n')



if __name__ == '__main__':
    # # region get argument
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '-ip', 
    #     '--img_path', 
    #     help="Path to folder contain images"
    # )
    # parser.add_argument(
    #     '-jp', 
    #     '--json_path',  
    #     help="Path to json file which save the result"
    # )

    # parser.add_argument(
    #     '-db', 
    #     '--debug',  
    #     help="show debug information",
    #     action="store_true",
    # )
    # args = parser.parse_args()
    # # endregon

    # PredictionPPOCR(
    #     image_path= args.img_path,
    #     json_name= args.json_path,
    #     debug = args.debug
    # ).predict()

    IMG_PATH='che_phong/bg_rm_lqn'
    JSON_PATH='che_phong/pred_ppocr_bg_rm.json'

    PredictionPPOCR(
        image_path= IMG_PATH,
        json_name= JSON_PATH,
        debug = False
    ).convert_to_format_mAP(
        path = 'che_phong/bg_rm_lqn_pred'
    )

             





