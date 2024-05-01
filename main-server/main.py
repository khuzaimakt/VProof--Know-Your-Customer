from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, create_all_tables
from models import User
from typing import Annotated
from seeder import seed_data
from routers import auth
from routers.auth import get_current_user
from routers import candidate
from utils import create_unique_directory
create_unique_directory()
from pathlib import Path
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
app = FastAPI()
app.include_router(auth.router)
app.include_router(candidate.router)
@app.on_event("startup")
def startup_event():
    create_all_tables()
    seed_data()
# Handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

backend_directory = Path(__file__).parent

# Path to the Unique folder
unique_folder_path = backend_directory / "Unique"


@app.get("/Unique/{image_name}")
async def get_image(image_name: str):
    image_path = unique_folder_path / image_name

    # Check if the file exists
    if not image_path.is_file():
        return {"error": "Image not found"}

    # Use FileResponse to serve the image
    return FileResponse(image_path, media_type="image/jpeg")

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db:db_dependency):
  if user is None:
    raise HTTPException(status_code=401, detail='Authentication Failed')
  return {"User": user}

