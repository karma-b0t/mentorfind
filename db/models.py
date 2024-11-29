from sqlalchemy import create_engine, Column, Integer, String, Boolean, SmallInteger, TIMESTAMP, Float, BigInteger, ForeignKey, Double, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, aliased
from datetime import datetime
import logging
import os
from decouple import config

# engine = create_engine('postgresql://postgres:123@localhost:5432/infobot')
DATABASE=config('DATABASE')
DB_HOST=config('DB_HOST')

DB_USER=config('DB_USER')
DB_PASSWORD=config('DB_PASSWORD')
DB_PORT=config('DB_PORT')

user=DB_USER                                  
password=DB_PASSWORD
host=DB_HOST
port=DB_PORT
database=DATABASE

DATABASE_URL = (
    f"postgresql://{user}:{password}@{host}:{port}/{database}"
)



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def log_message(message):
    logger.info(f" {message}")

import datetime

# Получаем текущую дату и время
current_datetime = datetime.datetime.now()

# Форматируем дату и время в строку в нужном формате (например, ISO 8601)
current_datetime_str = current_datetime

# Создание базового класса для объявления моделей
Base = declarative_base()

# Определение модели данных пользователя
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    username = Column(String(50), default=None)
    first_name = Column(String(50), default=None)
    last_name = Column(String(50), default=None)
    country = Column(String(50), default=None)
    spesiality = Column(String(50), default=None)
    preferred_languages = Column(String(50), default=None)
    experience_years = Column(SmallInteger, default=None)
    grade = Column(String(50), default='Junior')
    learning_goals = Column(String(250), default=None)
    paid_subscription = Column(Boolean, default=False)
    subscription_duration = Column(SmallInteger, default=None)
    subscription_expiration = Column(TIMESTAMP, default=None)
    mentor_id = Column(Integer, ForeignKey('mentors.id'), nullable=True)
    last_active = Column(TIMESTAMP, default=current_datetime)
    payment_status = Column(Boolean, default=False)
    feedback = Column(Text, default=None)


class Mentor(Base):
    __tablename__ = 'mentors'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    speciality = Column(String(255), nullable=True)
    price = Column(Text, nullable=True)
    contact = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    experience = Column(String(255), nullable=True)
    reviews = Column(Text, nullable=True)
    rating = Column(Float, nullable=True)

    def __str__(self):
        return f'name: {self.name}, speciality:{self.speciality}, price:{self.price}, contact:{self.contact}, description:{self.description}, experience:{self.experience}, reviews:{self.reviews}, rating:{self.rating}'
    