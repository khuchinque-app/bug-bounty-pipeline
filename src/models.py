from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

os.makedirs('data', exist_ok=True)
engine = create_engine('sqlite:///data/pipeline.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class ToolRun(Base):
    __tablename__ = 'tool_runs'
    id = Column(Integer, primary_key=True)
    tool_name = Column(String)
    target = Column(String)
    exit_code = Column(Integer)
    output_path = Column(String)   # path to log file
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Finding(Base):
    __tablename__ = 'findings'
    id = Column(Integer, primary_key=True)
    tool_run_id = Column(Integer)   # ForeignKey
    vulnerability = Column(String)
    severity = Column(String)
    evidence = Column(Text)

Base.metadata.create_all(engine)
