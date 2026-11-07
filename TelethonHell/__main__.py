
import glob
import sys
from pathlib import Path

from HellConfig import Config

from TelethonHell.clients.logger import LOGGER as LOGS
from TelethonHell.clients.session import H2, H3, H4, H5, Hell, HellBot
from TelethonHell.utils.plug import load_module, plug_channel
from TelethonHell.utils.startup import (
    join_it,
    logger_check,
    start_msg,
    update_sudo,
)
from TelethonHell.version import __hellver__


# Global Variables #
HELL_PIC = "https://te.legra.ph/file/978c82569c1886a27e991.jpg"


# Client Starter
async def hells(session=None, client=None, session_name="Main"):
    if not session or client is None:
        return 0

    LOGS.info(f"••• Starting Client [{session_name}] •••")

    try:
        await client.start()
        LOGS.info(f"••• {session_name} Started Successfully •••")
        return 1

    except Exception as e:
        LOGS.error(f"Error starting {session_name}: {e}")
        return 0


# Load plugins based on config UNLOAD
async def plug_load(path):
    files = sorted(glob.glob(path))

    if not files:
        LOGS.warning(f"No plugins found at: {path}")
        return

    for name in files:
        plugin_path = Path(name)
        shortname = plugin_path.stem

        if shortname in Config.UNLOAD:
            LOGS.info(f"Skipping unloaded plugin: {shortname}")
            continue

        try:
            load_module(shortname)
            LOGS.info(f"Loaded plugin: {shortname}")

        except Exception as e:
            LOGS.error(f"Failed to load plugin {shortname}: {e}")
            raise


# Final checks after startup
async def hell_is_on(total):
    await update_sudo()
    await logger_check(Hell)
    await start_msg(HellBot, HELL_PIC, __hellver__, total)

    clients = [Hell, H2, H3, H4, H5]

    for client in clients:
        if client is not None:
            await join_it(client)


# Hellbot starter
async def start_hellbot():
    try:
        tbot_id = await HellBot.get_me()
        Config.BOT_USERNAME = f"@{tbot_id.username}"

        Hell.tgbot = HellBot

        LOGS.info("••• Starting HellBot (TELETHON) •••")

        C1 = await hells(
            Config.HELLBOT_SESSION,
            Hell,
            "HELLBOT_SESSION",
        )

        C2 = await hells(
            Config.SESSION_2,
            H2,
            "SESSION_2",
        )

        C3 = await hells(
            Config.SESSION_3,
            H3,
            "SESSION_3",
        )

        C4 = await hells(
            Config.SESSION_4,
            H4,
            "SESSION_4",
        )

        C5 = await hells(
            Config.SESSION_5,
            H5,
            "SESSION_5",
        )

        if not HellBot.is_connected():
            await HellBot.start()

        total = C1 + C2 + C3 + C4 + C5

        if C1 == 0:
            raise RuntimeError(
                "Main Hell user session failed to start."
            )

        LOGS.info("••• HellBot Startup Completed •••")
        LOGS.info("••• Starting to load Plugins •••")

        await plug_load("TelethonHell/plugins/*.py")

        await plug_channel(Hell, Config.PLUGIN_CHANNEL)

        LOGS.info("⚡ Your userbot is run ab apni setting ka number de⚡")
        LOGS.info(
            "Head to @all_plugins_setup for Updates. "
            "Also join chat group to get help regarding HellBot."
        )
        LOGS.info(f"» Total Clients = {total} «")

        await hell_is_on(total)

    except Exception as e:
        LOGS.exception(f"HellBot startup failed: {e}")
        raise


# Main execution
try:
    Hell.loop.run_until_complete(start_hellbot())

    if len(sys.argv) not in (1, 3, 4):
        Hell.disconnect()
    else:
        LOGS.info("••• HellBot is running •••")
        Hell.run_until_disconnected()

except KeyboardInterrupt:
    LOGS.info("HellBot stopped manually.")

except ConnectionError as e:
    LOGS.warning(f"Telegram connection closed: {e}")

except Exception as e:
    LOGS.exception(f"Fatal startup error: {e}")
    sys.exit(1)


# hellbot
