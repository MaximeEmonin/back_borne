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
    password: str


class UserBase(BaseModel):
    name: str
    role: str


class UserCreate(UserBase):
    id: int


class User(UserBase):

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

    class Config:
        orm_mode = True


class ImageBase(BaseModel):
    id: int
    data: str


class ImageCreate(ImageBase):
    ...


class Image(ImageBase):

    class Config:
        orm_mode = True


class IngredientBase(BaseModel):
    recipe_id: int
    bib_id: int
    amount: int


class IngredientCreate(IngredientBase):
    ...


class Ingredient(IngredientBase):

    class Config:
        orm_mode = True


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
    revoked: bool


class SessionCreate(SessionBase):
    ...


class Session(SessionBase):

    class Config:
        orm_mode = True
