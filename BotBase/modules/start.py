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

import itertools
import logging

from pyrogram import Client, Filters, InlineKeyboardButton, InlineKeyboardMarkup

from BotBase.modules.antiflood import BANNED_USERS
from BotBase.config import GREET, BUTTONS, CACHE, bot, VERSION, user_banned, BACK_BUTTON, USER_LEFT_QUEUE, ADMINS, NAME, \
    CREDITS
from BotBase.database.query import get_users, set_user
from BotBase.methods import MethodWrapper

wrapper = MethodWrapper(bot)


@Client.on_message(Filters.command("start") & ~BANNED_USERS & Filters.private & ~user_banned())
def start_handler(_, message):
    """Simply handles the /start command sending a pre-defined greeting
    and saving new users to the database"""

    if message.from_user.first_name:
        name = message.from_user.first_name
    elif message.from_user.username:
        name = message.from_user.username
    else:
        name = "Anonymous"
    if message.from_user.id not in itertools.chain(*get_users()):
        logging.warning(f"New user detected ({message.from_user.id}), adding to database")
        set_user(message.from_user.id, message.from_user.username.lower() if message.from_user.username else None)
    if GREET:
        wrapper.send_message(message.from_user.id,
                             GREET.format(mention=f"[{name}](tg://user?id={message.from_user.id})",
                                          id=message.from_user.id,
                                          username=message.from_user.username
                                          ),
                             reply_markup=BUTTONS
                             )


@Client.on_callback_query(Filters.regex("back_start") & ~BANNED_USERS)
def back_start(_, query):
    cb_wrapper = MethodWrapper(query)
    if query.from_user.first_name:
        name = query.from_user.first_name
    elif query.from_user.username:
        name = query.from_user.usernamenel
    else:
        name = "Anonymous"
    if CACHE[query.from_user.id][0] == "AWAITING_ADMIN":
        data = CACHE[query.from_user.id][-1]
        if isinstance(data, list):
            for chatid, message_ids in data:
                wrapper.delete_messages(chatid, message_ids)
        for admin in ADMINS:
            wrapper.send_message(admin, USER_LEFT_QUEUE.format(user=f"[{name}]({NAME.format(query.from_user.id)})"))

    cb_wrapper.edit_message_text(
        GREET.format(mention=f"[{name}](tg://user?id={query.from_user.id})", id=query.from_user.id,
                     username=query.from_user.username),
        reply_markup=BUTTONS)
    del CACHE[query.from_user.id]


@Client.on_callback_query(Filters.regex("bot_info") & ~BANNED_USERS)
def bot_info(_, query):
    cb_wrapper = MethodWrapper(query)
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton(BACK_BUTTON, "back_start")]])
    cb_wrapper.edit_message_text(CREDITS.format(VERSION=VERSION), disable_web_page_preview=True,
                                 reply_markup=buttons)
