from sqlalchemy import Column, String, Integer                     # se importan las abstracciones con las que se trabajaran en el archivo sql

from base import Base

class Article(Base):

    __tablename__ = 'articles'

    id = Column(String, primary_key=True)
    body = Column(String)
    host = Column(String)
    title = Column(String)
    newspaper_uid = Column(String)
    tokens_body = Column(Integer)
    tokens_title = Column(Integer)
    url = Column(String(255), unique= True)

    def __init__(self, uid, body, host, title, newspaper_uid, tokens_body, tokens_title, url):
        self.id = uid
        self.body = body
        self.host = host
        self.title = title
        self. newspaper_uid = newspaper_uid
        self.tokens_body = tokens_body
        self.tokens_title = tokens_title
        self.url = url
