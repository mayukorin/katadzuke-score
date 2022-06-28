from statistics import median
import numba, base64, cv2, math, cloudinary
import numpy as np


@numba.jit
def cnt_floor_cnt_of_pixels(hsv):
    cnt = 0
    for h in range(hsv.shape[0]):
        for w in range(hsv.shape[1]):
            # print(hsv[h, w, 0])
            if 17 >= hsv[h, w, 0] and hsv[h, w, 0] >= 14:
                cnt += 1
    return cnt


def calc_percent_of_floors(base64_img):

    np_upload_room_photo = np.asarray(
        bytearray(base64.b64decode(base64_img.split(",")[1])), dtype="uint8"
    )
    img = cv2.imdecode(np_upload_room_photo, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print("ここまで")

    total_cnt_of_pixels = hsv.shape[0] * hsv.shape[1]
    floor_cnt_of_pixels = cnt_floor_cnt_of_pixels(hsv)

    return math.floor(floor_cnt_of_pixels / total_cnt_of_pixels * 100)


def upload_room_photo_to_cloudinary(base64Content):

    response = cloudinary.uploader.upload(file=base64Content)

    return response["public_id"], response["url"]


def destroy_room_photo_from_cloudinary(photo_public_id):

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
