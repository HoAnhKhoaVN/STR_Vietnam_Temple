import json
import time
import requests

ERR_TRANSLATE_STR = 'Cannot translate this text.'


def hcmus_translate(text):
    url = ' https://api.clc.hcmus.edu.vn/nom_translation/90/1'
    response = requests.request('POST', url, data={'nom_text': text})
    time.sleep(0.3)

    try:
        result = json.loads(response.text)['sentences']
        result = result[0][0]['pair']['modern_text']
        return result
    except:
        print(f'[ERR] "{text}": {response.text}')
        return ERR_TRANSLATE_STR

if __name__ == '__main__':
    text ='越南'
    print(hcmus_translate(text))