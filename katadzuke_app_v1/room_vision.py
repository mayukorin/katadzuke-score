from statistics import median
import numba, base64, cv2, math, cloudinary
import numpy as np
from numba.typed import Dict
from numba.types import types
from .models import FloorHueRange


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

    return floor_cnt


def calc_percent_of_floors(base64_img, floor_hue_ranges_list):

    np_upload_room_photo = np.asarray(
        bytearray(base64.b64decode(base64_img.split(",")[1])), dtype="uint8"
    )
    img = cv2.imdecode(np_upload_room_photo, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    total_cnt_of_pixels = hsv.shape[0] * hsv.shape[1]
    floor_cnt_of_pixels = cnt_floor_cnt_of_pixels(hsv, floor_hue_ranges_list)

    return math.floor(floor_cnt_of_pixels / total_cnt_of_pixels * 100)


@numba.jit
def calc_upload_floor_photo_hue_cnt_list(base64_img):

    np_upload_room_photo = np.asarray(
        bytearray(base64.b64decode(base64_img.split(",")[1])), dtype="uint8"
    )
    img = cv2.imdecode(np_upload_room_photo, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    area = np.int64(hsv.shape[0] * hsv.shape[1])

    hue_cnt_dict = Dict.empty(key_type=types.int64,value_type=types.int64)

    for h in range(hsv.shape[0]):
        for w in range(hsv.shape[1]):
            if hue_cnt_dict.get(np.int64(hsv[h, w, 0])) is None:
                hue_cnt_dict[np.int64(hsv[h, w, 0])] = 1
            else:
                hue_cnt_dict[np.int64(hsv[h, w, 0])] += 1

    hue_cnt_list = []
    for hsv_value in hue_cnt_dict:
        if hue_cnt_dict[hsv_value] >= area*0.3: 
            hue_cnt_list.append(hsv_value)

    return hue_cnt_list



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


def merge_floor_hue_ranges_into_upload_floor_photo_hue_cnt_list(floor_hue_ranges, new_floor_photo_hue_cnt_list):

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

def create_new_hue_ranges_model(hue_floor_pixel_cnt_list, user):

    pre_hue_value = -1
    is_floor_hue = False
    for hue_value, floor_pixel_cnt in enumerate(hue_floor_pixel_cnt_list):
        if is_floor_hue:
            if floor_pixel_cnt <= 0:
                print(hue_value)
                floor_hue_range = FloorHueRange()
                floor_hue_range.user = user
                floor_hue_range.min_hue = pre_hue_value
                floor_hue_range.max_hue = hue_value - 1
                floor_hue_range.save()
                print(floor_hue_range.min_hue)
                print(floor_hue_range.min_hue)
                is_floor_hue = False

        else:
            if floor_pixel_cnt > 0:
                print(hue_value)
                is_floor_hue = True
