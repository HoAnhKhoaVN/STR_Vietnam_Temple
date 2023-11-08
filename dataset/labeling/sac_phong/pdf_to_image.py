# import module
from pdf2image import convert_from_path
import os


# Store Pdf with convert_from_path function
images = convert_from_path('Sac Phong Trieu Nguyen.pdf')
ROOT = 'pdf2img_sac_phong_trieu_nguyen'

for i in range(len(images)):
    path = os.path.join(ROOT, f'page__{str(i).zfill(4)}.jpeg')
    images[i].save(path, 'JPEG')
