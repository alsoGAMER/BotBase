"""
Copyright 2020-2021 Nocturn9x, alsoGAMER, CrisMystik

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from collections import defaultdict

import MySQLdb
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# region Antiflood module configuration
# The antiflood works by accumulating up to MAX_UPDATE_THRESHOLD updates (user-wise) and
# when that limit is reached, perform some checks to tell if the user is actually flooding

BAN_TIME = 300
# The amount of seconds the user will be banned
MAX_UPDATE_THRESHOLD = 7
# How many updates to accumulate before starting to count
PRIVATE_ONLY = True
# If True, the antiflood will only work in private chats
FLOOD_PERCENTAGE = 75
# The percentage (from 0 to 100) of updates that when below ANTIFLOOD_SENSIBILITY will trigger the anti flood
# Example, if FLOOD_PERCENTAGE == 75, if at least 75% of the messages from a user are marked as flood it will be blocked
ANTIFLOOD_SENSIBILITY = 1
# The minimum amount of seconds between updates. Updates that are sent faster than this limit will trigger the antiflood
# This should not be below 1, but you can experiment if you feel bold enough
DELETE_MESSAGES = True
# Set this to false if you do not want the messages to be deleted after flood is detected
# endregion

# region Various options and global variables

CACHE = defaultdict(lambda: ["none", 0])
# Global cache. DO NOT TOUCH IT, really just don't
VERSION = ""
RELEASE_DATE = ""
CREDITS = "‍💻 <b>Bot developed by</b> @yourusernamehere in <b>Python3.9</b> and <b>BotBase 2.1.1</b>" \
          f"\n⚙️ <b>Version</b>: <code>{VERSION}</code>\n🗓 <b>Release Date</b>: <code>{RELEASE_DATE}</code>"
# These will be shown in the 'Credits' section
# endregion

# region Telegram client configuration

WORKERS_NUM = 15
# The number of worker threads that pyrogram will spawn at the startup.
# 15 workers means that the bot will process up to 15 users at the same time and then block until one worker has done

BOT_TOKEN = ""
# Get it with t.me/BotFather
SESSION_NAME = ""
# The name of the Telegram Session that the bot will have, will be visible from Telegram
PLUGINS_ROOT = {"root": f"BotBase/modules"}
# Do not change this unless you know what you're doing
API_ID = 000000
# Get it at https://my.telegram.org/apps
API_HASH = ""
# Same as above
DEVICE_MODEL = ""
# Name of the device shown in the sessions list - useless for a Bot
SYSTEM_VERSION = ""
# Host OS version, can be the same as VERSION - also useless for a Bot
LANG_CODE = "en_US"
# Session lang_code
# endregion

# region Logging configuration
# To know more about what these options mean, check https://docs.python.org/3/library/logging.html

LOGGING_FORMAT = "[%(levelname)s %(asctime)s] In thread '%(threadName)s', " \
                 f"module %(module)s, function %(funcName)s at line %(lineno)d -> [{SESSION_NAME}] %(message)s"
DATE_FORMAT = "%d/%m/%Y %H:%M:%S %p"
LOGGING_LEVEL = 30
bot = Client(api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins=PLUGINS_ROOT,
             session_name=SESSION_NAME, workers=WORKERS_NUM, device_model=DEVICE_MODEL, system_version=SYSTEM_VERSION,
             lang_code=LANG_CODE)
# endregion

# region Start module
# P.S.: {mention} in the GREET message will be replaced with a mention to the user, same applies for {id} and {username}

GREET = "👋 <b>Hi</b> {mention} and <b>welcome</b> to <b>BotBase</b>."
# The message that will be sent to the users as a reply to the /start command. If this string is empty the bot will not reply.
# endregion

# region Database configuration
# The only natively supported database is MariaDB, but you can easily tweak
# this section and the BotBase/database/query.py file to work with any DBMS
# If you do so and want to share your code feel free to open a PR on the repo!

DB_URL = MySQLdb.connect(host="host", user="user", passwd="passwd", db="db")
# endregion

# region Greet Keyboard
from BotBase.strings.default_strings import SUPPORT_BUTTON, ABOUT_BUTTON
BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton(SUPPORT_BUTTON, "begin_chat"),
     InlineKeyboardButton(ABOUT_BUTTON, "bot_about")]])
# This keyboard will be sent along with GREET, feel free to add or remove buttons
# endregion

# region Admin module configuration

ADMINS = {00000000: "A Dude"}
# Edit this dict adding the ID:NAME pair of the admin that you want to add. You can add as many admins as you want.

NAME = "tg://user?id={}"
BYPASS_FLOOD = True
# If False, admins can be flood-blocked too, otherwise the antiflood will ignore them
USER_INFO = """ℹ️ <b>User info</b>

🆔 <b>ID</b>: <code>{tg_id}</code>
✍️ <b>Username</b>: {tg_uname}
🗓 <b>Registered on</b>: <code>{date}</code>
⌨️ <b>Banned</b>: <code>{status}</code>
💡 <b>Admin</b>: <code>{admin}</code>"""
# The message that is sent with /getuser and /getranduser
GLOBAL_MESSAGE_STATS = """<b>Message Statistics</b>

✍️ <b>Message</b>: <code>{msg}</code>
🔄 <b>Attempts</b>: <code>{count}</code>
✅ <b>Delivered</b>: <code>{success}</code>"""
# Statistics that are sent to the admin after /global command
# endregion

# region Live chat configuration

ADMINS_LIST_UPDATE_DELAY = 30
# How many seconds between an update and another
LIVE_CHAT_STATUSES = "Legend: 🟢 = Available, 🔴 = Busy\n\n"
STATUS_FREE = "🟢 "
STATUS_BUSY = "🔴 "
USER_MESSAGE = "🗣 [{user_name}]({user_id}): {message}"
ADMIN_MESSAGE = "🧑‍💻 [{user_name}]({user_id}): {message}"
# endregion
