# Scene Text Recognition
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Xgdh0_snKMpJz4gn-kLQ8LwA9sTQ-VcQ?usp=sharing)

[Try Demo on our website](https://www.jaided.ai/easyocr)
## What's new
- 22 August 2023 - Version 0.2
    - Integrate OCR into the pipeline
    - Recognition for vertical texts.
    - Postprocessing for vertical texts.
    

- 11 August 2023 - Version 0.1
    - Code fullflow for STR Chinese Temples.
    - Code backend and fronents for demo.
    - Code postprocessing for final output.

## What's coming next

- Train more accurate model detection and recognition text
- Collect and label datasets.
- Host on server have GPU.

## Todo
### GUI
1. Show time to inference
2. Add download functionality
3. Clear output canvas when call API
4. Write code by React
5. Host on the server

6. Format log file
7. Delete unnecessary information


### Backend
1. Host on server


## Input and output
### Input
![Input](image/input_img.jpg)
### Output
![output](image/output_img.png)

## Installation
Install using `pip`
``` bash
pip install -r requirements.txt
```
### To use PP-OCR method
1. Download wheel PyMuPDF from [GG Drive](https://drive.google.com/file/d/1bYdtLr2tkyWZJr-TBSO8MB6w-BZTxkaG/view?usp=drive_link)
2. Install PyMuPDF
```sh
pip install PyMuPDF-1.20.2-cp311-cp311-win_amd64.whl
```
3. Install PaddleOCR
```sh
pip install paddleocr
```

## Run code
Change input and output path in `run.sh`. Then run this command:
``` bash
sh run.sh
```

## Run demo
### Run backend
``` bash
flask run
```
### Run frontend
Double click `frontend.html` to run the frontend.
![GUI](image/UI.png)

## Log
We write log in folder  `log`. Each log file will contain the log message every day.

## Fullflow diagram
![fullflow diagram](image/fullow_str_temple.png)

### Postprocessing
![Postprocess diagram](image/detail_postprocess.png)

### Preprocessing

### OCR
#### Text Detection


#### Text Recognition



## Dataset
### Synthesis


### Reality


### Label

## Language Model

## Translate from accent Vietnamese to modern Vietnamese



## Documentation









## References
