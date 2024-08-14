from tap import Tap
from PIL import Image
import numpy as np
import json
import os
import shutil
from utils import *
from config import *
from modules import GeminiAPI, SuryaModel
import torch

torch.set_grad_enabled(False)


llm = GeminiAPI()
surya_model = SuryaModel()
print("Finish Loading Models")


class ArgumentParser(Tap):
    file_path: str = "test_imgs/test_receipt.jpg" #Path to the input file
    output_dir_path: str = "output" #Path to the output directory
    use_ocr: bool = True #Use information from OCR or not
    use_latin: bool = True
    use_visualize: bool = True
    keys: str = "key_template/receipt.txt" #txt file describe desired output (keys that we want to extract)
    save_json_path: str = "running/output.json"




def visualize_main(args):
    #Stage 1: Preprocess input - Create a new folder contains image or images, and return a list contains file paths to those images
    images_path = preprocess_input(args.file_path, args.output_dir_path)
    images = [Image.open(path) for path in images_path]

    #Stage 2: Prepare prompt for LLM
    with open(args.keys, 'r') as f:
        keys = f.read()

    if args.use_ocr:
        preds, img_sizes = surya_model.generate_predictions(images=images, langs=['en'])
        out = process_surya_output(preds)

        if args.use_visualize:
            result = ocr_prompt(out, True)
            prompt = visualize_template.format(keys=keys, ocr_bbox_result = result)
        else:
            if args.use_latin:
                img_sizes = [img.size for img in images]
                result = latin_prompt(out, img_sizes)
                prompt = ocr_latin_template.format(keys=keys, ocr_latin_result = result)
                
            else:
                result = ocr_prompt(out)
                prompt = ocr_template.format(keys=keys, ocr_result = result)
    
    else:
        prompt = non_ocr_template.format(keys=keys)

    response = make_request_with_retry(llm, imgs_list=images, prompt=prompt, max_attempts=3)
    temp_dict = json.loads(response[8:-4])
    #print(temp_dict)
    dic = {}
    imgs = [np.array(img) for img in images]

    if response is None:
        print("Fail when calling API")
    else:
        try:
            temp_dict = json.loads(response[8:-4])
            #print(temp_dict)

            if args.use_visualize:
                with open('running/with_bbox.json', 'w', encoding='utf-8') as f:
                    json.dump(temp_dict, f, ensure_ascii=False)

                dic, imgs = visualize(imgs, temp_dict)
            else:
                dic = temp_dict
            #print(dic)
            
            with open(args.save_json_path, 'w', encoding='utf-8') as f:
                json.dump(dic, f, ensure_ascii=False)
        except:
            print("Convert to JSON fails")
            #print(response[8:-4])       
    


    return dic, imgs





if __name__ == "__main__":
    args = ArgumentParser().parse_args()
    visualize_main(args)