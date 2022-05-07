from sqlalchemy.orm import Session
from . import models, schemas


def get_bibs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bib).offset(skip).limit(limit).all()


def create_bib(db: Session, bib: schemas.BibCreate):
    db_bib = models.Bib(**bib.dict())
    db.add(db_bib)
    db.commit()
    db.refresh(db_bib)
    return db_bib


def delete_bib(db: Session, bib_id: int):
    db_bib = db.query(models.Bib).get(bib_id)
    db.delete(db_bib)
    db.commit()
    return db_bib


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).get(user_id)
    db.delete(db_user)
    db.commit()
    return db_user


def get_recipes(db, skip: int = 0, limit: int = 100):
    return db.query(models.Recipe).offset(skip).limit(limit).all()


def create_recipe(db, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def delete_recipe(db, recipe_id: int):
    db_recipe = db.query(models.Recipe).get(recipe_id)
    db.delete(db_recipe)
    db.commit()
    return db_recipe


def get_ingredients(db, skip: int = 0, limit: int = 100):
    return db.query(models.Ingredient).offset(skip).limit(limit).all()


def create_ingredient(db, ingredient: schemas.IngredientCreate):
    db_ingredient = models.Ingredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient


def delete_ingredient(db, recipe_id: int, bib_id: int):
    db_ingredient = db.query(models.Ingredient).get((recipe_id, bib_id))
    db.delete(db_ingredient)
    db.commit()
    return db_ingredient


def get_images(db, skip: int = 0, limit: int = 100):
    return db.query(models.Image).offset(skip).limit(limit).all()


def create_image(db, image: schemas.ImageCreate):
    db_image = models.Image(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_image(db, image_id: int):
    db_image = db.query(models.Image).get(image_id)
    db.delete(db_image)
    db.commit()
    return db_image


def get_orders(db, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()


def delete_order(db, order_id: int):
    db_order = db.query(models.Order).get(order_id)
    db.delete(db_order)
    db.commit()
    return db_order
