
from sqlalchemy import BigInteger, Column, Numeric, String, UnicodeText

from TelethonHell.DB import BASE, SESSION


class Welcome(BASE):
    __tablename__ = "welcome"

    chat_id = Column(String(14), primary_key=True)
    previous_welcome = Column(BigInteger)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, chat_id, previous_welcome, reply, f_mesg_id):
        self.chat_id = str(chat_id)
        self.previous_welcome = previous_welcome
        self.reply = reply
        self.f_mesg_id = f_mesg_id


Welcome.__table__.create(checkfirst=True)


def get_welcome(chat_id):
    try:
        return (
            SESSION.query(Welcome)
            .filter(Welcome.chat_id == str(chat_id))
            .first()
        )

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()


def get_current_welcome(chat_id):
    try:
        return (
            SESSION.query(Welcome)
            .filter(Welcome.chat_id == str(chat_id))
            .one_or_none()
        )

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()


def add_welcome(chat_id, previous_welcome, reply, f_mesg_id):
    try:
        chat_id = str(chat_id)

        existing = (
            SESSION.query(Welcome)
            .filter(Welcome.chat_id == chat_id)
            .first()
        )

        if existing:
            existing.previous_welcome = previous_welcome
            existing.reply = reply
            existing.f_mesg_id = f_mesg_id
            SESSION.commit()
            return False

        adder = Welcome(
            chat_id,
            previous_welcome,
            reply,
            f_mesg_id,
        )

        SESSION.add(adder)
        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def rm_welcome(chat_id):
    try:
        rem = (
            SESSION.query(Welcome)
            .filter(Welcome.chat_id == str(chat_id))
            .first()
        )

        if rem:
            SESSION.delete(rem)
            SESSION.commit()
            return True

        return False

    except Exception:
        SESSION.rollback()
        return False

    finally:
        SESSION.close()


def update_welcome(chat_id, previous_welcome):
    try:
        row = (
            SESSION.query(Welcome)
            .filter(Welcome.chat_id == str(chat_id))
            .first()
        )

        if not row:
            return False

        row.previous_welcome = previous_welcome
        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()
