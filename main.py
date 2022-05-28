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


@app.get('/recipes', response_model=list[schemas.Recipe])
def get_recipes(alcool: bool, db: Session = Depends(get_db)):
    """ Send all feasible recipes """
    recipes = crud.get_recipes(db)
    if not alcool:
        new_recipes = []
        for recipe in recipes:
            adding = True
            for ingredient in recipe.ingredients:
                if ingredient.bib.alcool:
                    adding = False
                    break
            if adding:
                new_recipes.append(recipe)
        return new_recipes
    return recipes

