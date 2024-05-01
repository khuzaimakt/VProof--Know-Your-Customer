from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from PIL import Image
import cv2
import numpy as np

def predict_live(image_bytes):
    model_face = YOLO('models/best_m_live_2.pt')
    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    spoof_flag = True
    results = model_face.predict(frame, verbose=False)

    for r in results:
        annotator = Annotator(frame.copy())
        boxes = r.boxes.cpu().numpy()

        for box in boxes:
            b = box.xyxy[0].astype(int)
            conf = box.conf
            c = box.cls
            if c != 1:
                    return 0

            elif c == 1 and conf > 0.8:
                return 1
            else:
                return 2