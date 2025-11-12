from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Настройки подключения
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:password@db:5432/mydb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
