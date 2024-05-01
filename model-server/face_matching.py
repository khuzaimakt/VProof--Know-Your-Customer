import dlib
import cv2
import numpy as np

def find_largest_face(faces):
    if not faces:
        return None

    largest_face = max(faces, key=lambda rect: (rect.right() - rect.left()) * (rect.bottom() - rect.top()))
    return largest_face

def face_matching_similar(image1, image2):
    shape_predictor_path = "models/shape_predictor_68_face_landmarks.dat"
    face_landmark_predictor = dlib.shape_predictor(shape_predictor_path)

    face_recognizer_path = "models/dlib_face_recognition_resnet_model_v1.dat"
    face_recognizer = dlib.face_recognition_model_v1(face_recognizer_path)

    image_id_card = cv2.imread(image2)
    image_front_camera = cv2.imread(image1)

    image_id_card_rgb = cv2.cvtColor(image_id_card, cv2.COLOR_BGR2RGB)
    image_front_camera_rgb = cv2.cvtColor(image_front_camera, cv2.COLOR_BGR2RGB)

    face_detector = dlib.get_frontal_face_detector()
    faces_id_card = face_detector(image_id_card_rgb)
    faces_front_camera = face_detector(image_front_camera_rgb)

    if len(faces_front_camera) != 1:
        return False
    
    if len(faces_id_card)== 0 or len(faces_id_card) > 2:
        return False

    largest_face_id_card = find_largest_face(faces_id_card)
    largest_face_front_camera = find_largest_face(faces_front_camera)

    left, top, right, bottom = largest_face_id_card.left(), largest_face_id_card.top(), largest_face_id_card.right(), largest_face_id_card.bottom()
    roi_id_card = image_id_card[top:bottom, left:right]
    


    left, top, right, bottom = largest_face_front_camera.left(), largest_face_front_camera.top(), largest_face_front_camera.right(), largest_face_front_camera.bottom()
    roi_front_camera = image_front_camera[top:bottom, left:right]
    

    landmarks_id_card = face_landmark_predictor(image_id_card_rgb, largest_face_id_card)
    landmarks_front_camera = face_landmark_predictor(image_front_camera_rgb, largest_face_front_camera)

    embedding_id_card = np.array(face_recognizer.compute_face_descriptor(image_id_card_rgb, landmarks_id_card))
    embedding_front_camera = np.array(face_recognizer.compute_face_descriptor(image_front_camera_rgb, landmarks_front_camera))

    cosine_similarity = np.dot(embedding_id_card, embedding_front_camera) / (np.linalg.norm(embedding_id_card) * np.linalg.norm(embedding_front_camera))

    similarity_threshold = 0.9
    if cosine_similarity > similarity_threshold:
        return True
    else:
        return False