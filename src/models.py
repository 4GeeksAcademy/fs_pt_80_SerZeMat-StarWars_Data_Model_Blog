import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Users Table
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    first_name = Column(String(80))
    last_name = Column(String(80))

    # Relationship with favorites
    favorites = relationship('Favorite', back_populates='user')

# Planets Table
class Planets(Base):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    climate = Column(String(80))
    terrain = Column(String(80))
    population = Column(Integer)

    # Relationship with favorites
    favorites = relationship('Favorite', back_populates='planet')
    categories = relationship('Category', secondary='planets_categories', back_populates='planets')
    characters = relationship('Characters', back_populates='home_planet')

# Character Table
class Characters(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    species = Column(String(50))
    gender = Column(String(50))
    bitrh_date = Column(String(50))
    home_planet_id = Column(Integer, ForeignKey('planets.id'))


    # Relationship with favorites
    favorites = relationship('Favorite', back_populates='character')
    categories = relationship('Category', secondary='character_categories', back_populates='character')
    home_planet =relationship('Planets', back_populates='character')


# Favorites Table (Intermidiate)
class Favorites(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    usuer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    planet_id = Column(Integer, ForeignKey('planets.id'), nullable=True)
    chatacter_id = Column(Integer, ForeignKey('character.id'), nullable=True)

    # Relationship
    user = relationship('User', back_populates='favorites')
    planet = relationship('Planet', back_populates='favorites')
    character = relationship('Character', back_populates='favorites')

    # Category Table
class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)

    # Relationship
    planets = relationship('Planet', secondary='planets_categories', back_populates='categories')
    character = relationship('Character', secondary='character_categories', back_populates='categories')

# Intermidiate Table for Planets and Categories
planets_categories = Table(
    'planets_categories',
    Base.metadata,
    Column('planet_id', Integer, ForeignKey('planets.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

# Intermidiate Table for Characters and Categories
character_categories = Table(
    'character_categories',
    Base.metadata,
    Column('character_id', Integer, ForeignKey('character.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)


## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
