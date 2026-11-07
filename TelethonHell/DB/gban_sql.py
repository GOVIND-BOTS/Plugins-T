from sqlalchemy import Column, String

from TelethonHell.DB import BASE, SESSION


class GBan(BASE):
    __tablename__ = "gban"

    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)


GBan.__table__.create(checkfirst=True)


def is_gbanned(chat_id):
    try:
        return (
            SESSION.query(GBan)
            .filter(GBan.chat_id == str(chat_id))
            .first()
        )

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()


def gbaner(chat_id):
    try:
        adder = GBan(str(chat_id))
        SESSION.merge(adder)
        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def ungbaner(chat_id):
    try:
        rem = (
            SESSION.query(GBan)
            .filter(GBan.chat_id == str(chat_id))
            .first()
        )

        if not rem:
            return False

        SESSION.delete(rem)
        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def all_gbanned():
    try:
        return SESSION.query(GBan).all()

    except Exception:
        SESSION.rollback()
        return []

    finally:
        SESSION.close()
