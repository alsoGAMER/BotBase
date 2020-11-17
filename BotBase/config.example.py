"""
Copyright 2020 Nocturn9x & alsoGAMER

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

from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton, Client

# Antiflood module configuration
# The antiflood works by accumulating up to MAX_UPDATE_THRESHOLD updates (user-wise)
# and when that limit is reached, perform some checks to tell if the user is actually flooding


BAN_TIME = 300  # The amount of seconds the user will be banned
MAX_UPDATE_THRESHOLD = 7  # How many updates to accumulate before starting to count
PRIVATE_ONLY = True  # If True, the antiflood will only work in private chats
# The percentage (from 0 to 100) of updates that when below ANTIFLOOD_SENSIBILITY will trigger the anti flood

# Example, if FLOOD_PERCENTAGE == 75, if at least 75% of the messages from a user are marked as flood it will be blocked
FLOOD_PERCENTAGE = 75
# The minimum amount of seconds between updates. Updates that are sent faster than this limit will trigger the antiflood
# This should not be below 1, but you can experiment if you feel bold enough
ANTIFLOOD_SENSIBILITY = 1
# If you want the user to be notified of being flood-blocked, set this to the desired message, False to disable
FLOOD_NOTICE = f"🤙 <b>Hey amico!</b>\n🕐 Rilassati! Sei stato bloccato per {BAN_TIME / 60:.1f} minuti"
FLOOD_CLEARED = "♻️ Tabella antiflood svuotata"
FLOOD_USER_CLEARED = "♻️ Tabella antiflood ripulita per <code>{user}</code>"
DELETE_MESSAGES = True  # Set this to false if you do not want the messages to be deleted after flood is detected

# Various options and global variables

CACHE = defaultdict(lambda: ["none", 0])  # Global cache. DO NOT TOUCH IT, really just don't
VERSION = "2.0A"  # These will be shown in the 'Credits' section
RELEASE_DATE = "17/11/2020"
CREDITS = "‍💻 <b>Bot sviluppato</b> da @alsoGAMER & @Nocturn9x in <b>Python3.8</b> e <b>Pyrogram 0.18.0</b>" \
          f"\n⚙️ <b>Versione</b>: <code>{VERSION}</code>\n🗓 <b>Data di rilascio</b>: <code>{RELEASE_DATE}</code>"

# Telegram client configuration

WORKERS_NUM = 15  # The number of worker threads that pyrogram will spawn at startup.
# 10 workers means that the bot will process up to 10 users at the same time and then block until one worker has done
BOT_TOKEN = "TOKEN HERE"  # Get it with t.me/BotFather
SESSION_NAME = "BotBase"  # The name of the Telegram Session that the bot will have, will be visible from Telegram
PLUGINS_ROOT = {"root": f"BotBase/modules"}  # Do not change this unless you know what you're doing
API_ID = 1234569  # Get it at https://my.telegram.org/apps
API_HASH = "abcdef1234567"  # Same as above
DEVICE_MODEL = "BotBase"  # Name of the device shown in the sessions list - useless for a Bot
SYSTEM_VERSION = "2.0A"  # Host OS version - can be the same as VERSION
LANG_CODE = "en_US"  # Session lang_code

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

GREET = """Ciao {mention} [<code>{id}</code>]!"""  # The message that will be sent as a reply to the /start command. If this string is empty the bot will not reply
SUPPORT_BUTTON = "💭 Avvia Chat"  # The text for the button that triggers the live chat
BACK_BUTTON = "🔙 Indietro"
CREDITS_BUTTON = "ℹ Crediti"  # The text for the 'Credits' button
BUTTONS = InlineKeyboardMarkup([  # This keyboard will be sent along with GREET, feel free to add or remove buttons
    [InlineKeyboardButton(SUPPORT_BUTTON, "begin_chat"), InlineKeyboardButton(CREDITS_BUTTON, "bot_info")]])

# Database configuration
# The only natively supported database is SQLite3, but you can easily tweak
# this section and the BotBase/database/query.py file to work with any DBMS
# If you do so and want to share your code feel free to open a PR on the repo!

DB_PATH = os.path.join(os.getcwd(), f"BotBase/database/database.db")
DB_CREATE = """CREATE TABLE IF NOT EXISTS users (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        tg_id INTEGER UNIQUE NOT NULL,
                        uname TEXT UNIQUE NULL DEFAULT 'null',
                        date TEXT NOT NULL,
                        banned INTEGER NOT NULL DEFAULT 0);
            """

DB_GET_USERS = "SELECT tg_id FROM users"
DB_GET_USER = "SELECT * FROM users where users.tg_id = ?"
DB_SET_USER = "INSERT INTO users (id, tg_id, uname, date, banned) VALUES(?, ?, ?, ?, ?)"
DB_BAN_USER = "UPDATE users SET banned = 1 WHERE users.tg_id = ?"
DB_UNBAN_USER = "UPDATE users SET banned = 0 WHERE users.tg_id = ?"
DB_UPDATE_NAME = "UPDATE users SET uname = ? WHERE users.tg_id = ?"
DB_GET_USER_BY_NAME = "SELECT * FROM users where users.uname = ?"
from BotBase.database.query import get_user

# Admin module configuration

# Edit this dict adding the ID:NAME pair of the admin that you want to add. You can add as many admins as you want
ADMINS = {1234567: "Lorem Ipsum"}
MARKED_BUSY = "🎲 Ora sei impegnato, invia nuovamente /busy per resettare questo stato"
UNMARKED_BUSY = "✍ Da ora riceverai nuovamente le richieste di assistenza"
CANNOT_BAN_ADMIN = "❌ L'utente é un amministratore"
USER_BANNED = "✅ Utente bannato"
USER_UNBANNED = "✅ Utente sbannato"
YOU_ARE_UNBANNED = "✅ Sei stato sbannato"
USER_NOT_BANNED = "❌ L'utente non é bannato"
CLOSE_CHAT_BUTTON = "❌ Chiudi chat"
UPDATE_BUTTON = "🔄 Aggiorna"
USER_ALREADY_BANNED = "❌ L'utente é già bannato"
YOU_ARE_BANNED = "❌ Sei stato bannato"
WHISPER_FROM = "📣 Messaggio da {admin}: {msg}"
WHISPER_SUCCESSFUL = "✅ Inviato"
NAME = "tg://user?id={}"
BYPASS_FLOOD = True  # If False, admins can be flood-blocked too, otherwise the antiflood will ignore them
USER_INFO_UPDATED = "✅ Informazioni aggiornate"
USER_INFO_UNCHANGED = "❌ Non ho rilevato cambiamenti per questo utente"
ADMIN_ACCEPTED_CHAT = "✅ {admin} ha preso in carico la chat con {user}"
USER_LEFT_QUEUE = "⚠️ {user} ha lasciato la coda"
QUEUE_LIST = "🚻 Lista utenti in attesa\n\n{queue}"
CHATS_LIST = "💬 Lista utenti in chat\n\n{chats}"
ADMIN_BUSY = "(Occupato)"
USER_INFO = """ℹ️ <b>Informazioni</b>

🆔 <b>ID</b>: <code>{uid}</code>
✍️ <b>Username</b>: {uname}
🗓 <b>Registrato il</b>: <code>{date}</code>
⌨️ <b>Bannato</b>: <code>{status}</code>
💡 <b>Admin</b>: <code>{admin}</code>"""  # The message that is sent with /getuser and /getranduser
INVALID_SYNTAX = "❌ <b>Sintassi invalida</b>: Usa <code>{correct}</code>"  # This is sent when a command is used the wrong way
ERROR = "❌ <b>Errore</b>"  # This is sent when a command returns an error
NONNUMERIC_ID = "L'ID deve essere numerico!"  # This is sent if the parameter to /getuser is not a numerical ID
USERS_COUNT = "<b>Utenti totali</b>: <code>{count}</code>"  # This is sent as a result of the /count command
NO_PARAMETERS = "❌ <code>{command}</code> non richiede parametri"  # Error saying that the given command takes no parameters
ID_MISSING = "L'ID selezionato (<code>{uid}</code>) non é nel database"  # Error when given ID is not in database
NAME_MISSING = "L'username selezionato (<code>{uname}</code>) non é nel database"  # Error when given username is not in database
YES = "Sì"
NO = "No"
GLOBAL_MESSAGE_STATS = """<b>Statistiche messaggio</b>

✍️ <b>Messaggio</b>: <code>{msg}</code>
🔄 <b>Tentativi</b>: <code>{count}</code>
✅ <b>Consegnati</b>: <code>{success}</code>"""  # Statistics that are sent to the admin after /global command

# Live chat configuration

ADMINS_LIST_UPDATE_DELAY = 30  # How many seconds between an update and another

# These strings are pretty self explanatory, aren't they?
LIVE_CHAT_STATUSES = "Legenda: 🟢 = Disponibile, 🔴 = Occupato\n\n"
SUPPORT_NOTIFICATION = "🔔 Nuova richiesta di supporto!\n\n{uinfo}"
ADMIN_JOINS_CHAT = " [{admin_name}]({admin_id}) entra in chat!"
USER_CLOSES_CHAT = "🔔 [{user_name}]({user_id}) ha chiuso la chat"
USER_LEAVES_CHAT = "✅ Hai lasciato la chat"
USER_JOINS_CHAT = "✅ Sei entrato in chat"
CHAT_BUSY = "⚠️ Un altro admin é già entrato"
LEAVE_CURRENT_CHAT = "⚠️ Chiudi prima la chat corrente!"
CANNOT_REQUEST_SUPPORT = "⚠️ Non puoi avviare la chat!"
STATUS_FREE = "🟢 "
STATUS_BUSY = "🔴 "
SUPPORT_REQUEST_SENT = "✅ Ora sei in coda, attendi che un admin ti risponda\n\n" \
                       "🔄 <b>Admin disponibili</b>\n{queue}\n<b>Aggiornato il</b>: <code>{date}</code>\n\n<b>Nota</b>: <i>Se non ci sono admin disponibili al momento, premi il bottone 'Aggiorna' ogni tanto per scoprire se si é liberato un posto!</i>"
JOIN_CHAT_BUTTON = "❗ Entra in chat"
USER_MESSAGE = "🗣 [{user_name}]({user_id}): {message}"
ADMIN_MESSAGE = "🧑‍💻 [{user_name}]({user_id}): {message}"
TOO_FAST = "✋ Non così veloce! Riprova piú tardi"


# Custom filters  - Don't touch them as well but feel free to add more!


def check_user_banned(tg_id: int):
    res = get_user(tg_id)
    if isinstance(res, Exception):
        return False
    else:
        if not res:
            return False
        return res[-1]


def callback_regex(pattern: str):
    return Filters.create(lambda _, update: re.match(pattern, update.data))


def admin_is_chatting():
    return Filters.create(
        lambda _, update: update.from_user.id in ADMINS and CACHE[update.from_user.id][0] == "IN_CHAT")


def user_is_chatting():
    return Filters.create(
        lambda _, update: update.from_user.id not in ADMINS and CACHE[update.from_user.id][0] == "IN_CHAT")


def user_banned():
    return Filters.create(lambda _, update: check_user_banned(update.from_user.id))
