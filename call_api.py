import requests
if __name__ == '__main__':
    url = "http://127.0.0.1:5000/predict"
    fn = 'input\hoang_phi_cau_doi.jpg'
    payload = {}
    files=[
    ('content_img',('hoang_phi_cau_doi.jpg',open(fn,'rb'),'image/jpeg'))
    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
