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

import logging
import time

import MySQLdb

from BotBase.config import DB_URL
from BotBase.database.raw_queries import *


def create_table(query: str):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.execute(query)
                DB_URL.commit()
                database.close()
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.info(f"An error has occurred while executing CREATE_TABLE: {query_error}")


def get_user(tg_id: int):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.execute(DB_GET_USER, (tg_id,))
                return database.fetchone()
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(f"An error has occurred while executing DB_GET_USER query: {query_error}")
            return query_error


def get_user_by_name(tg_uname: str):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.execute(DB_GET_USER_BY_NAME, (tg_uname,))
                return database.fetchone()
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(f"An error has occurred while executing DB_GET_USER_BY_NAME query: {query_error}")
            return query_error


def update_name(tg_id: int, name: str):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.execute(DB_UPDATE_NAME, (name, tg_id))
                DB_URL.commit()
            return True
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(f"An error has occurred while executing DB_UPDATE_NAME query: {query_error}")
            return query_error


def get_users():
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.execute(DB_GET_USERS)
                return database.fetchall()
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(f"An error has occurred while executing DB_GET_USERS query: {query_error}")
            return query_error


def set_user(tg_id: int, tg_uname: str):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.execute(DB_SET_USER,
                                 (tg_id, tg_uname, time.strftime("%d/%m/%Y %T %p"), 0))
                DB_URL.commit()
            return True
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(f"An error has occurred while executing DB_SET_USER query: {query_error}")
            return query_error


def ban_user(tg_id: int):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.execute(DB_BAN_USER, (tg_id,))
                DB_URL.commit()
            return True
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(f"An error has occurred while executing DB_BAN_USER query: {query_error}")
            return query_error


def unban_user(tg_id: int):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.execute(DB_UNBAN_USER, (tg_id,))
                DB_URL.commit()
            return True
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(f"An error has occurred while executing DB_UNBAN_USER query: {query_error}")
            return query_error


def check_banned(tg_id: int):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(f"An error has occurred while connecting to database: {connection_error}")
    else:
        try:
            with database:
                database.execute(DB_CHECK_BANNED, (tg_id,))
                return database.fetchone()
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(f"An error has occurred while executing DB_CHECK_BANNED query: {query_error}")
            return query_error
