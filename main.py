import uuid
from datetime import timedelta, datetime
from typing import List, Dict

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine

from dotenv import load_dotenv

from db.schemas import SessionCreate, DistantUserBase, DistantUserLogin, LoadedBibReplacement, Recipe, RecipesResponse
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


@app.get('/recipes', response_model=RecipesResponse)
def get_recipes(alcool: bool, db: Session = Depends(get_db)):
    """ Send all feasible recipes """
    recipes = crud.get_recipes(db)
    loaded_bibs = crud.get_loaded_bibs(db)
    # filter alcool recipes
    if not alcool:
        new_recipes: List[Recipe] = []
        for recipe in recipes:
            adding = True
            for ingredient in recipe.ingredients:
                if ingredient.bib.alcool:
                    adding = False
                    break
            if adding:
                new_recipes.append(recipe)
        recipes = new_recipes
    # filter not feasible recipes because bib not loaded
    new_recipes: list[Recipe] = []
    print('recipes', recipes)
    for recipe in recipes:
        print('checking recipe', recipe.title)
        adding = True
        for ingredient in recipe.ingredients:
            if ingredient.bib.id not in [bib.bib.id for bib in loaded_bibs]:
                adding = False
                break
        if adding:
            new_recipes.append(recipe)
    recipes = new_recipes
    print('recipes', recipes)
    # filter not feasible recipes because not enough amount in bibs
    not_feasible_recipes = []
    feasible_recipes = []
    for recipe in recipes:
        feasible = True
        for ingredient in recipe.ingredients:
            try:
                max_amount = max([loaded_bib.amount for loaded_bib in loaded_bibs if loaded_bib.bib.id == ingredient.bib.id])
            except ValueError:
                max_amount = 0
            if ingredient.amount > max_amount:
                feasible = False
                break
        if feasible:
            feasible_recipes.append(recipe)
        else:
            not_feasible_recipes.append(recipe)
    return {
        "feasible": feasible_recipes,
        "not_feasible": not_feasible_recipes
    }


@app.get('/images/{recipe_id}', response_model=schemas.Image)
def get_image(recipe_id: int, db: Session = Depends(get_db)):
    """ Send image of recipe """
    print(recipe_id)
    image = crud.get_image(db, recipe_id)
    return image


@app.get('/bibs', response_model=list[schemas.Bib])
def get_loaded_bibs(db: Session = Depends(get_db)):
    """ Send all loaded bibs """
    bibs = crud.get_loaded_bibs(db)
    return bibs


@app.post('/bibs/load', response_model=schemas.LoadedBib)
def load_bib(bib_request: schemas.LoadedBibCreate, db: Session = Depends(get_db)):
    """ Load bib """
    bib = crud.create_loaded_bib(db, bib_request.bib_id, bib_request.amount)
    return bib


@app.patch('/bibs/replace', response_model=list[schemas.LoadedBib])
def replace_loaded_bib(replacement: LoadedBibReplacement, db: Session = Depends(get_db)):
    """ Replace loaded bib """
    loaded_bibs = crud.get_loaded_bibs(db)
    bibs = crud.get_bibs(db)
    if replacement.old_bib_id not in map(lambda x: x.bib.id, loaded_bibs):
        raise HTTPException(status_code=404, detail="Bib not found")

    if replacement.new_bib_type not in map(lambda x: x.id, bibs):
        raise HTTPException(status_code=404, detail="Bib type not found")

    crud.delete_loaded_bib(db, replacement.old_bib_id)
    crud.create_loaded_bib(db, replacement.new_bib_type, replacement.new_bib_amount)
    
    return crud.get_loaded_bibs(db)

