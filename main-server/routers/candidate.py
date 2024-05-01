from base import CreateCandidateRequest
from database import get_db
from sqlalchemy.orm import Session
from datetime import datetime,timedelta
import models
from database import engine
import uuid
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile


router = APIRouter(
  prefix='/candidates',
  tags=['auth']
)

# function and api to create candidate
def create_candidate(db:Session,first_name: str, last_name: str, email: str, unique_identifier:str):
    unique_id = uuid.uuid4()
    last_updated = datetime.utcnow()
    status = "not started"
    candidate= models.Candidate(first_name=first_name,
        last_name=last_name,
        email=email,
        unique_identifier=unique_identifier,
        unique_id=unique_id,
        is_verified=status,
        last_update = last_updated)
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

@router.post("/")
def create_candidate_endpoint(
    request: CreateCandidateRequest,
    db: Session = Depends(get_db)
):
    candidate = create_candidate(
        db=db,
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        unique_identifier=request.unique_identifier
    )
    return {"unique_id": candidate.unique_id}


# function and api to add selfie of candidate
def update_candidate_selfie(db: Session, unique_id: str, new_selfie_path: str):
    candidate = db.query(models.Candidate).filter(models.Candidate.unique_id == unique_id).first()
    if candidate:
        candidate.selfie = new_selfie_path
        candidate.last_update = datetime.utcnow()
        db.commit()
        db.refresh(candidate)
        return candidate
    return None

@router.put("/selfie/")
async def update_candidate_selfie_endpoint(
    unique_id: str = Form(...),
    selfie: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    unique_filename = f"unique/{uuid.uuid4()}-{selfie.filename}"

    with open(unique_filename, "wb") as image_file:
        image_file.write(selfie.file.read())

    updated_candidate = update_candidate_selfie(db, unique_id, unique_filename)

    if updated_candidate:
        return {"message": f"selfie for candidate with unique ID {unique_id} updated successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"Candidate with unique ID {unique_id} not found.")
    
#function and api to add nic_front
def update_candidate_nic_front(db: Session, unique_id: str, new_nic_front_path: str):
    candidate = db.query(models.Candidate).filter(models.Candidate.unique_id == unique_id).first()
    if candidate:
        candidate.nic_front = new_nic_front_path
        candidate.last_update = datetime.utcnow()
        db.commit()
        db.refresh(candidate)
        return candidate
    return None

@router.put("/nic_front/")
async def update_candidate_nic_front_endpoint(
    unique_id: str = Form(...),
    nic_front: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    unique_filename = f"unique/{uuid.uuid4()}-{nic_front.filename}"

    with open(unique_filename, "wb") as image_file:
        image_file.write(nic_front.file.read())

    updated_candidate = update_candidate_nic_front(db, unique_id, unique_filename)

    if updated_candidate:
        return {"message": f"nic_front for candidate with unique ID {unique_id} updated successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"Candidate with unique ID {unique_id} not found.")
    
#function and api to add nic_back
def update_candidate_nic_back(db: Session, unique_id: str, new_nic_back_path: str):
    candidate = db.query(models.Candidate).filter(models.Candidate.unique_id == unique_id).first()
    if candidate:
        candidate.nic_back = new_nic_back_path
        candidate.last_update = datetime.utcnow()
        candidate.is_verified = "submitted"
        db.commit()
        db.refresh(candidate)
        return candidate
    return None

@router.put("/nic_back/")
async def update_candidate_nic_back_endpoint(
    unique_id: str = Form(...),
    nic_back: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    unique_filename = f"unique/{uuid.uuid4()}-{nic_back.filename}"

    with open(unique_filename, "wb") as image_file:
        image_file.write(nic_back.file.read())

    updated_candidate = update_candidate_nic_back(db, unique_id, unique_filename)

    if updated_candidate:
        return {"message": f"nic_back for candidate with unique ID {unique_id} updated successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"Candidate with unique ID {unique_id} not found.")
    
#function and api to add dl_front
def update_candidate_dl_front(db: Session, unique_id: str, new_dl_front_path: str):
    candidate = db.query(models.Candidate).filter(models.Candidate.unique_id == unique_id).first()
    if candidate:
        candidate.dl_front = new_dl_front_path
        candidate.last_update = datetime.utcnow()
        db.commit()
        db.refresh(candidate)
        return candidate
    return None

@router.put("/dl_front/")
async def update_candidate_dl_front_endpoint(
    unique_id: str = Form(...),
    dl_front: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    unique_filename = f"unique/{uuid.uuid4()}-{dl_front.filename}"

    with open(unique_filename, "wb") as image_file:
        image_file.write(dl_front.file.read())

    updated_candidate = update_candidate_dl_front(db, unique_id, unique_filename)

    if updated_candidate:
        return {"message": f"dl_front for candidate with unique ID {unique_id} updated successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"Candidate with unique ID {unique_id} not found.")
    
#function and api to add dl_back
def update_candidate_dl_back(db: Session, unique_id: str, new_dl_back_path: str):
    candidate = db.query(models.Candidate).filter(models.Candidate.unique_id == unique_id).first()
    if candidate:
        candidate.dl_back = new_dl_back_path
        candidate.last_update = datetime.utcnow()
        candidate.is_verified = "submitted"
        db.commit()
        db.refresh(candidate)
        return candidate
    return None

@router.put("/dl_back/")
async def update_candidate_dl_back_endpoint(
    unique_id: str = Form(...),
    dl_back: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    unique_filename = f"Unique/{uuid.uuid4()}-{dl_back.filename}"

    with open(unique_filename, "wb") as image_file:
        image_file.write(dl_back.file.read())

    updated_candidate = update_candidate_dl_back(db, unique_id, unique_filename)

    if updated_candidate:
        return {"message": f"dl_back for candidate with unique ID {unique_id} updated successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"Candidate with unique ID {unique_id} not found.")
    
#function and api to add passport
def update_candidate_passport(db: Session, unique_id: str, new_passport_path: str):
    candidate = db.query(models.Candidate).filter(models.Candidate.unique_id == unique_id).first()
    if candidate:
        candidate.passport = new_passport_path
        candidate.last_update = datetime.utcnow()
        candidate.is_verified = "submitted"
        db.commit()
        db.refresh(candidate)
        return candidate
    return None

@router.put("/passport/")
async def update_candidate_passport_endpoint(
    unique_id: str = Form(...),
    passport: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    unique_filename = f"unique/{uuid.uuid4()}-{passport.filename}"

    with open(unique_filename, "wb") as image_file:
        image_file.write(passport.file.read())

    updated_candidate = update_candidate_passport(db, unique_id, unique_filename)

    if updated_candidate:
        return {"message": f"passport for candidate with unique ID {unique_id} updated successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"Candidate with unique ID {unique_id} not found.")
    
#function and api to return data from candidate table

def get_candidates_info(db: Session):
    candidates = db.query(models.Candidate).all()
    result = []
    for candidate in candidates:
        document_type = None
        if candidate.nic_front:
            document_type = "ID Card"
        elif candidate.dl_front:
            document_type = "Driving License"
        elif candidate.passport:
            document_type = "Passport"
        candidate_info = {
            "first_name": candidate.first_name,
            "last_name": candidate.last_name,
            "is_verified": candidate.is_verified,
            "last_update": candidate.last_update.strftime('%Y-%m-%d %H:%M:%S') if candidate.last_update else None,
            "country": candidate.country,
            "document_type": document_type,
            "unique_id": candidate.unique_id
        }
        result.append(candidate_info)
    return result

@router.get("/info/", response_model=dict)
async def read_candidates(db: Session = Depends(get_db)):
    candidate_info_list = get_candidates_info(db)
    result = {"candidates": candidate_info_list}
    return result

#functions and apis to get and update each candidate info through manual verification
def get_candidate_info(db:Session, unique_id:str):
    candidate = db.query(models.Candidate).filter(models.Candidate.unique_id == unique_id).first()
    if candidate:
        document_type = None
        if candidate.nic_front:
            document_type = "ID Card"
        elif candidate.dl_front:
            document_type = "Driving License"
        elif candidate.passport:
            document_type = "Passport"
        info = {
            'first_name': candidate.first_name,
            'last_name': candidate.last_name,
            'email': candidate.email,
            'selfie': candidate.selfie,
            'document_front': candidate.nic_front or candidate.dl_front or candidate.passport,
            'document_back': candidate.nic_back or candidate.dl_back,
            'is_verified': candidate.is_verified,
            'is_document_tempered': candidate.is_document_tempered,
            'is_not_matching_pics': candidate.is_not_matching_pics,
            'is_spoof_picture': candidate.is_spoof_picture,
            'document_type': document_type,
        }

        return info
    else:
        return None
    
@router.get("/get_candidate_info/{unique_id}")
async def read_candidate_info(unique_id: str, db: Session = Depends(get_db) ):
    print(unique_id)
    candidate_info = get_candidate_info(db,unique_id)
    if candidate_info:
        return candidate_info
    else:
        raise HTTPException(status_code=404, detail="Candidate not found")