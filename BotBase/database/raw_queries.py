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

# region CreateTablesQueries
CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
                        tg_id INTEGER(20) PRIMARY KEY NOT NULL,
                        tg_uname VARCHAR(32) UNIQUE NULL DEFAULT 'null',
                        date TEXT NOT NULL,
                        banned TINYINT(1) NOT NULL DEFAULT 0);
            """
# endregion


DB_GET_USERS = "SELECT users.tg_id FROM users"
DB_GET_USER = "SELECT * FROM users WHERE users.tg_id = %s"
DB_SET_USER = "INSERT INTO users (tg_id, tg_uname, date, banned) VALUES (%s, %s, %s, %s)"
DB_BAN_USER = "UPDATE users SET users.banned = TRUE WHERE users.tg_id = %s"
DB_UNBAN_USER = "UPDATE users SET users.banned = FALSE WHERE users.tg_id = %s"
DB_CHECK_BANNED = "SELECT users.banned FROM users WHERE users.tg_id = %s"
DB_UPDATE_NAME = "UPDATE users SET users.tg_uname = %s WHERE users.tg_id = %s"
DB_GET_USER_BY_NAME = "SELECT * FROM users WHERE users.tg_uname = %s"
