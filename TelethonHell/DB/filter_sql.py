
from sqlalchemy import Column, LargeBinary, Numeric, String, UnicodeText

from TelethonHell.DB import BASE, SESSION


class Filters(BASE):
    __tablename__ = "filters"

    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True)
    reply = Column(UnicodeText)
    snip_type = Column(Numeric)
    media_id = Column(UnicodeText)
    media_access_hash = Column(UnicodeText)
    media_file_reference = Column(LargeBinary)

    def __init__(
        self,
        chat_id,
        keyword,
        reply,
        snip_type,
        media_id=None,
        media_access_hash=None,
        media_file_reference=None,
    ):
        self.chat_id = str(chat_id)
        self.keyword = keyword
        self.reply = reply
        self.snip_type = snip_type
        self.media_id = media_id
        self.media_access_hash = media_access_hash
        self.media_file_reference = media_file_reference


Filters.__table__.create(checkfirst=True)


def get_filter(chat_id, keyword):
    try:
        return (
            SESSION.query(Filters)
            .filter(
                Filters.chat_id == str(chat_id),
                Filters.keyword == keyword,
            )
            .first()
        )

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()


def get_all_filters(chat_id):
    try:
        return (
            SESSION.query(Filters)
            .filter(Filters.chat_id == str(chat_id))
            .all()
        )

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()


def add_filter(
    chat_id,
    keyword,
    reply,
    snip_type,
    media_id,
    media_access_hash,
    media_file_reference,
):
    try:
        adder = (
            SESSION.query(Filters)
            .filter(
                Filters.chat_id == str(chat_id),
                Filters.keyword == keyword,
            )
            .first()
        )

        if adder:
            adder.reply = reply
            adder.snip_type = snip_type
            adder.media_id = media_id
            adder.media_access_hash = media_access_hash
            adder.media_file_reference = media_file_reference

        else:
            adder = Filters(
                chat_id,
                keyword,
                reply,
                snip_type,
                media_id,
                media_access_hash,
                media_file_reference,
            )

        SESSION.add(adder)
        SESSION.commit()

        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def remove_filter(chat_id, keyword):
    try:
        saved_filter = (
            SESSION.query(Filters)
            .filter(
                Filters.chat_id == str(chat_id),
                Filters.keyword == keyword,
            )
            .first()
        )

        if not saved_filter:
            return False

        SESSION.delete(saved_filter)
        SESSION.commit()

        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def remove_all_filters(chat_id):
    try:
        result = (
            SESSION.query(Filters)
            .filter(Filters.chat_id == str(chat_id))
            .delete(synchronize_session=False)
        )

        SESSION.commit()

        return result > 0

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()
