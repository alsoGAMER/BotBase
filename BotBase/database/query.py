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

import sqlite3.dbapi2 as sqlite3
from BotBase.config import DB_GET_USERS, DB_GET_USER, DB_PATH, DB_SET_USER, DB_UPDATE_NAME, DB_BAN_USER, DB_UNBAN_USER, DB_GET_USER_BY_NAME
import logging
import time
import os


def create_database(path: str, query: str):
    if os.path.exists(path):
        logging.warning(f"Database file exists at {path}, running query")
    else:
        logging.warning(f"No database found, creating it at {path}")
    try:
        database = sqlite3.connect(path)
    except sqlite3.Error as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.executescript(query)
                database.close()
        except sqlite3.Error as query_error:
            logging.info(f"An error has occurred while executing DB_CREATE: {query_error}")


def get_user(tg_id: int):
    try:
        database = sqlite3.connect(DB_PATH)
    except sqlite3.Error as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                cursor = database.cursor()
                query = cursor.execute(DB_GET_USER, (tg_id,))
                return query.fetchone()
        except sqlite3.Error as query_error:
            logging.error(f"An error has occurred while executing DB_GET_USER query: {query_error}")
            return query_error


def get_user_by_name(uname: str):
    try:
        database = sqlite3.connect(DB_PATH)
    except sqlite3.Error as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                cursor = database.cursor()
                query = cursor.execute(DB_GET_USER_BY_NAME, (uname,))
                return query.fetchone()
        except sqlite3.Error as query_error:
            logging.error(f"An error has occurred while executing DB_GET_USER_BY_NAME query: {query_error}")
            return query_error


def update_name(tg_id: int, name: str):
    try:
        database = sqlite3.connect(DB_PATH)
    except sqlite3.Error as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.execute(DB_UPDATE_NAME, (name, tg_id))
            return True
        except sqlite3.Error as query_error:
            logging.error(f"An error has occurred while executing DB_UPDATE_NAME query: {query_error}")
            return query_error


def get_users():
    try:
        database = sqlite3.connect(DB_PATH)
    except sqlite3.Error as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                cursor = database.cursor()
                query = cursor.execute(DB_GET_USERS)
                return query.fetchall()
        except sqlite3.Error as query_error:
            logging.error(f"An error has occurred while executing DB_GET_USERS query: {query_error}")
            return query_error


def set_user(tg_id: int, uname: str):
    try:
        database = sqlite3.connect(DB_PATH)
    except sqlite3.Error as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.execute(DB_SET_USER, (None, tg_id, uname, time.strftime("%d/%m/%Y %T %p"), 0))
            return True
        except sqlite3.Error as query_error:
            logging.error(f"An error has occurred while executing DB_SET_USER query: {query_error}")
            return query_error


def ban_user(tg_id: int):
    try:
        database = sqlite3.connect(DB_PATH)
    except sqlite3.Error as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.execute(DB_BAN_USER, (tg_id, ))
            return True
        except sqlite3.Error as query_error:
            logging.error(f"An error has occurred while executing DB_BAN_USER query: {query_error}")
            return query_error


def unban_user(tg_id: int):
    try:
        database = sqlite3.connect(DB_PATH)
    except sqlite3.Error as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.execute(DB_UNBAN_USER, (tg_id, ))
            return True
        except sqlite3.Error as query_error:
            logging.error(f"An error has occurred while executing DB_UNBAN_USER query: {query_error}")
            return query_error
