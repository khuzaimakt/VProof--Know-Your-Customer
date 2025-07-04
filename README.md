# VProof - Know Your Customer (KYC)

**VProof** is an AI-powered customer verification application designed to streamline and automate the Know Your Customer (KYC) process. It performs liveness detection, document data extraction, and facial verification to ensure identity authenticity with high accuracy.

## 🔍 Overview

This project includes a modular backend engine built using **FastAPI**, located in the `model-server` directory. It provides the following core functionalities:

1. **Liveness & Anti-Spoofing Detection**
   - Ensures the uploaded selfie is from a real, live person and not a spoof (e.g., photo or video replay).
   - Utilizes **YOLOv8** for real-time face and spoof detection.

2. **Document OCR (Optical Character Recognition)**
   - Extracts key identity information (e.g., name, DOB, ID number) from uploaded documents such as:
     - National ID Cards
     - Passports
     - Driver’s Licenses
   - Uses OCR techniques to convert document images into structured data.

3. **Face Matching / Identity Verification**
   - Compares the user's uploaded selfie with the face image from the identity document.
   - Employs **DLib** facial recognition to confirm both images belong to the same person.

## 🚀 Getting Started

Follow these steps to set up and run the backend server locally.

### Prerequisites

- Python 3.8+
- `git` installed on your machine
- (Optional) `virtualenv` for isolated environment

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/vproof-kyc.git
cd vproof-kyc/model-server

```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```
### 4. Run the FastAPI server
```bash
cd model-server
uvicorn combined_api:app --reload

```

### 5. Run the FastAPI server
```bash
cd model-server
uvicorn main:app --reload
```
Once the server is running navigate to: http://localhost:8000/docs


## 📦 Features

- **Liveness & Anti-Spoofing Detection**  
  Detects whether the uploaded selfie is of a live person and not a spoof (e.g., printed image or screen replay).  
  Implemented using YOLOv8 for real-time face and spoof detection.

- **Document OCR (Optical Character Recognition)**  
  Extracts structured identity information from images of official documents such as ID cards, passports, and driver’s licenses.  
  Useful for automating form filling and data validation processes.

- **Face Matching / Identity Verification**  
  Compares the user’s selfie with the photo extracted from the identity document.  
  Uses DLib’s face recognition to validate if both images are of the same individual.

- **Modular Architecture**  
  Backend is modular and easy to extend. Components like OCR, face detection, and matching can be swapped or upgraded independently.

- **Interactive REST API**  
  Clean and well-documented FastAPI interface with built-in Swagger UI for testing endpoints directly from the browser.

---

## 🛠 Technologies Used

- **[FastAPI](https://fastapi.tiangolo.com/)** – High-performance web framework for building APIs with Python
- **[YOLOv8](https://github.com/ultralytics/ultralytics)** – State-of-the-art object detection model for real-time spoof detection
- **[DLib](http://dlib.net/)** – Machine learning toolkit used for face detection and recognition
- **[Tesseract OCR](https://github.com/tesseract-ocr/tesseract)** – Open-source OCR engine used to extract text from documents
- **OpenCV / Pillow** – Libraries for image processing and preprocessing

---

## ✅ Use Cases

- Remote customer onboarding for banks, fintechs, and e-wallets
- Identity verification for gig economy or ride-sharing apps
- Fraud prevention in online marketplaces
- Automated check-ins and access control for high-security areas
- KYC compliance and verification for crypto platforms

---

## 📌 Future Improvements

- Multilingual OCR and country-specific ID parsing
- Integration with real-time identity verification APIs (e.g., Jumio, Onfido)
- Web frontend or mobile SDK for end-user interaction
- Dockerization for easy deployment
- CI/CD and test coverage for production-readiness

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for full license text.
