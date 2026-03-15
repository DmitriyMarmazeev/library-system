import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

load_dotenv()

# Импортируем все модели для автогенерации
from app.core.database import Base
from app.modules.users.models import User, Role
from app.modules.books.models import Book, Author, Genre
from app.modules.copies.models import Copy
from app.modules.loans.models import Loan

config = context.config

# Переопределяем URL из переменных окружения
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/library_db"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()