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

import itertools
import logging
import random
import re

from pyrogram import Client, filters

from BotBase.config import ADMINS, CACHE, GLOBAL_MESSAGE_STATS, NAME, USER_INFO, bot
from BotBase.strings.default_strings import CANNOT_BAN_ADMIN, CHATS_LIST, ERROR, ID_MISSING, INVALID_SYNTAX, \
    LEAVE_CURRENT_CHAT, MARKED_BUSY, NAME_MISSING, NO, NON_NUMERIC_ID, NO_PARAMETERS, QUEUE_LIST, UNMARKED_BUSY, \
    USERS_COUNT, USER_ALREADY_BANNED, USER_BANNED, USER_INFO_UNCHANGED, USER_INFO_UPDATED, USER_NOT_BANNED, \
    USER_UNBANNED, WHISPER_FROM, WHISPER_SUCCESSFUL, YES, YOU_ARE_BANNED, YOU_ARE_UNBANNED
from BotBase.database.query import ban_user, get_user, get_user_by_name, get_users, unban_user, update_name
from BotBase.methods import MethodWrapper
from BotBase.modules.antiflood import BANNED_USERS

ADMINS_FILTER = filters.user(list(ADMINS.keys()))
wrapper = MethodWrapper(bot)


def format_user(user):
    tg_id, tg_uname, date, banned = user
    return USER_INFO.format(
        tg_id=tg_id,
        tg_uname='@' + tg_uname if tg_uname else 'N/A',
        date=date,
        status=YES if banned else NO,
        admin=YES if tg_id in ADMINS else NO,
    )


@Client.on_message(filters.command("getranduser") & ADMINS_FILTER & ~BANNED_USERS & ~filters.edited)
async def get_random_user(_, message):
    logging.warning(f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /getranduser")
    if len(message.command) > 1:
        await wrapper.send_message(message.chat.id, NO_PARAMETERS.format(command='/getranduser'))
    else:
        user = random.choice(get_users())
        result = get_user(*user)
        text = format_user(result)
        await wrapper.send_message(message.chat.id, text)


@Client.on_message(filters.command("getuser") & ADMINS_FILTER & filters.private & ~BANNED_USERS & ~filters.edited)
async def get_user_info(_, message):
    if len(message.command) != 2:
        return await wrapper.send_message(message.chat.id, INVALID_SYNTAX.format(correct='/getuser id/[@]username'))

    if message.command[1].isdigit():
        name = None
        user = get_user(message.command[1])
    else:
        name = message.command[1].lstrip("@").lower()
        user = get_user_by_name(name)

    if user:
        logging.warning(
            f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /getuser {message.command[1]}")
        result = user
        text = format_user(result)
        await wrapper.send_message(message.chat.id, text)
    else:
        if name:
            await wrapper.send_message(message.chat.id, f"{ERROR}: {NAME_MISSING.format(tg_uname=message.command[1])}")
        else:
            await wrapper.send_message(message.chat.id, f"{ERROR}: {ID_MISSING.format(tg_id=message.command[1])}")


@Client.on_message(filters.command("count") & ADMINS_FILTER & filters.private & ~BANNED_USERS & ~filters.edited)
async def count_users(_, message):
    if len(message.command) > 1:
        await wrapper.send_message(message.chat.id, NO_PARAMETERS.format(command='/count'))
    else:
        logging.warning(f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /count")
        count = len(get_users())
        await wrapper.send_message(message.chat.id, USERS_COUNT.format(count=count))


@Client.on_message(filters.command("global") & ADMINS_FILTER & filters.private & ~BANNED_USERS & ~filters.edited)
async def global_message(_, message):
    if len(message.command) > 1:
        msg = message.text.html[7:]
        logging.warning(
            f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent the following global message: {msg}"
        )

        missed = 0
        count = 0

        for tg_id in itertools.chain(*get_users()):
            count += 1
            result = await wrapper.send_message(tg_id, msg)

            if isinstance(result, Exception):
                logging.error(
                    f"Could not deliver the global message to {tg_id} because of {type(result).__name__}: {result}"
                )
                missed += 1

        logging.warning(f"{count - missed}/{count} global messages were successfully delivered")
        await wrapper.send_message(
            message.chat.id,
            GLOBAL_MESSAGE_STATS.format(count=count, success=(count - missed), msg=msg)
        )
    else:
        await wrapper.send_message(
            message.chat.id,
            f"{INVALID_SYNTAX.format(correct='/global message')}\n<b>HTML and Markdown styling supported</b>"
        )


@Client.on_message(filters.command("whisper") & ADMINS_FILTER & filters.private & ~BANNED_USERS & ~filters.edited)
async def whisper(_, message):
    if len(message.command) < 2:
        return await wrapper.send_message(
            message.chat.id,
            f"{INVALID_SYNTAX.format(correct='/whisper ID')}\n<b>HTML and Markdown styling supported</b>"
        )

    if not message.command[1].isdigit():
        return await wrapper.send_message(message.chat.id, f"{ERROR}: {NON_NUMERIC_ID}")

    logging.warning(f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent {message.text.html}")

    tg_id = int(message.command[1])
    msg = message.text.html[9:]
    msg = msg[re.search(message.command[1], msg).end():]

    if tg_id not in itertools.chain(*get_users()):
        return await wrapper.send_message(message.chat.id, f"{ERROR}: {ID_MISSING.format(tg_id=tg_id)}")

    result = await wrapper.send_message(
        tg_id,
        WHISPER_FROM.format(
            admin=f"[{ADMINS[message.from_user.id]}]({NAME.format(message.from_user.id)})",
            msg=msg
        )
    )

    if isinstance(result, Exception):
        logging.error(f"Could not whisper to {tg_id} because of {type(result).__name__}: {result}")
        await wrapper.send_message(message.chat.id, f"{ERROR}: {type(result).__name__} -> {result}")
    else:
        await wrapper.send_message(message.chat.id, WHISPER_SUCCESSFUL)


@Client.on_message(filters.command("update") & ADMINS_FILTER & filters.private & ~BANNED_USERS & ~filters.edited)
async def update(_, message):
    if len(message.command) != 2:
        return await wrapper.send_message(message.chat.id, INVALID_SYNTAX.format(correct='/update ID'))

    if not message.command[1].isdigit():
        return await wrapper.send_message(message.chat.id, f"{ERROR}: {NON_NUMERIC_ID}")

    user = get_user(message.command[1])
    if user:
        logging.warning(f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /update {message.command[1]}")

        tg_id, tg_uname = user[:2]
        new = await wrapper.get_users(tg_id)

        if isinstance(new, Exception):
            logging.error(f"An error has occurred when calling get_users({tg_id}), {type(new).__name__}: {new}")
            await wrapper.send_message(message.chat.id, f"{ERROR}: {type(new).__name__} -> {new}")
        else:
            if new.username is None:
                new.username = "null"
            if new.username != tg_uname:
                update_name(tg_id, new.username)
                await wrapper.send_message(message.chat.id, USER_INFO_UPDATED)
            else:
                await wrapper.send_message(message.chat.id, USER_INFO_UNCHANGED)
    else:
        await wrapper.send_message(message.chat.id, f"{ERROR}: {ID_MISSING.format(tg_id=message.command[1])}")


@Client.on_message(filters.command(["ban", "unban"]) & ADMINS_FILTER & filters.private & ~BANNED_USERS &
                   ~filters.edited)
async def ban(_, message):
    cmd = message.command[0]
    condition = {"ban": False, "unban": True}.get(cmd)

    if len(message.command) != 2:
        return await wrapper.send_message(message.chat.id, INVALID_SYNTAX.format(correct=f'/{cmd} ID'))

    if not message.command[1].isdigit():
        return await wrapper.send_message(message.chat.id, f"{ERROR}: {NON_NUMERIC_ID}")

    if int(message.command[1]) in ADMINS:
        return await wrapper.send_message(message.chat.id, CANNOT_BAN_ADMIN)

    user = get_user(message.command[1])
    if user:
        if bool(user[3]) is condition:
            logging.warning(f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /{cmd} {message.command[1]}")

            tg_id = user[0]
            if condition:
                res = unban_user(tg_id)
            else:
                res = ban_user(tg_id)

            if isinstance(res, Exception):
                logging.error(f"An error has occurred when calling {cmd}_user({tg_id}), {type(res).__name__}: {res}")
                await wrapper.send_message(message.chat.id, f"{ERROR}: {type(res).__name__} -> {res}")
            else:
                if condition and tg_id in BANNED_USERS:
                    BANNED_USERS.remove(tg_id)
                else:
                    BANNED_USERS.add(tg_id)

                await wrapper.send_message(message.chat.id, USER_UNBANNED if condition else USER_BANNED)
                await wrapper.send_message(tg_id, YOU_ARE_UNBANNED if condition else YOU_ARE_BANNED)
        else:
            await wrapper.send_message(message.chat.id, USER_NOT_BANNED if condition else USER_ALREADY_BANNED)
    else:
        await wrapper.send_message(message.chat.id, f"{ERROR}: {ID_MISSING.format(tg_id=message.command[1])}")


@Client.on_message(filters.command("busy") & ADMINS_FILTER & filters.private & ~BANNED_USERS & ~filters.edited)
async def busy(_, message):
    if len(message.command) > 1:
        return await wrapper.send_message(message.chat.id, f"{NO_PARAMETERS.format(command='/busy')}")

    logging.warning(f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /busy")
    if CACHE[message.from_user.id][0] == "IN_CHAT" and CACHE[message.from_user.id][1] != 1234567:
        await wrapper.send_message(message.from_user.id, LEAVE_CURRENT_CHAT)
    elif CACHE[message.from_user.id][0] == "none":
        await wrapper.send_message(message.chat.id, MARKED_BUSY)
        CACHE[message.from_user.id] = ["IN_CHAT", 1234567]
    else:
        if message.from_user.id in CACHE:
            del CACHE[message.from_user.id]
        await wrapper.send_message(message.chat.id, UNMARKED_BUSY)


@Client.on_message(filters.command("chats") & ADMINS_FILTER & filters.private & ~BANNED_USERS & ~filters.edited)
async def chats(_, message):
    if len(message.command) > 1:
        return await wrapper.send_message(message.chat.id, f"{NO_PARAMETERS.format(command='/chats')}")

    logging.warning(f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /chats")
    text = ""
    for user in CACHE:
        if CACHE[user][0] == "IN_CHAT" and user not in ADMINS:
            admin_id = CACHE[user][1]
            admin_name = ADMINS[admin_id]
            text += f"- 👤 [User]({NAME.format(user)}) -> 👨‍💻 [{admin_name}]({NAME.format(admin_id)})\n"
    await wrapper.send_message(message.chat.id, CHATS_LIST.format(chats=text))


@Client.on_message(filters.command("queue") & ADMINS_FILTER & filters.private & ~BANNED_USERS & ~filters.edited)
async def queue(_, message):
    if len(message.command) > 1:
        return await wrapper.send_message(message.chat.id, f"{NO_PARAMETERS.format(command='/queue')}")

    logging.warning(f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /queue")
    text = ""
    for user in CACHE:
        if CACHE[user][0] == "AWAITING_ADMIN":
            text += f"- 👤 [User]({NAME.format(user)})\n"
    await wrapper.send_message(message.chat.id, QUEUE_LIST.format(queue=text))
