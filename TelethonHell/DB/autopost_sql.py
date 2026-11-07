
import threading

from sqlalchemy import Column, String

from TelethonHell.DB import BASE, SESSION


class Post(BASE):
    __tablename__ = "post"

    target_chat_id = Column(String(14), primary_key=True)
    to_post_chat_id = Column(String(14), primary_key=True, nullable=False)

    def __init__(self, target_chat_id, to_post_chat_id):
        self.to_post_chat_id = str(to_post_chat_id)
        self.target_chat_id = str(target_chat_id)

    def __repr__(self):
        return "<Auto post filter '%s' for %s>" % (
            self.target_chat_id,
            self.to_post_chat_id,
        )

    def __eq__(self, other):
        return bool(
            isinstance(other, Post)
            and self.target_chat_id == other.target_chat_id
            and self.to_post_chat_id == other.to_post_chat_id
        )


Post.__table__.create(checkfirst=True)


POST_FILTER_INSERTION_LOCK = threading.RLock()

CHAT_POSTS = {}


def add_post(target_chat_id: str, to_post_chat_id: str):
    target_chat_id = str(target_chat_id)
    to_post_chat_id = str(to_post_chat_id)

    with POST_FILTER_INSERTION_LOCK:
        try:
            blacklist_filt = Post(
                target_chat_id,
                to_post_chat_id,
            )

            SESSION.merge(blacklist_filt)
            SESSION.commit()

            CHAT_POSTS.setdefault(target_chat_id, set()).add(
                to_post_chat_id
            )

            return True

        except Exception:
            SESSION.rollback()
            raise

        finally:
            SESSION.close()


def get_all_post(target_chat_id: str):
    return CHAT_POSTS.get(str(target_chat_id), set())


def is_post(target_chat_id, to_post_chat_id):
    target_chat_id = str(target_chat_id)
    to_post_chat_id = str(to_post_chat_id)

    with POST_FILTER_INSERTION_LOCK:
        try:
            broadcast_group = (
                SESSION.query(Post)
                .filter(
                    Post.target_chat_id == target_chat_id,
                    Post.to_post_chat_id == to_post_chat_id,
                )
                .first()
            )

            return bool(broadcast_group)

        except Exception:
            SESSION.rollback()
            raise

        finally:
            SESSION.close()


def remove_post(target_chat_id, to_post_chat_id):
    target_chat_id = str(target_chat_id)
    to_post_chat_id = str(to_post_chat_id)

    with POST_FILTER_INSERTION_LOCK:
        try:
            blacklist_filt = (
                SESSION.query(Post)
                .filter(
                    Post.target_chat_id == target_chat_id,
                    Post.to_post_chat_id == to_post_chat_id,
                )
                .first()
            )

            if not blacklist_filt:
                return False

            SESSION.delete(blacklist_filt)
            SESSION.commit()

            posts = CHAT_POSTS.get(target_chat_id, set())
            posts.discard(to_post_chat_id)

            if not posts:
                CHAT_POSTS.pop(target_chat_id, None)

            return True

        except Exception:
            SESSION.rollback()
            raise

        finally:
            SESSION.close()


def __load_chat_channels():
    global CHAT_POSTS

    try:
        all_filters = SESSION.query(Post).all()

        CHAT_POSTS = {}

        for item in all_filters:
            CHAT_POSTS.setdefault(
                item.target_chat_id,
                set(),
            ).add(item.to_post_chat_id)

        return CHAT_POSTS

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


__load_chat_channels()
