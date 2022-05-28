import uuid
from datetime import timedelta, datetime

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine

from dotenv import load_dotenv

from db.schemas import SessionCreate, DistantUserBase, DistantUserLogin
from sync import mock_sync_all, sync_all
from fastapi.middleware.cors import CORSMiddleware

import os

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if os.environ["MOCK_DISTANT_API"] == "true":
    sync_all = mock_sync_all


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


sync_all(list(get_db())[0])


@app.post('/login/')
def login(user_request: DistantUserLogin, db: Session = Depends(get_db)):
    """ admin login """
    user = crud.get_user_by_name(db, user_request.user)
    if user is None:
        return {"error": "User not found"}
    token = str(uuid.uuid4())
    # create session and store in db
    session = crud.create_session(db, SessionCreate(
        user_id=user.id,
        token=token,
        max_date=datetime.now() + timedelta(hours=2),
        revoked=False
    ))
    return {"token": session.token}


@app.post('/logout/')
def logout(user: DistantUserBase, db: Session = Depends(get_db)):
    """ admin logout """
    user = crud.delete_all_sessions(db, user.user)

    return {"message": "logged out"}


@app.get('/mock_recipes/')
def get_mock_recipes(db: Session = Depends(get_db)):
    """ Send some mock recipes """
    return [
        {"id": 1, "name": "Mock Recipe 1"},
        {"id": 2, "name": "Mock Recipe 2"},
        {"id": 3, "name": "Mock Recipe 3"},
        {"id": 4, "name": "Mock Recipe 4"},
    ]


@app.get('/recipes', response_model=schemas.Recipe)
def get_recipes(db: Session = Depends(get_db), alcool=True):
    """ Send all feasible recipes """
    recipes = crud.get_recipes(db)
    return recipes


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     """
#     Create a new user
#     """
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)
#
#
# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     """
#     Get all users from the database
#     """
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
#
#
# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     """
#     Get a specific user by id
#     """
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     """
#     Create a new item for a specific user
#     """
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     """
#     Get all items from the database
#     """
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
