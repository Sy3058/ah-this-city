from sqlalchemy import Column, String, INT, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Score_table(Base):
    __tablename__ = 'score_table'

    Location = Column(TEXT, nullable=False, primary_key=True)
    Edu = Column(INT, nullable=False)
    Env = Column(INT, nullable=False)
    Med = Column(INT, nullable=False)
    Saf = Column(INT, nullable=False)
    Tot = Column(INT, nullable=False)


