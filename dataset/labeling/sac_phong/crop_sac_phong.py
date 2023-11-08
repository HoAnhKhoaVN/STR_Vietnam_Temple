import cv2
import numpy as np
import glob
import os
from tqdm import tqdm
import imutils


configs = {
    'FC_LowerThreshold': 0,
    'FC_HigherThreshold': 50,
    'FC_RetrivalMode': 'cv2.RETR_EXTERNAL',
    'FC_ApproxMode': 'cv2.CHAIN_APPROX_SIMPLE',
    'AB_MinAcceptedBBoxArea': 200000,
    'AB_AcceptedQuantile': 0.25,
    'AB_RejectedWHRatio': 3
}

OUTPUT = 'sptn_figures'
if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT, exist_ok= True)


def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

def find_contour(img, configs):
    # parse args
    FC_LowerThreshold = int(configs['FC_LowerThreshold'])
    FC_HigherThreshold = int(configs['FC_HigherThreshold'])
    FC_RetrivalMode = str(configs['FC_RetrivalMode'])
    FC_ApproxMode = str(configs['FC_ApproxMode'])

    if FC_RetrivalMode == 'cv2.RETR_EXTERNAL':
        FC_RetrivalMode = cv2.RETR_EXTERNAL

    if FC_ApproxMode == 'cv2.CHAIN_APPROX_SIMPLE':
        FC_ApproxMode = cv2.CHAIN_APPROX_SIMPLE

    
    # select with color range from FC_LowerThreshold to FC_HigherThreshold
    mask = cv2.inRange(img, FC_LowerThreshold, FC_HigherThreshold)

    # locate the selection
    # cv2.findContours returns a 3-element tuple where contours, threshold are always the two last most elements
    contours = cv2.findContours(mask.copy(), FC_RetrivalMode, FC_ApproxMode)[-2]
    
    return contours

def get_accepted_bboxes(contours, configs):
    # parse args
    AB_MinAcceptedBBoxArea = int(configs['AB_MinAcceptedBBoxArea'])
    AB_AcceptedQuantile = float(configs['AB_AcceptedQuantile'])
    AB_RejectedWHRatio = float(configs['AB_RejectedWHRatio'])


    list_of_bboxes, tmp_bboxes, areas = [], [], []

    # filter based on area
    for contour in contours:
        (l, t, w, h) = cv2.boundingRect(contour)
        if w*h >= AB_MinAcceptedBBoxArea:
            tmp_bboxes.append((w*h, ((l, t), (l+w, t+h))))
            areas.append(w*h)
    tmp_bboxes = sorted(tmp_bboxes, key=lambda x: x[0])
    areas = sorted(areas)
    q = np.quantile(areas, AB_AcceptedQuantile)

    # filter based on width-height ratio
    for i in range(len(areas)):    
        (min_x, min_y) = tmp_bboxes[i][1][0]
        (max_x, max_y) = tmp_bboxes[i][1][1]
        if abs(max_x - min_x) > abs(max_y - min_y):
            if abs(max_x - min_x) / abs(max_y - min_y) >= AB_RejectedWHRatio:
                continue
        elif abs(max_y - min_y) / abs(max_x - min_x) >= AB_RejectedWHRatio:
            continue
        
        if areas[i] >= q:
            list_of_bboxes.append(tmp_bboxes[i][1])
    
    return list_of_bboxes

def rectangle_detect(image_path, configs, block_size=871):# parse args
    AB_MinAcceptedBBoxArea = int(configs['AB_MinAcceptedBBoxArea'])
    AB_RejectedWHRatio = float(configs['AB_RejectedWHRatio'])
    
    # Load image, grayscale, adaptive threshold
    n,e = os.path.splitext(os.path.basename(image_path))
        
    image = cv2.imread(image_path)
    result = image.copy()
    thresh = cv2.imread(image_path, 0)
    thresh = cv2.adaptiveThreshold(thresh,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,block_size,2)

    # Fill rectangular contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]


    
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (255,255,255), -1)

    # Morph open
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=8)

    # Draw rectangles
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    
    # sorted_ctrs = sorted(cnts, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * image.shape[1] )
    # sorted_ctrs = sorted(cnts, key=cv2.contourArea, reverse=False)
    
    # sort the contours according to the provided method
    (sorted_ctrs, boundingBoxes) = sort_contours(cnts, method="bottom-to-top")
    for i, c in enumerate(sorted_ctrs[::-1]):
        x,y,w,h = cv2.boundingRect(c)
        if w*h >= AB_MinAcceptedBBoxArea and h/w <= 2 and w/h <= 5:
            # cv2.rectangle(image, (x, y), (x + w, y + h), (255,0,255), 5) # draw rectangles
            # cutout_figure_folder = os.path.dirname(image_path).replace('pdf-figures','figures')
            cv2.imwrite(f'{OUTPUT}/{n}-fig{i+1}.jpeg', image[y:y+h,x:x+w])


if __name__ == '__main__':
    IMAGE_PATHS = sorted(glob.glob('pdf2img_sac_phong_trieu_nguyen/*.jpg'))[:]
    for image_path in tqdm(IMAGE_PATHS, desc = "Progress crop sac phong: "):
        # use rectangle_detect
        n,e = os.path.splitext(os.path.basename(image_path))
    
        image_id = int(n.split('-')[1].replace('page',''))
        if image_id < 3 or image_id > 118:
            continue
    
        block_size = 551
        if image_id in [88]:
            block_size = 351
        rectangle_detect(image_path, configs, block_size)