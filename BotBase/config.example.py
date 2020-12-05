"""
Copyright 2020 Nocturn9x, alsoGAMER, CrisMystik

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

import os
import re
from collections import defaultdict

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Antiflood module configuration
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
FLOOD_NOTICE = f"🤙 <b>Hey buddy!</b>\n🕐 Relax! You have been banned for {BAN_TIME / 60:.1f} minutes"
# If you want the user to be notified of being flood-blocked, set this to the desired message, False to disable
FLOOD_CLEARED = "♻️ Antiflood table cleaned up"
FLOOD_USER_CLEARED = "♻️ Antiflood table for<code>{user}</code> cleaned up"
DELETE_MESSAGES = True
# Set this to false if you do not want the messages to be deleted after flood is detected

# Various options and global variables

CACHE = defaultdict(lambda: ["none", 0])
# Global cache. DO NOT TOUCH IT, really just don't
VERSION = "2.0.1a"
RELEASE_DATE = "05/12/2020"
CREDITS = "‍💻 <b>Bot developed by</b> @yourusernamehere in <b>Python3.x</b> and <b>BotBase 2.0.1</b>" \
          f"\n⚙️ <b>Version</b>: <code>{VERSION}</code>\n🗓 <b>Release date</b>: <code>{RELEASE_DATE}</code>"
# These will be shown in the 'Credits' section

# Telegram client configuration

WORKERS_NUM = 15
# The number of worker threads that pyrogram will spawn at the startup.
# 15 workers means that the bot will process up to 15 users at the same time and then block until one worker has done
BOT_TOKEN = "BOT_TOKEN_HERE"
# Get it with t.me/BotFather
SESSION_NAME = "BotBase"
# The name of the Telegram Session that the bot will have, will be visible from Telegram
PLUGINS_ROOT = {"root": f"BotBase/modules"}
# Do not change this unless you know what you're doing
API_ID = 123456
# Get it at https://my.telegram.org/apps
API_HASH = "API_HASH_HERE"
# Same as above
DEVICE_MODEL = "BotBase"
# Name of the device shown in the sessions list - useless for a Bot
SYSTEM_VERSION = "2.0.1a"
# Host OS version, can be the same as VERSION - also useless for a Bot
LANG_CODE = "en_US"
# Session lang_code

# Logging configuration
# To know more about what these options mean, check https://docs.python.org/3/library/logging.html

LOGGING_FORMAT = "[%(levelname)s %(asctime)s] In thread '%(threadName)s', " \
                 f"module %(module)s, function %(funcName)s at line %(lineno)d -> [{SESSION_NAME}] %(message)s"
DATE_FORMAT = "%d/%m/%Y %H:%M:%S %p"
LOGGING_LEVEL = 30
bot = Client(api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins=PLUGINS_ROOT,
             session_name=SESSION_NAME, workers=WORKERS_NUM, device_model=DEVICE_MODEL, system_version=SYSTEM_VERSION,
             lang_code=LANG_CODE)

# Start module
# P.S.: {mention} in the GREET message will be replaced with a mention to the user, same applies for {id} and {username}

GREET = """👋 <b>Hi</b> {mention} and <b>welcome</b> to <b>BotBase</b>."""
# The message that will be sent as a reply to the /start command. If this string is empty the bot will not reply.
SUPPORT_BUTTON = "💭 Start Chat"
# The text for the button that triggers the live chat
BACK_BUTTON = "🔙 Back"
# The text for the 'Back' button
CREDITS_BUTTON = "ℹ Credits"
# The text for the 'Credits' button
BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton(SUPPORT_BUTTON, "begin_chat"),
     InlineKeyboardButton(CREDITS_BUTTON, "bot_info")]])
# This keyboard will be sent along with GREET, feel free to add or remove buttons

# Database configuration
# The only natively supported database is SQLite3, but you can easily tweak
# this section and the BotBase/database/query.py file to work with any DBMS
# If you do so and want to share your code feel free to open a PR on the repo!

DB_PATH = os.path.join(os.getcwd(), f"BotBase/database/database.db")
DB_CREATE = """CREATE TABLE IF NOT EXISTS users (
                        tg_id INTEGER PRIMARY KEY NOT NULL,
                        tg_uname TEXT UNIQUE NULL DEFAULT 'null',
                        date TEXT NOT NULL,
                        banned INTEGER NOT NULL DEFAULT 0);
            """

DB_GET_USERS = "SELECT tg_id FROM users"
DB_GET_USER = "SELECT * FROM users where users.tg_id = ?"
DB_SET_USER = "INSERT INTO users (tg_id, tg_uname, date, banned) VALUES(?, ?, ?, ?)"
DB_BAN_USER = "UPDATE users SET banned = 1 WHERE users.tg_id = ?"
DB_UNBAN_USER = "UPDATE users SET banned = 0 WHERE users.tg_id = ?"
DB_CHECK_BANNED = "SELECT banned FROM users WHERE users.tg_id = ?"
DB_UPDATE_NAME = "UPDATE users SET tg_uname = ? WHERE users.tg_id = ?"
DB_GET_USER_BY_NAME = "SELECT * FROM users where users.tg_uname = ?"
from BotBase.database.query import check_banned

# Admin module configuration

ADMINS = {1234567: "Lorem Ipsum"}
# Edit this dict adding the ID:NAME pair of the admin that you want to add. You can add as many admins as you want.
MARKED_BUSY = "🎲 You're now busy, resend /busy to reset this state"
UNMARKED_BUSY = "✍ You'll now receive support requests again"
CANNOT_BAN_ADMIN = "❌ <b>Error</b>: This user is an administrator"
USER_BANNED = "✅ <b>User banned successfully</b>"
USER_UNBANNED = "✅ <b>User unbanned successfully</b>"
YOU_ARE_UNBANNED = "✅ <b>You've been unbanned</b>"
USER_NOT_BANNED = "❌ <b>This user isn't banned</b>"
CLOSE_CHAT_BUTTON = "❌ Close chat"
UPDATE_BUTTON = "🔄 Update"
USER_ALREADY_BANNED = "❌ <b>This user is already banned</b>"
YOU_ARE_BANNED = "❌ <b>You've been banned</b>"
WHISPER_FROM = "📣 <b>Message from</b> {admin}: {msg}"
WHISPER_SUCCESSFUL = "✅ <b>Sent successfully</b>"
NAME = "tg://user?id={}"
BYPASS_FLOOD = True
# If False, admins can be flood-blocked too, otherwise the antiflood will ignore them
USER_INFO_UPDATED = "✅ <i>Information updated</i>"
USER_INFO_UNCHANGED = "❌ <b>I haven't detected any changes for this user</b>"
ADMIN_ACCEPTED_CHAT = "✅ {admin} has joined the chat with {user}"
USER_LEFT_QUEUE = "⚠️ {user} left the queue"
QUEUE_LIST = "🚻 List of users waiting\n\n{queue}"
CHATS_LIST = "💬 List of users in chat\n\n{chats}"
ADMIN_BUSY = "(Busy)"
USER_INFO = """ℹ️ <b>User infos</b>

🆔 <b>ID</b>: <code>{tg_id}</code>
✍️ <b>Username</b>: {tg_uname}
🗓 <b>Registered on</b>: <code>{date}</code>
⌨️ <b>Banned</b>: <code>{status}</code>
💡 <b>Admin</b>: <code>{admin}</code>"""
# The message that is sent with /getuser and /getranduser
INVALID_SYNTAX = "❌ <b>Invalid syntax</b>: Use <code>{correct}</code>"
# This is sent when a command is used the wrong way
ERROR = "❌ <b>Error</b>"
# This is sent when a command returns an error
NON_NUMERIC_ID = "The ID must be numeric!"
# This is sent if the parameter to /getuser is not a numerical ID
USERS_COUNT = "<b>Total users</b>: <code>{count}</code>"
# This is sent as a result of the /count command
NO_PARAMETERS = "❌ <code>{command}</code> requires no parameters"
# Error saying that the given command takes no parameters
ID_MISSING = "The selected ID (<code>{tg_id}</code>) isn't in the database"
# Error when given ID is not in database
NAME_MISSING = "The selected username (<code>{tg_uname}</code>) isn't in the database"
# Error when given username is not in database
YES = "Yes"
NO = "No"
GLOBAL_MESSAGE_STATS = """<b>Message Statistics</b>

✍️ <b>Message</b>: <code>{msg}</code>
🔄 <b>Attempts</b>: <code>{count}</code>
✅ <b>Delivered</b>: <code>{success}</code>"""
# Statistics that are sent to the admin after /global command

# Live chat configuration

ADMINS_LIST_UPDATE_DELAY = 30
# How many seconds between an update and another
LIVE_CHAT_STATUSES = "Legend: 🟢 = Available, 🔴 = Busy\n\n"
SUPPORT_NOTIFICATION = "🔔 New support request!\n\n{uinfo}"
ADMIN_JOINS_CHAT = " [{admin_name}]({admin_id}) joined the chat!"
USER_CLOSES_CHAT = "🔔 [{user_name}]({user_id}) closed the chat"
USER_LEAVES_CHAT = "✅ You left the chat"
USER_JOINS_CHAT = "✅ You've joined the chat"
CHAT_BUSY = "⚠️ Another admin has already joined"
LEAVE_CURRENT_CHAT = "⚠️ Close current chat first!"
CANNOT_REQUEST_SUPPORT = "⚠️ You can't start a chat!"
STATUS_FREE = "🟢 "
STATUS_BUSY = "🔴 "
SUPPORT_REQUEST_SENT = "✅ You're now in the queue, wait for an admin to answer you\n\n" \
                       "🔄 <b>Admins available</b>\n{queue}\n<b>Updated on</b>: <code>{date}</code>\n\n<b>Note</b>: " \
                       "<i>If there are no admins available at the moment, press the 'Update' button every now and " \
                       "then to find out if a seat is available!"
JOIN_CHAT_BUTTON = "❗ Join the chat"
USER_MESSAGE = "🗣 [{user_name}]({user_id}): {message}"
ADMIN_MESSAGE = "🧑‍💻 [{user_name}]({user_id}): {message}"
TOO_FAST = "✋ Calm down! Try again later"


# Custom filters  - Don't touch them as well but feel free to add more!

def check_user_banned(tg_id: int):
    res = check_banned(tg_id)
    if isinstance(res, Exception):
        return False
    else:
        if not res:
            return False
        return bool(res[0])


def callback_regex(pattern: str):
    return filters.create(lambda flt, client, update: re.match(pattern, update.data))


def admin_is_chatting():
    return filters.create(
        lambda flt, client, update: update.from_user.id in ADMINS and CACHE[update.from_user.id][0] == "IN_CHAT")


def user_is_chatting():
    return filters.create(
        lambda flt, client, update: update.from_user.id not in ADMINS and CACHE[update.from_user.id][0] == "IN_CHAT")


def user_banned():
    return filters.create(lambda flt, client, update: check_user_banned(update.from_user.id))
