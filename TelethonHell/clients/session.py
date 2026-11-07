
import sys

from telethon import TelegramClient
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession

from HellConfig import Config


def validate_session(session):
    if not isinstance(session, str):
        raise ValueError("Session must be a string.")

    session = session.strip()

    if not session.lower().startswith("==hell"):
        raise ValueError(
            "Invalid session format. Expected ==hell...bot=="
        )

    if not session.lower().endswith("bot=="):
        raise ValueError(
            "Invalid session format. Expected ==hell...bot=="
        )

    new_session = session[6:-5].strip()

    if not new_session:
        raise ValueError("Session string is empty.")

    return new_session


def create_client(session, name="Hell"):
    try:
        return TelegramClient(
            session=session,
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            connection=ConnectionTcpAbridged,
            auto_reconnect=True,
            connection_retries=None,
        )
    except Exception as e:
        print(f"{name} initialization error: {e}")
        sys.exit(1)


try:
    if Config.HELLBOT_SESSION:
        session = StringSession(
            validate_session(Config.HELLBOT_SESSION)
        )
    else:
        session = "hellbot"

    Hell = create_client(session, "HELL")

except Exception as e:
    print(f"HELLBOT_SESSION ERROR: {e}")
    sys.exit(1)


try:
    if Config.SESSION_2:
        session2 = StringSession(
            validate_session(Config.SESSION_2)
        )
        H2 = create_client(session2, "SESSION_2")
    else:
        H2 = None

    if Config.SESSION_3:
        session3 = StringSession(
            validate_session(Config.SESSION_3)
        )
        H3 = create_client(session3, "SESSION_3")
    else:
        H3 = None

    if Config.SESSION_4:
        session4 = StringSession(
            validate_session(Config.SESSION_4)
        )
        H4 = create_client(session4, "SESSION_4")
    else:
        H4 = None

    if Config.SESSION_5:
        session5 = StringSession(
            validate_session(Config.SESSION_5)
        )
        H5 = create_client(session5, "SESSION_5")
    else:
        H5 = None

except Exception as e:
    print(f"ADDITIONAL SESSION ERROR: {e}")
    sys.exit(1)


try:
    HellBot = create_client("Hell-TBot", "HellBot").start(
        bot_token=Config.BOT_TOKEN
    )
except Exception as e:
    print(f"HELLBOT TOKEN ERROR: {e}")
    sys.exit(1)
