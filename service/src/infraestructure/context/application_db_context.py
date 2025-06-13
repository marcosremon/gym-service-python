from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from src.service.configuration.config import load_db_config

Base = declarative_base()

class ApplicationDbContext:
    def __init__(self):
        config = load_db_config()
        database_url = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['name']}"
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        return self.SessionLocal()