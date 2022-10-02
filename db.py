from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 
from dotenv import load_dotenv
load_dotenv()

PASSWORD = os.getenv("MARIA_PASSWORD")
USERNAME = os.getenv("MARIA_USERNAME")
DATABASE_URL = f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@192.168.0.100:3306/AleDrogo'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()