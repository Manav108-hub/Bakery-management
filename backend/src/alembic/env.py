from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
import sys
from pathlib import Path

# Add your project root to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import your SQLAlchemy Base and models
from src.models.models import Base
from src.database import DATABASE_URL

# This is the Alembic Config object, which provides access to the values within alembic.ini
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Set target_metadata to your SQLAlchemy Base.metadata
target_metadata = Base.metadata

def run_migrations_offline():
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # Create an engine using the DATABASE_URL defined in src/database.py
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
