from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    recipes = relationship("Recipe", back_populates="user")


class Bib(Base):
    __tablename__ = "bibs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    image_id = Column(Integer, ForeignKey("images.id"), nullable=True)

    author = relationship("User", back_populates="recipes")
    image = relationship("Image", back_populates="recipes")
    ingredients = relationship("Ingredient", back_populates="recipe")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, index=True)

    recipe = relationship("Recipe", back_populates="images")


class Ingredient(Base):
    __tablename__ = "ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    bib_id = Column(Integer, ForeignKey("bibs.id"), primary_key=True)
    amount = Column(Integer, index=True)

    recipe = relationship("Recipe", back_populates="ingredients")
    bib = relationship("Bib", back_populates="ingredients")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, ForeignKey("machines.id"), index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), index=True)
    price = Column(Integer, index=True)
    date = Column(DateTime, index=True)
    consumer_id = Column(Integer, ForeignKey("users.id"), index=True)

    recipe = relationship("Recipe", back_populates="orders")
    consumer = relationship("User", back_populates="orders")