from sqlalchemy import Column, String

from TelethonHell.DB import BASE, SESSION


class Sudo(BASE):
    __tablename__ = "sudo"

    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)


Sudo.__table__.create(checkfirst=True)


def in_sudo(chat_id):
    try:
        return (
            SESSION.query(Sudo)
            .filter(Sudo.chat_id == str(chat_id))
            .first()
        )

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()


def add_sudo(chat_id):
    try:
        adder = Sudo(str(chat_id))
        SESSION.merge(adder)
        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def rem_sudo(chat_id):
    try:
        rem = (
            SESSION.query(Sudo)
            .filter(Sudo.chat_id == str(chat_id))
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


def all_sudo():
    try:
        rem = SESSION.query(Sudo).all()
        return rem if rem else 1234

    except Exception:
        SESSION.rollback()
        return 1234

    finally:
        SESSION.close()
