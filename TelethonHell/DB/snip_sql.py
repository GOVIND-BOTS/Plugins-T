from sqlalchemy import Column, Numeric, UnicodeText

from TelethonHell.DB import BASE, SESSION


class Note(BASE):
    __tablename__ = "snip"

    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, keyword, reply, f_mesg_id):
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id


Note.__table__.create(checkfirst=True)


def get_note(keyword):
    try:
        return (
            SESSION.query(Note)
            .filter(Note.keyword == keyword)
            .first()
        )

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()


def get_notes():
    try:
        return SESSION.query(Note).all()

    except Exception:
        SESSION.rollback()
        return []

    finally:
        SESSION.close()


def add_note(keyword, reply, f_mesg_id):
    try:
        existing = (
            SESSION.query(Note)
            .filter(Note.keyword == keyword)
            .first()
        )

        if existing:
            existing.reply = reply
            existing.f_mesg_id = f_mesg_id
            SESSION.commit()
            return False

        adder = Note(keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def rm_note(keyword):
    try:
        rem = (
            SESSION.query(Note)
            .filter(Note.keyword == keyword)
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
