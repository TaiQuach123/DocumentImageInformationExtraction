import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

generation_config = {'temperature': 0}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

non_ocr_template = """Given an image or a list of images, you need to extract information and return the result in json format with the following keys:

KEYS:
{keys}.

You MUST extract information based on the given keys, DO NOT add any other keys.
"""


ocr_template = """Given an image or a list of images, along with their OCR results:

OCR:
{ocr_result}.

You need to extract information and return the result in json format with the following keys:
KEYS:
{keys}.

Note that you can utilize OCR results to provide better result, but this is only optional, not obligatory.
You MUST extract information based on the given keys, DO NOT add any other keys.
"""


ocr_latin_template = """Given an image or a list of images, along with their OCR results written in LATIN Prompt:

OCR (LATIN Prompt):
{ocr_latin_result}.

You need to extract information and return the result in json format with the following keys:
KEYS:
{keys}.

Note that you can utilize OCR results to provide better result, but this is only optional, not obligatory.
You MUST extract information based on the given keys, DO NOT add any other keys.
"""


visualize_template = """Given an image or a list of images, along with their OCR results including texts and bounding box coordinates. Each image's OCR results separate by the PAGE_i, where i is the number of page.

OCR (text and bounding box coordinate):
{ocr_bbox_result}

You need to extract information and return the result in json format with the following keys:

KEYS:
{keys}.

Utilizing the OCR results to determine the bounding box coordinate and number of page for each piece of information. Information, bounding box coordinate and the page number must be separated by "||".
Example for a key-value pair: "some_key": "some piece of information || [bounding box coordinate] || I".
You MUST extract information based on the given keys, DO NOT add any other keys.
"""
