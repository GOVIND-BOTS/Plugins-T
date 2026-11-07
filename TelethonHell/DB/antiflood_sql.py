
import threading

from sqlalchemy import Column, Integer, String

from TelethonHell.DB import BASE, SESSION


DEF_COUNT = 0
DEF_LIMIT = 0
DEF_OBJ = (None, DEF_COUNT, DEF_LIMIT)


class FloodControl(BASE):
    __tablename__ = "antiflood"

    chat_id = Column(String(14), primary_key=True)
    user_id = Column(Integer, nullable=True)
    count = Column(Integer, default=DEF_COUNT)
    limit = Column(Integer, default=DEF_LIMIT)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)

    def __repr__(self):
        return "<flood control for %s>" % self.chat_id


FloodControl.__table__.create(checkfirst=True)


INSERTION_LOCK = threading.RLock()

CHAT_FLOOD = {}


def set_flood(chat_id, amount):
    chat_id = str(chat_id)
    amount = int(amount)

    with INSERTION_LOCK:
        try:
            flood = (
                SESSION.query(FloodControl)
                .filter(FloodControl.chat_id == chat_id)
                .first()
            )

            if not flood:
                flood = FloodControl(chat_id)

            flood.user_id = None
            flood.count = DEF_COUNT
            flood.limit = amount

            SESSION.add(flood)
            SESSION.commit()

            CHAT_FLOOD[chat_id] = (None, DEF_COUNT, amount)

        except Exception:
            SESSION.rollback()
            raise

        finally:
            SESSION.close()


def update_flood(chat_id: str, user_id) -> bool:
    chat_id = str(chat_id)

    with INSERTION_LOCK:
        if chat_id not in CHAT_FLOOD:
            return False

        curr_user_id, count, limit = CHAT_FLOOD.get(
            chat_id,
            DEF_OBJ,
        )

        if limit == 0:
            return False

        if user_id != curr_user_id or user_id is None:
            CHAT_FLOOD[chat_id] = (
                user_id,
                DEF_COUNT + 1,
                limit,
            )
            return False

        count += 1

        if count > limit:
            CHAT_FLOOD[chat_id] = (
                None,
                DEF_COUNT,
                limit,
            )
            return True

        CHAT_FLOOD[chat_id] = (
            user_id,
            count,
            limit,
        )

        return False


def get_flood_limit(chat_id):
    return CHAT_FLOOD.get(str(chat_id), DEF_OBJ)[2]


def migrate_chat(old_chat_id, new_chat_id):
    old_chat_id = str(old_chat_id)
    new_chat_id = str(new_chat_id)

    with INSERTION_LOCK:
        try:
            flood = (
                SESSION.query(FloodControl)
                .filter(FloodControl.chat_id == old_chat_id)
                .first()
            )

            if flood:
                CHAT_FLOOD[new_chat_id] = CHAT_FLOOD.get(
                    old_chat_id,
                    DEF_OBJ,
                )

                flood.chat_id = new_chat_id
                SESSION.commit()

                CHAT_FLOOD.pop(old_chat_id, None)

        except Exception:
            SESSION.rollback()
            raise

        finally:
            SESSION.close()


def __load_flood_settings():
    global CHAT_FLOOD

    try:
        all_chats = SESSION.query(FloodControl).all()

        CHAT_FLOOD = {
            chat.chat_id: (
                None,
                DEF_COUNT,
                chat.limit,
            )
            for chat in all_chats
        }

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()

    return CHAT_FLOOD
