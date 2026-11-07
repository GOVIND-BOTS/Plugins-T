
import time

import heroku3
from HellConfig import Config

from TelethonHell.clients.logger import LOGGER as LOGS


StartTime = time.time()


REQUIRED_VARIABLES = {
    "API_HASH": Config.API_HASH,
    "APP_ID": Config.APP_ID,
    "BOT_TOKEN": Config.BOT_TOKEN,
    "DATABASE_URL": Config.DATABASE_URL,
    "HELLBOT_SESSION": Config.HELLBOT_SESSION,
}


for variable, value in REQUIRED_VARIABLES.items():
    if not value:
        LOGS.warning(
            f"Please fill var {variable} to continue."
        )
        raise SystemExit(1)


HEROKU_APP = None

if Config.HEROKU_API_KEY and Config.HEROKU_APP_NAME:
    try:
        HEROKU_APP = heroku3.from_key(
            Config.HEROKU_API_KEY
        ).apps()[Config.HEROKU_APP_NAME]

        LOGS.info("Heroku configuration loaded.")

    except Exception as e:
        HEROKU_APP = None
        LOGS.warning(
            f"Heroku configuration unavailable: {e}"
        )


# govind sir
