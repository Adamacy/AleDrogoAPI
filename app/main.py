from uuid import UUID, uuid4
from fastapi import FastAPI, Depends, HTTPException, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from db import Base, SessionLocal, engine
import crud as crud
import schemas as schemas
import models as models
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi.responses import JSONResponse
load_dotenv()

cookie_params = CookieParameters()

app = FastAPI()

Base.metadata.create_all(bind=engine)

SECRET_KEY = os.getenv("SECRET_KEY")

backend = InMemoryBackend[UUID, schemas.SessionData]()


class BasicVerifier(SessionVerifier[UUID, schemas.SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, schemas.SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: schemas.SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verify = BasicVerifier(
    identifier='general_verifier',
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(
        status_code=403, detail="Invalid session")
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


cookie = SessionCookie(
    cookie_name='loginCookie',
    identifier='general_verifier',
    auto_error=True,
    secret_key=SECRET_KEY,
    cookie_params=cookie_params
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials = True,
    allow_origins=[
        'http://localhost:8080'
    ],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type","Set-Cookie"],
    
)

# MySQL Database
PASSWORD = os.getenv("MARIA_PASSWORD")
USERNAME = os.getenv("MARIA_USERNAME")


@app.get("/offers")
def get_offers(db: Session = Depends(get_db)):
    return crud.get_items(db = db)


@app.post("/offer/create", response_model=schemas.Item)
def create_offer(item: schemas.ItemCreate, user_id: int | None = Cookie(default=None), db: Session = Depends(get_db)):
    print(user_id)
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get('/offer/search/{query}')
def search_offer(query: str, db: Session = Depends(get_db)):
    return crud.search_offer(query = query, db = db)


@app.post("/user/signin")
async def login_user(user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if crud.verify_password(user.password, db_user.password):
        session = uuid4()
        response.set_cookie("loginCookie", session, expires=14 * 24 * 60 * 60, httponly=True, secure=True, samesite='none')
        response.set_cookie(key='user_id', value=db_user.id, httponly=True, secure=True, samesite='none')
        
        return HTTPException(200, detail="User loged in")
    else:
        return HTTPException(status_code=401, detail="Incorrect password or email address")


@app.post("/user/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_user(db=db, user=user)
    return HTTPException(status_code=201, detail="Account created")


@app.get("/offer/{query}")
def get_offer(query: str, db: Session = Depends(get_db)):
    return crud.take_one_offer(query = query, db = db)