from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # Абсолютный импорт

# Определяем таблицу "Услуги"
class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    working_hours = Column(String)  # Добавляем поле working_hours
    appointments = relationship("Appointment", back_populates="service")

# Определяем таблицу "Записи"
class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    appointment_time = Column(DateTime, nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)

    service = relationship("Service", back_populates="appointments")

# Определяем таблицу "Пользователи"
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
