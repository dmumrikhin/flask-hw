from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func 

POSTGRES_DSN = f'postgresql://adverts:secret@127.0.0.1:5431/adverts' #юзер, пароль, адрес, база


engine = create_engine(POSTGRES_DSN)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Adverts(Base):
    
    __tablename__ = 'adverts'

    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(String(70), index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False) 
    creation_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[str] = mapped_column(String(50), nullable=False)

Base.metadata.create_all(bind=engine)  # создаем миграцию



