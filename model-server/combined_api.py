from fastapi import FastAPI, UploadFile, File, HTTPException
import predict_f
from predict_f import predict_live
from fastapi.responses import JSONResponse
import os
import numpy as np
import cv2
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import easyocr
import ocr_f
import json
import os
import face_matching

app=FastAPI()

origins = ["http://localhost", "http://localhost:3000", "http://127.0.0.1:5500", "http://localhost:3001", "http://192.168.1.26:3001","http://192.168.1.27:30004","http://192.168.1.8:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_directory = 'user_data'
if not os.path.exists(user_directory):
    os.makedirs(user_directory)

if not os.listdir(user_directory):
    pass

else:
    for filename in os.listdir(user_directory):
        file_path = os.path.join(user_directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Error while deleting '{file_path}': {e}")
            
@app.post("/upload_selfie/")
async def upload_selfie(file: UploadFile):

    image_directory = 'ocr_output'
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    if not os.listdir(image_directory):
        pass

    else:
        for filename in os.listdir(image_directory):
            file_path = os.path.join(image_directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Error while deleting '{file_path}': {e}")

    try:
        image_bytes = await file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        image_path= user_directory +'/selfie_image.jpg'
        cv2.imwrite(image_path, frame)
        flag= predict_live(image_bytes)

        if flag==0:
            return {"message": "Spoof Detected"}

        elif flag==1:
            return {"message": "Live Face Detected"}

        elif flag==2:
            return {"message": "No Face Detected"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/upload_front_id/")
async def upload_front_id(file: UploadFile):
    image_directory = 'ocr_output'
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    if not os.listdir(image_directory):
        pass

    else:
        for filename in os.listdir(image_directory):
            file_path = os.path.join(image_directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Error while deleting '{file_path}': {e}")
    
    try:
        image_bytes = await file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        frame= ocr_f.resize_image(frame)
        image_path= user_directory+'/front_image.jpg'
        cv2.imwrite(image_path, frame)
    
        image_path_selfie= user_directory+'/selfie_image.jpg'
        image_path_id= user_directory+'/front_image.jpg'
        output_text = {}
        matching_flag= face_matching.face_matching_similar(image_path_selfie,image_path_id)

        if matching_flag== True:
            output_text['matching_faces']=True
        else:
           output_text['matching_faces']=False

        results = ocr_f.predict_roi_id_pak(frame)

        for r in results:
            boxes=r.boxes.cpu().numpy()
            for box in boxes:
                cls= int(box.cls)
                b= box.xyxy[0].astype(int)
                output_path= ocr_f.path_generator_id_pak(cls)
                ocr_f.extract_and_save_region(frame,b[0],b[1],b[2],b[3],output_path)


        reader = easyocr.Reader(['en'])
        
        
        image_files = [f for f in os.listdir(image_directory) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
                            
            
        for image_file in image_files:
            image_path = os.path.join(image_directory, image_file)
            if image_file=='GENDER.jpg':
                ocr_f.resize_image_2(image_path,75,75)
            result = reader.readtext(image_path)
            detected_text = [entry[1] for entry in result]
            if len(detected_text)!=0:
                image_file = image_file.rsplit('.', 1)[0]
                output_text[image_file]=detected_text[0]
            else:
                image_file = image_file.rsplit('.', 1)[0]
                output_text[image_file]='-'


        return output_text

    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/upload_front_pp/")
async def upload_front_pp(file: UploadFile):

    image_directory = 'ocr_output'
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    if not os.listdir(image_directory):
        pass

    else:
        for filename in os.listdir(image_directory):
            file_path = os.path.join(image_directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Error while deleting '{file_path}': {e}")
    
    try:
        image_bytes = await file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        frame=ocr_f.resize_image(frame)
        image_path= user_directory+'/front_image.jpg'
        cv2.imwrite(image_path, frame)

        image_path_selfie= user_directory+'/selfie_image.jpg'
        image_path_pp= user_directory+'/front_image.jpg'
        output_text={}

        matching_flag= face_matching.face_matching_similar(image_path_selfie,image_path_pp)
        
        if matching_flag== True:
            output_text['matching_faces']=True
        else:
           output_text['matching_faces']=False

        results = ocr_f.predict_roi_pp_usa(frame)
        for r in results:
            boxes=r.boxes.cpu().numpy()
            for box in boxes:
                cls= int(box.cls)
                b= box.xyxy[0].astype(int)
                output_path= ocr_f.path_generator_pp_usa(cls)
                ocr_f.extract_and_save_region(frame,b[0],b[1],b[2],b[3],output_path)


        reader = easyocr.Reader(['en'])
        
        image_files = [f for f in os.listdir(image_directory) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
            
        for image_file in image_files:
            image_path = os.path.join(image_directory, image_file)
            if image_file=='GENDER.jpg':
                ocr_f.resize_image_2(image_path,75,75)
            result = reader.readtext(image_path)
            detected_text = [entry[1] for entry in result]
            if len(detected_text)!=0:
                image_file = image_file.rsplit('.', 1)[0]
                output_text[image_file]=detected_text[0]
            else:
                image_file = image_file.rsplit('.', 1)[0]
                output_text[image_file]='-'

        return output_text
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/upload_front_dl/")
async def upload_front_dl(file: UploadFile):

    image_directory = 'ocr_output'
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    if not os.listdir(image_directory):
        pass

    else:
        for filename in os.listdir(image_directory):
            file_path = os.path.join(image_directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Error while deleting '{file_path}': {e}")
    
    try:
        image_bytes = await file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        frame= ocr_f.resize_image(frame)
        image_path= user_directory+'/front_image.jpg'
        cv2.imwrite(image_path, frame)


        image_path_selfie= user_directory+'/selfie_image.jpg'
        image_path_dl= user_directory+'/front_image.jpg'
        output_text={}

        matching_flag= face_matching.face_matching_similar(image_path_selfie,image_path_dl)
        
        
        if matching_flag== True:
            output_text['matching_faces']=True
        else:
           output_text['matching_faces']=False


        results = ocr_f.predict_roi_dl_usa(frame)

        for r in results:
            boxes=r.boxes.cpu().numpy()
            for box in boxes:
                cls= int(box.cls)
                b= box.xyxy[0].astype(int)
                output_path= ocr_f.path_generator_dl_usa(cls)
                ocr_f.extract_and_save_region(frame,b[0],b[1],b[2],b[3],output_path)


        

        reader = easyocr.Reader(['en'])
        
        
        image_files = [f for f in os.listdir(image_directory) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
            
        for image_file in image_files:
            image_path = os.path.join(image_directory, image_file)
            if image_file=='GENDER.jpg':
                ocr_f.resize_image_2(image_path,70,70)
            result = reader.readtext(image_path)
            detected_text = [entry[1] for entry in result]
            if len(detected_text)!=0:
                image_file = image_file.rsplit('.', 1)[0]
                output_text[image_file]=detected_text[0]
            else:
                image_file = image_file.rsplit('.', 1)[0]
                output_text[image_file]='-'

        return output_text
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload_back_id/")
async def upload_back_id(file: UploadFile):

    image_directory = 'ocr_output'
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    if not os.listdir(image_directory):
        pass

    else:
        for filename in os.listdir(image_directory):
            file_path = os.path.join(image_directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Error while deleting '{file_path}': {e}")
    try:
        image_bytes = await file.read()
            
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        frame= ocr_f.resize_image(frame)
        image_path= user_directory +'/back_image.jpg'
        cv2.imwrite(image_path, frame)

        results = ocr_f.predict_roi_id_back_usa(frame)

        for r in results:
            boxes=r.boxes.cpu().numpy()
            for box in boxes:
                cls= int(box.cls)
                b= box.xyxy[0].astype(int)
                output_path= ocr_f.path_generator_id_back_usa(cls)
                ocr_f.extract_and_save_region(frame,b[0],b[1],b[2],b[3],output_path)

        
        return JSONResponse(content={"message": "File uploaded successfully"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@app.post("/upload_back_dl/")
async def upload_back_dl(file: UploadFile):
    image_directory = 'ocr_output'
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    if not os.listdir(image_directory):
        pass

    else:
        for filename in os.listdir(image_directory):
            file_path = os.path.join(image_directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Error while deleting '{file_path}': {e}")


    try:
        image_bytes = await file.read()
            

        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        frame= ocr_f.resize_image(frame)
        image_path= user_directory +'/back_image.jpg'
        cv2.imwrite(image_path, frame)
        results = ocr_f.predict_roi_dl_back_usa(frame)

        for r in results:
            boxes=r.boxes.cpu().numpy()
            for box in boxes:
                cls= int(box.cls)
                b= box.xyxy[0].astype(int)
                output_path= ocr_f.path_generator_dl_back_usa(cls)
                ocr_f.extract_and_save_region(frame,b[0],b[1],b[2],b[3],output_path)
        
        return JSONResponse(content={"message": "File uploaded successfully"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)