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

import logging

from BotBase.config import bot, LOGGING_LEVEL, LOGGING_FORMAT, DATE_FORMAT, DB_PATH, DB_CREATE
from BotBase.database.query import create_database
from pyrogram.session import Session


if __name__ == "__main__":
    logging.basicConfig(format=LOGGING_FORMAT, datefmt=DATE_FORMAT, level=LOGGING_LEVEL)
    Session.notice_displayed = True
    try:
        logging.warning("Running create_database()")
        create_database(DB_PATH, DB_CREATE)
        logging.warning("Database interaction complete")
        logging.warning("Starting bot")
        bot.run()
        logging.warning("Bot started")
    except Exception as e:
        logging.warning(f"Stopping bot due to a {type(e).__name__}: {e}")
        bot.stop()
