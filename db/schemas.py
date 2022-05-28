from typing import TypedDict

from pydantic import BaseModel
from datetime import datetime


class BibBase(BaseModel):
    name: str
    id: int
    alcool: bool


class BibCreate(BibBase):
    pass


class Bib(BibBase):

    class Config:
        orm_mode = True


class DistantUserBase(BaseModel):
    user: str


class DistantUserLogin(DistantUserBase):
    password: str


class UserBase(BaseModel):
    name: str
    role: str


class UserCreate(UserBase):
    id: int


class User(UserBase):

    class Config:
        orm_mode = True


class ImageBase(BaseModel):
    data: str
    recipe_id: int


class ImageCreate(ImageBase):
    id: int


class Image(ImageBase):

    class Config:
        orm_mode = True


class IngredientBase(BaseModel):
    amount: int


class IngredientCreate(IngredientBase):
    bib_id: int
    recipe_id: int


class Ingredient(IngredientBase):
    bib: Bib

    class Config:
        orm_mode = True


class RecipeBase(BaseModel):
    title: str
    description: str
    author_id: int
    price: float


class RecipeCreate(RecipeBase):
    id: int


class Recipe(RecipeBase):
    ingredients: list[Ingredient]

    class Config:
        orm_mode = True


class RecipesResponse(TypedDict):
    feasible: list[Recipe]
    not_feasible: list[Recipe]


class OrderBase(BaseModel):
    machine_id: str
    recipe_id: int
    price: int
    date: datetime
    consumer_id: int


class OrderCreate(OrderBase):
    ...


class Order(OrderBase):

    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    user_id: int
    max_date: datetime
    token: str


class SessionCreate(SessionBase):
    ...


class Session(SessionBase):

    class Config:
        orm_mode = True


class LoadedBibBase(BaseModel):
    amount: int


class LoadedBibCreate(LoadedBibBase):
    bib_id: int


class LoadedBib(LoadedBibBase):
    bib: Bib

    class Config:
        orm_mode = True


class LoadedBibReplacement(BaseModel):
    old_bib_id: int
    new_bib_type: int
    new_bib_amount: int = 3000
