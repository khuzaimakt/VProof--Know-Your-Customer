from pydantic import BaseModel
from fastapi import File, UploadFile
class CreateCandidateRequest(BaseModel):
  first_name: str
  last_name: str
  email: str
  unique_identifier: str
  
class CandidateSelfieRequest(BaseModel):
  nic_front: UploadFile
  unique_id: str
  