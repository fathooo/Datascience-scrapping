# se importa sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base   # permite tener acceso a las funcionalidades de ORM ( object relation and mapper), es decir, permite trabajar con objetos de python en vez de df de sql
from sqlalchemy.orm import sessionmaker


#se inicializa sqlalchemy engine

engine = create_engine('sqlite:///newspaper.db')

Session = sessionmaker(bind=engine)

Base = declarative_base()