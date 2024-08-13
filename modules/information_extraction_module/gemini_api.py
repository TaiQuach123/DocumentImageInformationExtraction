from config import *
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)

class GeminiAPI:
    def __init__(self, generation_config=generation_config, safety_settings=safety_settings):
        self.gemini_api = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                                                generation_config=generation_config,
                                                safety_settings=safety_settings)
    
    def generate_output(self, prompt, imgs_list):
        new_imgs_list = []
        for img in imgs_list:
            if isinstance(img, Image.Image):
                new_imgs_list.append(img)
            elif isinstance(img, str):
                new_imgs_list.append(Image.open(img))

        response = self.gemini_api.generate_content([prompt, *new_imgs_list])
        return response.text
