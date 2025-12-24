from logging.config import fileConfig
import sys
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context

# -------------------------------------------------
# Fix Python path ώστε να βλέπει το app/
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

# -------------------------------------------------
# Alembic Config
# -------------------------------------------------
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -------------------------------------------------
# Import settings & Base
# -------------------------------------------------
from app.core.config import settings
from app.db.database import Base

# IMPORTANT:
# Εδώ κάνουμε import ΟΛΑ τα models
# ώστε το autogenerate να τα "δει"
from app.models import user  # noqa: F401

target_metadata = Base.metadata


# -------------------------------------------------
# DB URL από settings (.env)
# -------------------------------------------------
def get_url():
    return settings.DATABASE_URL


# -------------------------------------------------
# Offline migrations
# -------------------------------------------------
def run_migrations_offline():
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------------------------------
# Online migrations
# -------------------------------------------------
def run_migrations_online():
    connectable = engine_from_config(
        {
            "sqlalchemy.url": get_url(),
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
