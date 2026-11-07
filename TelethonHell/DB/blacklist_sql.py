
import threading

from sqlalchemy import Column, String, UnicodeText, distinct, func

from TelethonHell.DB import BASE, SESSION


class BlackListFilters(BASE):
    __tablename__ = "blacklist"

    chat_id = Column(String(14), primary_key=True)
    trigger = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, chat_id, trigger):
        self.chat_id = str(chat_id)
        self.trigger = trigger

    def __repr__(self):
        return "<Blacklist filter '%s' for %s>" % (
            self.trigger,
            self.chat_id,
        )

    def __eq__(self, other):
        return bool(
            isinstance(other, BlackListFilters)
            and self.chat_id == other.chat_id
            and self.trigger == other.trigger
        )


BlackListFilters.__table__.create(checkfirst=True)

BLACKLIST_FILTER_INSERTION_LOCK = threading.RLock()
CHAT_BLACKLISTS = {}


def add_to_blacklist(chat_id, trigger):
    chat_id = str(chat_id)

    with BLACKLIST_FILTER_INSERTION_LOCK:
        try:
            blacklist_filt = BlackListFilters(chat_id, trigger)

            SESSION.merge(blacklist_filt)
            SESSION.commit()

            CHAT_BLACKLISTS.setdefault(chat_id, set()).add(trigger)
            return True

        except Exception:
            SESSION.rollback()
            raise

        finally:
            SESSION.close()


def rm_from_blacklist(chat_id, trigger):
    chat_id = str(chat_id)

    with BLACKLIST_FILTER_INSERTION_LOCK:
        try:
            blacklist_filt = (
                SESSION.query(BlackListFilters)
                .filter(
                    BlackListFilters.chat_id == chat_id,
                    BlackListFilters.trigger == trigger,
                )
                .first()
            )

            if not blacklist_filt:
                return False

            SESSION.delete(blacklist_filt)
            SESSION.commit()

            filters = CHAT_BLACKLISTS.get(chat_id, set())
            filters.discard(trigger)

            if not filters:
                CHAT_BLACKLISTS.pop(chat_id, None)

            return True

        except Exception:
            SESSION.rollback()
            raise

        finally:
            SESSION.close()


def get_chat_blacklist(chat_id):
    return CHAT_BLACKLISTS.get(str(chat_id), set())


def num_blacklist_filters():
    try:
        return SESSION.query(BlackListFilters).count()

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def num_blacklist_chat_filters(chat_id):
    try:
        return (
            SESSION.query(BlackListFilters)
            .filter(BlackListFilters.chat_id == str(chat_id))
            .count()
        )

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def num_blacklist_filter_chats():
    try:
        return (
            SESSION.query(
                func.count(distinct(BlackListFilters.chat_id))
            ).scalar()
        )

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def __load_chat_blacklists():
    global CHAT_BLACKLISTS

    try:
        all_filters = SESSION.query(BlackListFilters).all()

        loaded = {}

        for item in all_filters:
            loaded.setdefault(item.chat_id, set()).add(item.trigger)

        with BLACKLIST_FILTER_INSERTION_LOCK:
            CHAT_BLACKLISTS = loaded

        return CHAT_BLACKLISTS

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


__load_chat_blacklists()
