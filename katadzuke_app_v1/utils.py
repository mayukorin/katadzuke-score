import base64, cv2, math, cloudinary, numba, numpy as np

@numba.jit
def calc_percent_of_floors_of_photo(base64_content, floor_hue_ranges_list):

        np_img = np.asarray(
            bytearray(base64.b64decode(base64_content.split(",")[1])), dtype="uint8"
        )
        hsv = cv2.cvtColor(cv2.imdecode(np_img, cv2.IMREAD_COLOR), cv2.COLOR_BGR2HSV)

        total_num_of_floor_pixels = 0
        for h in range(hsv.shape[0]):
            for w in range(hsv.shape[1]):
                hue_value = hsv[h, w, 0]
                
                for i in range(0, len(floor_hue_ranges_list), 2):
                    min_hue = floor_hue_ranges_list[i]
                    max_hue = floor_hue_ranges_list[i+1]
                    
                    if max_hue >= hue_value and hue_value >= min_hue:
                        total_num_of_floor_pixels += 1
                    elif max_hue >= hue_value + 360 and hue_value + 360 >= min_hue:
                        total_num_of_floor_pixels += 1
        
        total_num_of_pixels = hsv.shape[0] * hsv.shape[1]

        return math.floor(total_num_of_floor_pixels / total_num_of_pixels * 100)

def upload_photo_to_cloudinary(base64_content):

    response = cloudinary.uploader.upload(file=base64_content)

    return response["public_id"], response["url"]


def destroy_photo_from_cloudinary(photo_public_id):

    cloudinary.uploader.destroy(photo_public_id)


def replace_current_cloudinary_photo_with_posted_photo(public_id_of_current_cloudinary_photo, base64_content_of_posted_photo):

    if public_id_of_current_cloudinary_photo is not None:
        destroy_photo_from_cloudinary(photo_public_id=public_id_of_current_cloudinary_photo)

    public_id_of_photo_uploaded_to_cloudinary, url_of_photo_uploaded_to_cloudinary = upload_photo_to_cloudinary(
        base64_content=base64_content_of_posted_photo
    )

    return public_id_of_photo_uploaded_to_cloudinary, url_of_photo_uploaded_to_cloudinary
