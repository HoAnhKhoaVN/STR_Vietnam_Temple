import cv2

if __name__ == '__main__':

    bl_path = 'OUTPUT/sptn-page3-fig1-so01/sptn-page3-fig1-so01__Blackhat_13_13.png'
    bl = cv2.imread(filename= bl_path)
    bl_gray = cv2.cvtColor(bl, cv2.COLOR_BGR2GRAY)
    bl_gray_igv = 255-bl_gray

    bg_path = 'OUTPUT/sptn-page3-fig1-so01/sptn-page3-fig1-so01Tohat13_13.png'
    bg = cv2.imread(filename= bg_path)
    bg_gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)

    img_path = 'img/sptn-page3-fig1-so01.jpeg'
    img = cv2.imread(filename= img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow('bl_gray_igv', bl_gray_igv)
    cv2.imshow('Foreground', bg_gray - img_gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


