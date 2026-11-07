from sqlalchemy import Column, String

from TelethonHell.DB import BASE, SESSION


class Harem(BASE):
    __tablename__ = "harem"

    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)


Harem.__table__.create(checkfirst=True)


def add_grp(chat_id: str):
    try:
        waifu = Harem(str(chat_id))
        SESSION.merge(waifu)
        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def rm_grp(chat_id: str):
    try:
        waifu = (
            SESSION.query(Harem)
            .filter(Harem.chat_id == str(chat_id))
            .first()
        )

        if not waifu:
            return False

        SESSION.delete(waifu)
        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def get_all_grp():
    try:
        return SESSION.query(Harem).all()

    except Exception:
        SESSION.rollback()
        return []

    finally:
        SESSION.close()


def is_harem(chat_id: str):
    try:
        waifu = (
            SESSION.query(Harem)
            .filter(Harem.chat_id == str(chat_id))
            .first()
        )

        if waifu:
            return str(waifu.chat_id)

        return None

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()
