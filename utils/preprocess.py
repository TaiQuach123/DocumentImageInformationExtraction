from PIL import Image
import os
import pdf2image
import shutil

def process_surya_output(output):
    pages = []
    for out in output: #(each out correspond to ocr result of each image)
        page = []
        for text_line in out.text_lines:
            page.append({'text': text_line.text, 'bbox': text_line.bbox})
        pages.append(page)
    
    return pages

def resize_image_with_ratio(img, new_w=1028):
    if isinstance(img, str):
        img = Image.open(img)
    w, h = img.size

    if new_w > w:
        return img
    
    aspect_ratio = w / h
    new_h = int(new_w / aspect_ratio)
    return img.resize((new_w, new_h))

def ocr_prompt(pages, include_bbox = False):
    res = ''
    if include_bbox:
        for i, page in enumerate(pages):
            res += '-'*20 + f'PAGE {i+1}' + '-'*20 + '\n'
            for textline in page:
                res += textline['text'] + '\t' + str(textline['bbox']) + '\n'
    else:
        for i, page in enumerate(pages):
            res += '-'*20 + f'PAGE {i+1}' + '-'*20 + '\n'
            for textline in page:
                res += textline['text'] + '\n'
            
    return res





def preprocess_pdf_input(pdf_path: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)
    return pdf2image.convert_from_path(
        pdf_path, 
        dpi=200,
        output_folder=output_folder,
        fmt="jpg",
        paths_only=True
    )

def preprocess_input(file_path: str, output_dir: str):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    if file_path.endswith('.pdf'):
        images_path = preprocess_pdf_input(file_path, output_dir)
    else:
        os.makedirs(output_dir)
        new_img_path = os.path.join(output_dir, 'image.jpg')
        Image.open(file_path).save(new_img_path)
        images_path = [new_img_path]

    return images_path
