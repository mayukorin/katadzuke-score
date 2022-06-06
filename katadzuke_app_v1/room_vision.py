import cv2
from statistics import  median
import numba


@numba.jit
def caculate_score(hsv):
    score = 0
    for h in range(hsv.shape[0]):
        for w in range(hsv.shape[1]):
            # print(hsv[h, w, 0])
            if hsv[h, w, 0] != 15 and hsv[h, w, 0] !=16:
                score += 1
    return score/(hsv.shape[0]*hsv.shape[1])*100

def tranlate_rgb_to_csv(img_path):
    
    org_img = cv2.imread(img_path)
    hsv = cv2.cvtColor(org_img, cv2.COLOR_BGR2HSV)
    return caculate_score(hsv)


def tranlate_rgb_to_csv2(np_img):
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return caculate_score(hsv)