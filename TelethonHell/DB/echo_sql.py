
from sqlalchemy import Column, String

from TelethonHell.DB import BASE, SESSION


class ECHOSQL(BASE):
    __tablename__ = "echo_sql"

    user_id = Column(String(14), primary_key=True)
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, user_id, chat_id):
        self.user_id = str(user_id)
        self.chat_id = str(chat_id)


ECHOSQL.__table__.create(checkfirst=True)


def is_echo(user_id, chat_id):
    try:
        return (
            SESSION.query(ECHOSQL)
            .filter(
                ECHOSQL.user_id == str(user_id),
                ECHOSQL.chat_id == str(chat_id),
            )
            .first()
        )

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()


def get_all_echos():
    try:
        return SESSION.query(ECHOSQL).all()

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()


def addecho(user_id, chat_id):
    try:
        adder = ECHOSQL(str(user_id), str(chat_id))

        SESSION.merge(adder)
        SESSION.commit()

        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def remove_echo(user_id, chat_id):
    try:
        note = (
            SESSION.query(ECHOSQL)
            .filter(
                ECHOSQL.user_id == str(user_id),
                ECHOSQL.chat_id == str(chat_id),
            )
            .first()
        )

        if not note:
            return False

        SESSION.delete(note)
        SESSION.commit()

        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()
