from src.application.uses_cases.user_application import UserApplication
from src.infraestructure.context.application_db_context import ApplicationDbContext
from src.infraestructure.persistence.user_repository import UserRepository

def get_user_application():
    db_context = ApplicationDbContext()
    session = db_context.get_session()
    repository = UserRepository(session)
    return UserApplication(repository)