from statistics import median
import numba, base64, cv2, math, cloudinary
import numpy as np


@numba.jit
def cnt_floor_cnt_of_pixels(hsv, floor_hue_ranges_list):
    cnt = 0
    for h in range(hsv.shape[0]):
        for w in range(hsv.shape[1]):
            # print(hsv[h, w, 0])5
            hue_value = hsv[h, w, 0]
            is_floor = False
            
            for index in range(0, len(floor_hue_ranges_list), 2):
                hue_min = floor_hue_ranges_list[index]
                hue_max = floor_hue_ranges_list[index+1]
                if hue_max >= hue_value and hue_value >= hue_min:
                    is_floor = True
                if hue_max >= hue_value + 360 and hue_value + 360 >= hue_min:
                    is_floor = True 
            if is_floor:
                cnt += 1
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
    return cnt


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
