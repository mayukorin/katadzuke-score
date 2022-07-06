from statistics import median
import numba, base64, cv2, math, cloudinary
import numpy as np
from numba.typed import Dict
from numba.types import types


@numba.jit
def cnt_floor_cnt_of_pixels(hsv, floor_hue_ranges_list):
    floor_cnt = 0
    for h in range(hsv.shape[0]):
        for w in range(hsv.shape[1]):
            # print(hsv[h, w, 0])5
            hue_value = hsv[h, w, 0]
            
            for index in range(0, len(floor_hue_ranges_list), 2):
                hue_min = floor_hue_ranges_list[index]
                hue_max = floor_hue_ranges_list[index+1]
                if hue_max >= hue_value and hue_value >= hue_min:
                    floor_cnt += 1
                elif hue_max >= hue_value + 360 and hue_value + 360 >= hue_min:
                    floor_cnt += 1

            '''
            hue_min = 14
            hue_max = 17
            if hue_max >= hue_value and hue_value >= hue_min:
                is_floor = True
            if hue_max >= hue_value + 360 and hue_value + 360 >= hue_min:
                is_floor = True 
            if is_floor:
                cnt += 1
            '''

    print("ok")
    return floor_cnt


def calc_percent_of_floors(base64_img, floor_hue_ranges_list):

    np_upload_room_photo = np.asarray(
        bytearray(base64.b64decode(base64_img.split(",")[1])), dtype="uint8"
    )
    img = cv2.imdecode(np_upload_room_photo, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print("ここまで")

    total_cnt_of_pixels = hsv.shape[0] * hsv.shape[1]
    floor_cnt_of_pixels = cnt_floor_cnt_of_pixels(hsv, floor_hue_ranges_list)

    return math.floor(floor_cnt_of_pixels / total_cnt_of_pixels * 100)

@numba.jit
def get_hsv_value_list(base64_img):

    np_upload_room_photo = np.asarray(
        bytearray(base64.b64decode(base64_img.split(",")[1])), dtype="uint8"
    )
    img = cv2.imdecode(np_upload_room_photo, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    area = np.int64(hsv.shape[0] * hsv.shape[1])

    hsv_value_dict = Dict.empty(key_type=types.int64,value_type=types.int64)
    # hsv_value_dict = {}
    cnt = 0
    for h in range(hsv.shape[0]):
        for w in range(hsv.shape[1]):
            if hsv_value_dict.get(np.int64(hsv[h, w, 0])) is None:
                hsv_value_dict[np.int64(hsv[h, w, 0])] = 1
            else:
                hsv_value_dict[np.int64(hsv[h, w, 0])] += 1
    
    return hsv_value_dict


@numba.jit
def get_hsv_value_list2(base64_img):

    np_upload_room_photo = np.asarray(
        bytearray(base64.b64decode(base64_img.split(",")[1])), dtype="uint8"
    )
    img = cv2.imdecode(np_upload_room_photo, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    area = np.int64(hsv.shape[0] * hsv.shape[1])

    hsv_value_dict = Dict.empty(key_type=types.int64,value_type=types.int64)
    # hsv_value_dict = {}
    cnt = 0
    for h in range(hsv.shape[0]):
        for w in range(hsv.shape[1]):
            if hsv_value_dict.get(np.int64(hsv[h, w, 0])) is None:
                hsv_value_dict[np.int64(hsv[h, w, 0])] = 1
            else:
                hsv_value_dict[np.int64(hsv[h, w, 0])] += 1
    '''
    hsv_value_dict = Dict.empty(key_type=types.int64,value_type=types.int64)
    for h in range(hsv.shape[0]):
        for w in range(hsv.shape[1]):
            hsv_value_dict[np.int64(hsv[h, w, 0])] += np.int64(1)
    '''

    hsv_value_list = []
    for hsv_value in hsv_value_dict:
        if hsv_value_dict[hsv_value] >= area*0.3: 
            hsv_value_list.append(hsv_value)

    return hsv_value_list



def upload_photo_to_cloudinary(base64Content):

    response = cloudinary.uploader.upload(file=base64Content)

    return response["public_id"], response["url"]


def destroy_photo_from_cloudinary(photo_public_id):

    cloudinary.uploader.destroy(photo_public_id)


def reflect_room_photo_score_to_amount_of_money(
    threshould_fine_score,
    threshould_reward_score,
    amount_of_fine,
    amount_of_reward,
    new_room_photo_score,
):

    add_amount_of_money = 0

    if new_room_photo_score <= threshould_fine_score:
        add_amount_of_money -= amount_of_fine
    elif new_room_photo_score >= threshould_reward_score:
        add_amount_of_money += amount_of_reward

    return add_amount_of_money


def remove_reflection_of_room_photo_score_from_amount_of_money(
    threshould_fine_score,
    threshould_reward_score,
    amount_of_fine,
    amount_of_reward,
    prev_room_photo_score,
):

    remove_amount_of_money = 0

    if prev_room_photo_score <= threshould_fine_score:
        remove_amount_of_money -= amount_of_fine
    elif prev_room_photo_score >= threshould_reward_score:
        remove_amount_of_money += amount_of_reward

    return remove_amount_of_money


def calc_floor_hue_cnt_list(floor_hue_ranges, new_floor_photo_hue_cnt_list):

    floor_hue_cnt_list = [0] * 721

    for floor_hue_range in floor_hue_ranges:
            floor_hue_cnt_list[floor_hue_range.min_hue] += 1
            floor_hue_cnt_list[floor_hue_range.max_hue+1] -= 1
       

    for hsv_value in new_floor_photo_hue_cnt_list:
        if hsv_value -2 < 0:
            hsv_value += 360
        hsv_min = hsv_value - 2
        hsv_max = hsv_value + 2

        floor_hue_cnt_list[hsv_min] += 1
        floor_hue_cnt_list[hsv_max+1] -= 1

    for hsv_value in range(1, 720):
        
        floor_hue_cnt_list[hsv_value] = floor_hue_cnt_list[hsv_value-1] + floor_hue_cnt_list[hsv_value]

    return floor_hue_cnt_list
