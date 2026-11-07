from sqlalchemy import Column, Numeric, String

from TelethonHell.DB import BASE, SESSION


class forceSubscribe(BASE):
    __tablename__ = "forceSubscribe"

    chat_id = Column(Numeric, primary_key=True)
    channel = Column(String)

    def __init__(self, chat_id, channel):
        self.chat_id = chat_id
        self.channel = channel


forceSubscribe.__table__.create(checkfirst=True)


def is_fsub(chat_id):
    try:
        return (
            SESSION.query(forceSubscribe)
            .filter(forceSubscribe.chat_id == chat_id)
            .first()
        )

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()


def add_fsub(chat_id, channel):
    try:
        adder = (
            SESSION.query(forceSubscribe)
            .filter(forceSubscribe.chat_id == chat_id)
            .first()
        )

        if adder:
            adder.channel = channel
        else:
            adder = forceSubscribe(chat_id, channel)
            SESSION.add(adder)

        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def rm_fsub(chat_id):
    try:
        rem = (
            SESSION.query(forceSubscribe)
            .filter(forceSubscribe.chat_id == chat_id)
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


def all_fsub():
    try:
        return SESSION.query(forceSubscribe).all()

    except Exception:
        SESSION.rollback()
        return []

    finally:
        SESSION.close()
