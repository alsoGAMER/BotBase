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

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from BotBase.config import ADMINS, BUTTONS, CACHE, CREDITS, GREET, NAME, VERSION, bot
from BotBase.strings.default_strings import BACK_BUTTON, USER_LEFT_QUEUE
from BotBase.methods.custom_filters import user_banned
from BotBase.database.query import get_users, set_user
from BotBase.methods import MethodWrapper
from BotBase.modules.antiflood import BANNED_USERS

wrapper = MethodWrapper(bot)


@Client.on_message(filters.command("start") & ~BANNED_USERS & filters.private & ~user_banned())
async def start_handler(_, update):
    """Simply handles the /start command sending a pre-defined greeting
    and saving new users to the database"""
    update_wrapper = MethodWrapper(update)

    if update.from_user.first_name:
        name = update.from_user.first_name
    elif update.from_user.username:
        name = update.from_user.username
    else:
        name = "Anonymous"
    if update.from_user.id not in itertools.chain(*get_users()):
        logging.warning(f"New user detected ({update.from_user.id}), adding to database")
        set_user(update.from_user.id, update.from_user.username.lower() if update.from_user.username else None)
    if GREET:
        if isinstance(update, Message):
            await update_wrapper.reply(
                text=GREET.format(
                    mention=f"[{name}](tg://user?id={update.from_user.id})",
                    id=update.from_user.id,
                    username=update.from_user.username
                ),
                reply_markup=BUTTONS
            )
        elif isinstance(update, CallbackQuery):
            if CACHE[update.from_user.id][0] == "AWAITING_ADMIN":
                data = CACHE[update.from_user.id][-1]

                if isinstance(data, list):
                    for chatid, message_ids in data:
                        await wrapper.delete_messages(chatid, message_ids)

                for admin in ADMINS:
                    await wrapper.send_message(
                        chat_id=admin,
                        text=USER_LEFT_QUEUE.format(user=f"[{name}]({NAME.format(update.from_user.id)})")
                    )

            await update_wrapper.edit_message_text(
                text=GREET.format(
                    mention=f"[{name}](tg://user?id={update.from_user.id})",
                    id=update.from_user.id,
                    username=update.from_user.username
                ),
                reply_markup=BUTTONS
            )

            del CACHE[update.from_user.id]
            await update_wrapper.answer()


@Client.on_callback_query(filters.regex("back_start") & ~BANNED_USERS)
async def cb_start_handler(_, message):
    await start_handler(_, message)


@Client.on_callback_query(filters.regex("bot_about") & ~BANNED_USERS)
async def bot_about(_, query):
    cb_wrapper = MethodWrapper(query)
    await cb_wrapper.edit_message_text(
        text=CREDITS.format(VERSION=VERSION),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(BACK_BUTTON, "back_start")]])
    )
    await cb_wrapper.answer()
