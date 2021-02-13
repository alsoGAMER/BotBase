# BotBase

BotBase is a collection of plugins that use [Pyrogram's](https://github.com/pyrogram/pyrogram) API to make Telegram bot development extremely easy.

### Disclaimer

BotBase requires a solid knowledge of pyrogram and of the Telegram MTProto API itself, you can check pyrogram's docs [here](https://docs.pyrogram.org)

The author of this project assumes that the reader is not completely computer illiterate, this project is thought for smart people that want to develop better bots faster, it is **not** a beginner's friendly framework.

Also, you need to know how to host a bot yourself. I mean, I coded all of this for you already, make some effort!

## BotBase - Setup

To set up a project using BotBase, follow this step-by-step guide (assuming `pip` and `git` are already installed and up to date):

- Open a terminal and type `git clone https://github.com/alsoGAMER/BotBase`
- `cd` into the newly created directory and run `python3 -m pip install -r requirements.txt`
- Once that is done, copy `BotBase/config.example.py` as `config.py` and edit your `config.py` module with a text editor and start changing the default settings
- The first thing you might want to do is change the `API_ID`, `API_HASH`, and `BOT_TOKEN` global variables. Check [this page](https://my.telegram.org/apps) and log in with your Telegram account to create an `API_ID`/`API_HASH` pair by registering a new application. For the bot token, just create one with [BotFather](https://t.me/BotFather).

**Note**: The configuration file is still a python file, and when it will be imported any python code that you typed inside it will be executed, so be careful.
If you need to perform pre-startup operations it is advised to do them in the `if __name__ == "main":` block inside `bot.py`, before `bot.run()`

Once you're done configuring, move to the top-level directory of the project and run `python3 bot.py`

## BotBase - Plugins

BotBase comes with lots of default plugins and tools to manage database interaction.

As of now, the following plugins are active:

- An advanced live chat accessible through buttons
- A start module that simply replies to /start and adds the user to the database if not already present
- A highly customizable antiflood module 
- An administration module with lots of pre-built features such as /global and /whisper


### Plugins - Live Chat

The live-chat is probably the most complicated plugin because it needs to save the user's status and takes advantage of custom filters to
work properly. To customize this plugin, go to the appropriate section in `config.py` and edit the available options at your heart's desire.

This plugin works the following way:

- When a user presses the button to trigger the live chat, all admins get notified that user xyz is asking for support
- The notification will contain the user information such as ID and username, if available
- At the same time, the user will see a waiting queue. Available admins will be shown with a green sphere next to their name, while admins that are already chatting will be shown as busy
- The user can press the update button to update the admin's statuses
- When an administrator joins, all notifications from all admins are automatically deleted, and the admin is marked as busy
- When an admin joins a chat, other admins won't be able to join
- Admins that are busy will not receive other support notifications
- An admin cannot join a chat if it's already busy

Most of the working of the module is pre-defined, but you can customize the texts that the bot will use in the appropriate section of `strings/default_strings.py`


### Plugins - Admin

This is the administrative module for the bot, and it also has its section in the `config.py` file.

To configure this plugin, go to the appropriate section in `config.py` and change the default values in the `ADMINS` dictionary. Do **NOT** change the value of `ADMINS`, just update the dictionary as follows:

- Use the admin's Telegram ID as a key
- As a value choose the name that the users will see when that admin joins a chat


The available commands are:

__Note__: ID can either be a Telegram User ID or a Telegram username (with or without the trailing @, case-insensitive)

__Note__: Arguments marked with square brackets are optional

- `/getuser ID`: Fetches information about the given user
- `/getranduser`: Fetches a random user from the database
- `/ban ID`: Bans a user from using the bot, permanently
- `/unban ID`: Unbans a user from using the bot
- `/count`: Shows the current number of registered users
- `/global msg`: Broadcast `msg` to all users, supports HTML and markdown formatting
- `/whisper ID msg`: Send `msg` to a specific user. HTML and markdown formatting supported
- `/update ID`: Updates the user's info in the database, if they've changed
- `/busy`: Sets your admin status as busy/not busy to silence/unsilence support requests to you
- `/clearflood [ID]` - Clears the antiflood local storage. If a user ID is given, only that user's cache is purged, otherwise the whole module-level cache is reset-

__Warning__: Altough acting on users by their username is supported, it is not recommended. Users can change their name, and the bot wouldn't detect
this change until you send the `/update` command. A telegram user can never change its ID (without deleting his own account) so that's way more reliable!

### Plugins - Antiflood

The antiflood plugin is a well-designed and optimized floodwait protection system that works by accumulating a fixed number of messages from a user and then subtract their timestamps in groups of 2. You can choose whether to delete messages after a flood is detected, to act upon admins (or not) and send a custom
notification to the perpetrator. Please note that this system only works in private chats, but its filters can be easily changed. Also, its handler priority
is set to -1, so that it is the first handler to run: take this into account when you extend BotBase's functionality.

__Warning__: This module has been designed to protect _the bot_ from getting floodwait exceptions from Telegram. It has been thoroughly designed and tested to achieve exactly this purpose. The antiflood _might_ work well to protect groups from flood, but it is not guaranteed. Just because it can avoid floodwaits, it doesn't mean it uses the best approach to handle a lot of users flooding at the same time in a public group!

To configure this plugin and to know more about how it works, check the appropriate section in `config.py`

### Plugins - Start

This module is simple: it will reply to private messages containing the /start command with a pre-defined greeting and inline buttons

To configure it, check its section in the `config.py` file


## Extending the default functionality

Extending BotBase's functionality is easy, just create a pyrogram smart plugin in the `BotBase/modules` section, and you're ready to go!

If you don't know what a smart plugin is, check [this link](https://docs.pyrogram.org/topics/smart-plugins) from pyrogram's official documentation to know more.

There are some things to keep in mind, though:

- If you want to protect your plugin from flood, import the `BotBase.modules.antiflood.BANNED_USERS` filter (basically a `Filters.user()` object) and use it like this: `~BANNED_USERS`. This will restrict banned users from reaching your handler at all.
Please note that users banned with the `/ban` command are filtered with the custom filter `BotBase.methods.custom_filters.user_banned`!
- To avoid repetition with try/except blocks, BotBase implements a wrapper object that performs automatic exception handling and log to the console, check the `METHODS.md` file in this repo to know more
- Nothing restricts you from changing how the default plugins work, but this is not advised. The default plugins have been designed to cooperate and breaking this might lead to obscure tracebacks and errors that are hard to debug.
- BotBase also has many default methods to handle database interaction, check the `DATABASE.md` file in this repo to know more


## License

This project is licensed under the Apache 2 License.<br/> 
License terms are available [here](https://github.com/alsoGAMER/BotBase/blob/master/LICENSE).

## Note

This is a fork of Nocturn9x's [BotBase](https://github.com/nocturn9x/BotBase).
