import cv2
import json
from PIL import Image


def make_request_with_retry(model, imgs_list, prompt, max_attempts=5):
    for attempt in range(1, max_attempts + 1):
        try: 
            response = model.generate_output(imgs_list=imgs_list, prompt=prompt)
            return response
        except:
            print(f"There are some errors when calling API, retrying {attempt+1}...")


def visualize(imgs, temp_dict):
    result_dct = {}
    for key in temp_dict:
        if isinstance(temp_dict[key], dict):
            result_dct[key], imgs = visualize(imgs, temp_dict[key])
        elif isinstance(temp_dict[key], list):
            result_dct[key] = []
            for i in range(len(temp_dict[key])):
                res, imgs = visualize(imgs, temp_dict[key][i])
                result_dct[key].append(res)
        elif temp_dict[key] is None:
            result_dct[key] = None
        else:
            result_dct[key] = temp_dict[key].split('||')[0].strip()
            title = key
            bbox_coordinate = json.loads(temp_dict[key].split('||')[1].strip())
            x0, y0, x1, y1 = bbox_coordinate
            idx = int(temp_dict[key].split('||')[2].strip())
            cv2.rectangle(imgs[idx-1], (int(x0), int(y0)), (int(x1), int(y1)), (0,255,0), 2)
            cv2.putText(imgs[idx-1], title, (int(x0), int(y0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
            

    return result_dct, imgs