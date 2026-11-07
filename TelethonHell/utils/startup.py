
from HellConfig import Config

from telethon import Button
from telethon.tl import functions
from telethon.tl.types import ChatAdminRights

from TelethonHell.clients.logger import LOGGER as LOGS
from TelethonHell.DB.gvar_sql import addgvar, gvarstat
from TelethonHell.helpers.int_str import make_int
from TelethonHell.version import __telever__


# Creates the logger group on first deploy and adds the helper bot
async def logger_id(client):
    desc = "A Bot Logger Group For Hellbot. DO NOT LEAVE THIS GROUP!!"

    try:
        grp = await client(
            functions.channels.CreateChannelRequest(
                title="govind userbot Logger",
                about=desc,
                megagroup=True,
            )
        )

        grp_id = grp.chats[0].id

        if not str(grp_id).startswith("-100"):
            grp_id = int(f"-100{grp_id}")

        LOGS.info(f"Logger group created: {grp_id}")

    except Exception as e:
        LOGS.error(f"Logger group creation failed: {e}")
        return None

    if not Config.BOT_USERNAME:
        LOGS.warning("BOT_USERNAME is not available. Assistant was not invited.")
        return grp_id

    try:
        new_rights = ChatAdminRights(
            add_admins=True,
            invite_users=True,
            change_info=True,
            ban_users=True,
            delete_messages=True,
            pin_messages=True,
            manage_call=True,
        )

        await client(
            functions.channels.InviteToChannelRequest(
                channel=grp_id,
                users=[Config.BOT_USERNAME],
            )
        )

        await client(
            functions.channels.EditAdminRequest(
                channel=grp_id,
                user_id=Config.BOT_USERNAME,
                admin_rights=new_rights,
                rank="assistant",
            )
        )

        LOGS.info("Assistant bot added and promoted to admin.")

    except Exception as e:
        LOGS.error(f"Assistant setup failed: {e}")

    return grp_id


# Updates sudo cache on every restart
async def update_sudo():
    try:
        sudo_users = list(Config.SUDO_USERS or [])
        stored_sudo = gvarstat("SUDO_USERS")

        if stored_sudo:
            int_list = await make_int(stored_sudo)

            if int_list:
                sudo_users.extend(int_list)

        Config.SUDO_USERS = list(dict.fromkeys(
            int(user) for user in sudo_users
        ))

        LOGS.info(
            f"SUDO users loaded: {len(Config.SUDO_USERS)}"
        )

    except Exception as e:
        LOGS.error(f"SUDO update failed: {e}")


# Checks for logger group
async def logger_check(bot):
    try:
        logger = Config.LOGGER_ID

        if not logger:
            logger = gvarstat("LOGGER_ID")

        if not logger:
            logger = await logger_id(bot)

            if not logger:
                raise RuntimeError(
                    "Logger group could not be created."
                )

            addgvar("LOGGER_ID", logger)

        Config.LOGGER_ID = int(logger)

        LOGS.info(f"Logger group configured: {Config.LOGGER_ID}")

    except Exception as e:
        LOGS.error(f"Logger configuration failed: {e}")
        raise


# Sends the startup message to logger group
async def start_msg(client, pic, version, total):
    is_sudo = "True" if Config.SUDO_USERS else "False"

    text = f"""
#START

<b><i>Version:</i></b> <code>{version}</code>
<b><i>Clients:</i></b> <code>{total}</code>
<b><i>Sudo:</i></b> <code>{is_sudo}</code>
<b><i>Library:</i></b> <code>Telethon - {__telever__}</code>

<b><i>»» <u><a href="https://t.me/all_plugins_setup">more help</a></u> ««</i></b>
"""

    try:
        await client.send_file(
            Config.LOGGER_ID,
            pic,
            caption=text,
            parse_mode="HTML",
            buttons=[
                [
                    Button.url(
                        "govind Network",
                        "https://t.me/all_plugins_setup",
                    )
                ]
            ],
        )

        LOGS.info("Startup message sent to logger group.")

    except Exception as e:
        LOGS.error(f"Startup message failed: {e}")
        raise


# Joins the hellbot chat and channel from all clients
async def join_it(client):
    if client is None:
        return

    try:
        await client(
            functions.channels.JoinChannelRequest(
                "@all_plugins_setup"
            )
        )
    except Exception as e:
        LOGS.warning(f"Plugin channel join: {e}")

    try:
        await client(
            functions.messages.ImportChatInviteRequest(
                "itu7bWHnA2djNjY1"
            )
        )
    except Exception as e:
        LOGS.warning(f"Plugin group join: {e}")


# hellbot
