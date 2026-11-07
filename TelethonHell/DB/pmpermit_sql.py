from sqlalchemy import Column, String

from TelethonHell.DB import BASE, SESSION


class PMPermit(BASE):
    __tablename__ = "pmpermit"

    chat_id = Column(String(14), primary_key=True)
    reason = Column(String(127))

    def __init__(self, chat_id, reason=""):
        self.chat_id = str(chat_id)
        self.reason = reason


PMPermit.__table__.create(checkfirst=True)


def is_approved(chat_id):
    try:
        return (
            SESSION.query(PMPermit)
            .filter(PMPermit.chat_id == str(chat_id))
            .first()
        )

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()


def approve(chat_id, reason):
    try:
        adder = PMPermit(str(chat_id), str(reason))
        SESSION.merge(adder)
        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def disapprove(chat_id):
    try:
        rem = (
            SESSION.query(PMPermit)
            .filter(PMPermit.chat_id == str(chat_id))
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


def get_all_approved():
    try:
        return SESSION.query(PMPermit).all()

    except Exception:
        SESSION.rollback()
        return []

    finally:
        SESSION.close()
