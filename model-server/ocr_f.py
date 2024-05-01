import cv2
import easyocr
import subprocess
import os
from roboflow import Roboflow
from ultralytics import YOLO

def run_tesseract(input_image, output_file, language):
    command = [
        "tesseract.exe",
        input_image,
        output_file,
        "-l", language
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Tesseract command executed for {input_image}.")
    except subprocess.CalledProcessError:
        print(f"Error executing Tesseract command for {input_image}.")

def resize_image(image):
    resized_image = cv2.resize(image, (640, 640))
    
    return resized_image

def resize_image_2(image_path, height, width):

    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (width, height))
    cv2.imwrite(image_path, resized_image)


def pre_image(image):

    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grayscale_image



def predict_roi_id_usa(image):
    model = YOLO('models/best_usa_id_m_2.pt')
    results=model.predict(image)
    
    return results


def predict_roi_pp_usa(image):
    model= YOLO('models/best_usa_pp_m_2.pt')
    results=model.predict(image)
    return results

def predict_roi_dl_usa(image):
    model= YOLO('models/best_usa_dl_m_2.pt')
    results=model.predict(image)
    return results

def predict_roi_id_back_usa(image):
    model=YOLO('models/best_us_id_back_m.pt')
    results=model.predict(image)
    return results

def predict_roi_dl_back_usa(image):
    model=YOLO('models/best_us_dl_back.pt')
    results=model.predict(image)
    return results

def predict_roi_id_pak(image):
    model= YOLO('models/best_pak_id_m.pt')
    results=model.predict(image)
    return results

def extract_and_save_region(image_path, x, y, width, height, output_path):
    roi = image_path[y:height,x:width]
    cv2.imwrite(output_path, roi)


def path_generator_id_usa(class_name):
    
    if class_name==0:
        return 'ocr_output/DOB.jpg'
    
    elif class_name==1:
        return 'ocr_output/DOE.jpg'
    
    elif class_name==2:
        return 'ocr_output/GENDER.jpg'

    elif class_name==3:
        return 'ocr_output/IDN.jpg'

    elif class_name==4:
        return 'ocr_output/NAME.jpg'
    
    elif class_name==5:
        return 'ocr_output/SURNAME.jpg'


    
   
def path_generator_pp_usa(class_name):

    if class_name==0:
        return 'ocr_output/DOB.jpg'
    
    elif class_name==1:
        return 'ocr_output/DOE.jpg'
    
    elif class_name==2:
        return 'ocr_output/DOI.jpg'

    elif class_name==3:
        return 'ocr_output/GENDER.jpg'
    
    elif class_name==4:
        return 'ocr_output/NAME.jpg'

    elif class_name==5:
        return 'ocr_output/SURNAME.jpg'
    
    
    
    
def path_generator_dl_usa(class_name):

    if class_name==0:
        return 'ocr_output/DOB.jpg'
    
    elif class_name==1:
        return 'ocr_output/DOE.jpg'
    
    elif class_name==2:
        return 'ocr_output/DOI.jpg'

    elif class_name==3:
        return 'ocr_output/GENDER.jpg'

    elif class_name==4:
        return 'ocr_output/IDN.jpg'
    
    elif class_name==5:
        return 'ocr_output/NAME.jpg'
    
    elif class_name==6:
        return 'ocr_output/SURNAME.jpg'

    

def path_generator_id_back_usa(class_name):

    if class_name==0:
        return 'ocr_output/BC.jpg'
    
    elif class_name==1:
        return 'ocr_output/BF.jpg'
    
    elif class_name==2:
        return 'ocr_output/VC.jpg'
    
    
def path_generator_dl_back_usa(class_name):
    if class_name==0:
        return 'ocr_output/QR.jpg'
    
def path_generator_id_pak(class_name):
    if class_name==0:
        return 'ocr_output/DOB.jpg'
    
    elif class_name==1:
        return 'ocr_output/DOE.jpg'
    
    elif class_name==2:
        return 'ocr_output/DOI.jpg'

    elif class_name==3:
        return 'ocr_output/GENDER.jpg'

    elif class_name==4:
        return 'ocr_output/IDN.jpg'
    
    elif class_name==5:
        return 'ocr_output/NAME.jpg'



def is_empty_file(file_path):
    return os.path.getsize(file_path) == 0

def clear_file_contents(file_path):
    with open(file_path, "w") as file:
        file.truncate(0)