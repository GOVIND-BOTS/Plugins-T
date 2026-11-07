
from HellConfig import Config

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool


BASE = declarative_base()
SESSION = None
ENGINE = None


def start() -> scoped_session:
    global ENGINE

    if not Config.DATABASE_URL:
        raise ValueError("DATABASE_URL is not configured.")

    database_url = Config.DATABASE_URL.strip()

    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1,
        )

    ENGINE = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_recycle=300,
        poolclass=NullPool,
        connect_args={
            "connect_timeout": 15,
        },
    )

    BASE.metadata.bind = ENGINE
    BASE.metadata.create_all(ENGINE)

    return scoped_session(
        sessionmaker(
            bind=ENGINE,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
    )


try:
    SESSION = start()

except Exception as e:
    print(
        "DATABASE_URL connection failed. "
        "Database-dependent features may not work."
    )
    print(f"Database error: {e}")
    raise
