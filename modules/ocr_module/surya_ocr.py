from PIL import Image
from surya.ocr import run_ocr
from surya.model.detection.model import load_model as load_detection_model, load_processor as load_detection_processor
from surya.model.recognition.model import load_model as load_recognition_model
from surya.model.recognition.processor import load_processor as load_recognition_processor
from typing import List, Any

class SuryaModel:
    def __init__(self):
        self.det_model = load_detection_model()
        self.det_processor = load_detection_processor()
        self.rec_model = load_recognition_model()
        self.rec_processor = load_recognition_processor()
    
        self.det_model.eval()
        self.rec_model.eval()

    def generate_predictions(self, images=List[Image.Image], langs: List[str] = ['en', 'vi']):
        return run_ocr(images=images, langs=[langs], det_model=self.det_model, det_processor=self.det_processor, rec_model=self.rec_model, rec_processor=self.rec_processor), [img.size for img in images]


