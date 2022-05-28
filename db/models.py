from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table, Boolean, Float
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)


class Bib(Base):
    __tablename__ = "bibs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    alcool = Column(Boolean, nullable=False)


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    price = Column(Float, index=True)

    image = relationship("Image", back_populates="recipe", uselist=False)
    ingredients = relationship("Ingredient")
    author = relationship("User")


class Ingredient(Base):
    __tablename__ = "ingredients"
    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    bib_id = Column(Integer, ForeignKey('bibs.id'), primary_key=True)
    amount = Column(Integer, primary_key=True)

    bib = relationship("Bib")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))

    recipe = relationship("Recipe", back_populates="image")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), index=True)
    price = Column(Integer, index=True)
    date = Column(DateTime, index=True)
    consumer_id = Column(Integer, ForeignKey("users.id"), index=True)

    consumer = relationship("User")
    recipe = relationship("Recipe")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    max_date = Column(DateTime, index=True)

    user = relationship("User")


class LoadedBib(Base):
    __tablename__ = "loaded_bibs"

    id = Column(Integer, primary_key=True, index=True)
    bib_id = Column(Integer, ForeignKey("bibs.id"), index=True)
    amount = Column(Integer, index=True)

    bib = relationship("Bib")
