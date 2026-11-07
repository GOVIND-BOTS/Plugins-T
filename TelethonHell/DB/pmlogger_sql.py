from sqlalchemy import Column, String

from TelethonHell.DB import BASE, SESSION


class PmLogger(BASE):
    __tablename__ = "pmlogger"

    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)


PmLogger.__table__.create(checkfirst=True)


def add_nolog(chat_id: str):
    try:
        chatid = PmLogger(str(chat_id))
        SESSION.merge(chatid)
        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def del_nolog(chat_id: str):
    try:
        chatid = (
            SESSION.query(PmLogger)
            .filter(PmLogger.chat_id == str(chat_id))
            .first()
        )

        if not chatid:
            return False

        SESSION.delete(chatid)
        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def get_all_nolog():
    try:
        return SESSION.query(PmLogger).all()

    except Exception:
        SESSION.rollback()
        return []

    finally:
        SESSION.close()


def is_nolog(chat_id: str):
    try:
        chatid = (
            SESSION.query(PmLogger)
            .filter(PmLogger.chat_id == str(chat_id))
            .first()
        )

        if chatid:
            return str(chatid.chat_id)

        return None

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()
