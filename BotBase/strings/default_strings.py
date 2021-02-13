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

# region Flood Strings
from BotBase.config import BAN_TIME

FLOOD_NOTICE = f"🤙 <b>Hey buddy!</b>\n🕐 Relax! You have been banned for {BAN_TIME / 60:.1f} minutes"
# If you want the user to be notified of being flood-blocked, set this to the desired message, False to disable
FLOOD_CLEARED = "♻️ Antiflood table cleaned up"
FLOOD_USER_CLEARED = "♻️ Antiflood table for<code>{user}</code> cleaned up"
TOO_FAST = "✋ Calm down! Try again later"
# endregion

# region Greet Buttons Strings
SUPPORT_BUTTON = "💭 Support Chat"
# The text for the button that triggers the live chat
BACK_BUTTON = "🔙 Back"
# The text for the 'Back' button
ABOUT_BUTTON = "ℹ About"
# The text for the 'About' button
# endregion

# region Livechat Strings
MARKED_BUSY = "🎲 You're now busy, resend /busy to reset this state"
UNMARKED_BUSY = "✍ You'll now receive support requests again"
CLOSE_CHAT_BUTTON = "❌ Close chat"
UPDATE_BUTTON = "🔄 Update"
ADMIN_ACCEPTED_CHAT = "✅ {admin} has joined the chat with {user}"
USER_LEFT_QUEUE = "⚠️ {user} left the queue"
QUEUE_LIST = "🚻 List of users waiting\n\n{queue}"
CHATS_LIST = "💬 List of users in chat\n\n{chats}"
ADMIN_BUSY = "(Busy)"
SUPPORT_NOTIFICATION = "🔔 New support request!\n\n{uinfo}"
ADMIN_JOINS_CHAT = " [{admin_name}]({admin_id}) joined the chat!"
USER_CLOSES_CHAT = "🔔 [{user_name}]({user_id}) closed the chat"
USER_LEAVES_CHAT = "✅ You left the chat"
USER_JOINS_CHAT = "✅ You've joined the chat"
CHAT_BUSY = "⚠️ Another admin has already joined"
LEAVE_CURRENT_CHAT = "⚠️ Close current chat first!"
CANNOT_REQUEST_SUPPORT = "⚠️ You can't start a chat!"
SUPPORT_REQUEST_SENT = "✅ You're now in the queue, wait for an admin to answer you\n\n" \
                       "🔄 <b>Admins available</b>\n{queue}\n<b>Updated on</b>: <code>{date}</code>\n\n<b>Note</b>: " \
                       "<i>If there are no admins available at the moment, press the 'Update' button every now and " \
                       "then to find out if a seat is available!</i>"
JOIN_CHAT_BUTTON = "❗ Join the chat"
# endregion

# region User Interaction Strings
USER_INFO_UPDATED = "✅ <i>Information updated</i>"
USER_INFO_UNCHANGED = "❌ <b>I haven't detected any changes for this user</b>"
USER_BANNED = "✅ <b>User banned successfully</b>"
USER_UNBANNED = "✅ <b>User unbanned successfully</b>"
YOU_ARE_UNBANNED = "✅ <b>You've been unbanned</b>"
USER_NOT_BANNED = "❌ <b>This user isn't banned</b>"
USER_ALREADY_BANNED = "❌ <b>This user is already banned</b>"
YOU_ARE_BANNED = "❌ <b>You've been banned</b>"
# endregion

# region Whisper Strings
WHISPER_FROM = "📣 <b>Message from</b> {admin}: {msg}"
WHISPER_SUCCESSFUL = "✅ <b>Sent successfully</b>"
# endregion

# region Misc Strings
YES = "Yes"
NO = "No"
# endregion

# region Error Strings
CANNOT_BAN_ADMIN = "❌ <b>Error</b>: This user is an administrator"
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
# endregion
