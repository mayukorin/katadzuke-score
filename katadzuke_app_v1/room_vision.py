from statistics import  median
import numba, base64, cv2, math
import numpy as np


@numba.jit
def cnt_floor_cnt_of_pixels(hsv):
    cnt = 0
    for h in range(hsv.shape[0]):
        for w in range(hsv.shape[1]):
            # print(hsv[h, w, 0])
            if hsv[h, w, 0] == 15 or hsv[h, w, 0] ==16:
                cnt += 1
    return cnt


def calc_percent_of_floors(base64_img):

    np_upload_room_photo = np.asarray(bytearray(base64.b64decode( base64_img.split(',')[1] )), dtype="uint8")
    img = cv2.imdecode(np_upload_room_photo, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print("ここまで")
    
    total_cnt_of_pixels = hsv.shape[0]*hsv.shape[1]
    floor_cnt_of_pixels = cnt_floor_cnt_of_pixels(hsv)

    return math.floor(floor_cnt_of_pixels/total_cnt_of_pixels*100)
