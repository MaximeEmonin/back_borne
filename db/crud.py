from typing import List

from sqlalchemy.orm import Session
from . import models, schemas
from .schemas import LoadedBib


class BIBException(Exception):
    """
    Exception for BIB errors.
    """
    pass


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


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**(user.dict()))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).get(user_id)
    db.delete(db_user)
    db.commit()
    return db_user


def get_recipes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Recipe]:
    return db.query(models.Recipe).offset(skip).limit(limit).all()


def get_recipe(db: Session, _id: int) -> models.Recipe:
    """ Get a recipe by id """
    return db.query(models.Recipe).get(_id)


def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def delete_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(models.Recipe).get(recipe_id)
    db.delete(db_recipe)
    db.commit()
    return db_recipe


def get_ingredients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ingredient).offset(skip).limit(limit).all()


def create_ingredient(db: Session, ingredient: schemas.IngredientCreate):
    db_ingredient = models.Ingredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient


def delete_ingredient(db: Session, recipe_id: int, bib_id: int):
    db_ingredient = db.query(models.Ingredient).get((recipe_id, bib_id))
    db.delete(db_ingredient)
    db.commit()
    return db_ingredient


def get_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Image).offset(skip).limit(limit).all()


def create_image(db: Session, image: schemas.ImageCreate):
    db_image = models.Image(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_image(db: Session, image_id: int):
    """
    Delete an image.
    """
    db_image = db.query(models.Image).get(image_id)
    db.delete(db_image)
    db.commit()
    return db_image


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    """
    Get all orders.
    """
    return db.query(models.Order).offset(skip).limit(limit).all()


def delete_order(db: Session, order_id: int):
    """
    Delete an order.
    """
    db_order = db.query(models.Order).get(order_id)
    db.delete(db_order)
    db.commit()
    return db_order


def create_session(db: Session, session: schemas.SessionCreate):
    """
    Create a new session.
    """
    db_session = models.Session(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_sessions_by_user(db: Session, user_id: int):
    """
    Get all sessions for a user.
    """
    return db.query(models.Session).filter(models.Session.user_id == user_id).all()


def delete_all_sessions(db: Session, user_name: str):
    """
    Delete all sessions for a user.
    """
    db_user = get_user_by_name(db, user_name)
    db_sessions = get_sessions_by_user(db, db_user.id)
    for db_session in db_sessions:
        db.delete(db_session)
    db.commit()


def get_loaded_bibs(db: Session) -> List[LoadedBib]:
    """ Get all loaded bibs """
    return db.query(models.LoadedBib).all()


def create_loaded_bib(db: Session, bib_id: int, amount: int = 3000):
    """ Create a new loaded_bib object """
    if len(get_loaded_bibs(db)) > 6:
        raise BIBException("There are already 6 loaded bibs. Cannot load more.")

    db_loaded_bib = models.LoadedBib(bib_id=bib_id, amount=amount)
    db.add(db_loaded_bib)
    db.commit()
    db.refresh(db_loaded_bib)
    return db_loaded_bib


def delete_loaded_bib(db: Session, loaded_bib_id: int):
    """ Delete a loaded_bib object """
    db_loaded_bib = db.query(models.LoadedBib).get(loaded_bib_id)
    db.delete(db_loaded_bib)
    db.commit()
    return db_loaded_bib


def get_image(db: Session, recipe_id: int):
    """ Get the image for a recipe. """
    return db.query(models.Image).filter(models.Image.recipe_id == recipe_id).first()


def recipe_set_price(db, recipe_id, price) -> models.Recipe:
    """ Set the price of a recipe """
    db_recipe = db.query(models.Recipe).get(recipe_id)
    db_recipe.price = price
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def recipe_set_title(db, recipe_id, title) -> models.Recipe:
    """ Set the name of a recipe """
    db_recipe = db.query(models.Recipe).get(recipe_id)
    db_recipe.title = title
    db.commit()
    db.refresh(db_recipe)
    return db_recipe
