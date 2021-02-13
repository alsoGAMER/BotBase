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

import re

from pyrogram import filters

from BotBase.config import ADMINS, CACHE
from BotBase.database.query import check_banned


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
