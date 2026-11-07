from sqlalchemy import Column, String

from TelethonHell.DB import BASE, SESSION


class Husbando(BASE):
    __tablename__ = "husbando"

    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)


Husbando.__table__.create(checkfirst=True)


def add_hus_grp(chat_id: str):
    try:
        husba = Husbando(str(chat_id))
        SESSION.merge(husba)
        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def rm_hus_grp(chat_id: str):
    try:
        husba = (
            SESSION.query(Husbando)
            .filter(Husbando.chat_id == str(chat_id))
            .first()
        )

        if not husba:
            return False

        SESSION.delete(husba)
        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def get_all_hus_grp():
    try:
        return SESSION.query(Husbando).all()

    except Exception:
        SESSION.rollback()
        return []

    finally:
        SESSION.close()


def is_husb(chat_id: str):
    try:
        husba = (
            SESSION.query(Husbando)
            .filter(Husbando.chat_id == str(chat_id))
            .first()
        )

        if husba:
            return str(husba.chat_id)

        return None

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()
