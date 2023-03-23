from data.db_loader import Base, engine


async def create_db():
    """Создание БД и наполнение ее предустановленными данными."""
    Base.metadata.create_all(engine)
