from data.db_loader import Base, engine
from data.services import fill_notifications


async def create_db():
    """Создание БД и наполнение ее предустановленными данными."""
    Base.metadata.create_all(engine)
    fill_notifications()
