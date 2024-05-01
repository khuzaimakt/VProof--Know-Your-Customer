from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal, get_db
from models import User, Company
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
  prefix='/auth',
  tags=['auth']
)
SECRET_KEY = 'ca8ec18938b7f9c283c931193934cb943aacabb272837c4a0ad4922c1ab6a62aa364e4c4bea292e81e31869ab145220d66e0efe016f3274b9c9cbdee26c85ed2'
ALGORITHM =  'HS256'
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl = 'auth/token')

class CreateUserRequest(BaseModel):
  username: str
  name: str
  email: str
  password: str
  company_name: str
class Token(BaseModel):
  access_token: str
  token_type: str

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
  create_company_modal = Company(
    name=create_user_request.company_name
  )
  db.add(create_company_modal)
  db.commit()
  create_user_model = User(
    username=create_user_request.username,
    hashed_password=bcrypt_context.hash(create_user_request.password),
    email=create_user_request.email,
    name=create_user_request.name,
    is_verified=False,
    rid=1,
    cid=create_company_modal.cid
  )
  db.add(create_user_model)
  db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
  user = authenticate_user(form_data.username, form_data.password, db)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user!')
  token = create_access_token(user.username, user.uid, timedelta(minutes=20))
  return {'access_token': token, 'token_type': 'bearer'}

def authenticate_user(username: str, password: str, db):
  user = db.query(User).filter(User.username==username).first()
  if not user:
    return False
  if not bcrypt_context.verify(password, user.hashed_password):
    return False
  return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
  encode = {'sub': username, 'id': user_id}
  expires = datetime.utcnow() + expires_delta
  encode.update({'exp': expires})
  return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    username: str = payload.get('sub')
    user_id: int = payload.get('id')

    if (username is None or user_id is None):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    return {'username': username, 'id': user_id}
  except JWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get('jti')
        if jti:
            # Add the token to the blacklist (you may want to use a database for this in production)
            blacklisted_token = BlacklistedToken(jti=jti)
            db.add(blacklisted_token)
            db.commit()
        return {'message': 'User logged out successfully'}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
