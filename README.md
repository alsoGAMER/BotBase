# BotBase

BotBase is a collection of plugins that use [Pyrogram's](https://github.com/pyrogram/pyrogram) API to make Telegram bot development extremely easy.

### Disclaimer

BotBase requires a solid knowledge of pyrogram and of the Telegram MTProto API itself, you can check pyrogram's docs [here](https://docs.pyrogram.org)

The author of this project assumes that the reader is not completely computer illiterate, this project is thought for smart people that want to develop better bots faster, it is **not** a beginner's friendly thing.

Also, you need to know how to host a bot yourself. I mean, I coded all of this for you already, make some effort!

## BotBase - Setup

To set up a project using BotBase, follow this step-by-step guide (assuming `pip` and `git` are already installed and up to date):

- Open a terminal and type `git clone https://github.com/alsoGAMER/BotBase`
- `cd` into the newly created directory and run `python3 -m pip install -r requirements.txt`
- Once that is done, copy `BotBase/config.example.py` as `config.py` and edit your `config.py` module with a text editor and start changing the default settings
- The first thing you might want to do is change the `API_ID`, `API_HASH`, and `BOT_TOKEN` global variables. Check [this page](https://my.telegram.org/apps) and log in with your Telegram account to create an `API_ID`/`API_HASH` pair by registering a new application. For the bot token, just create one with [BotFather](https://telegram.me/BotFather).

**Note**: The configuration file is still a python file and when it will be imported any python code that you typed inside it will be executed, so be careful! If you need to perform pre-startup operations it is advised to do them in the `if __name__ == "main":` block inside `bot.py`, before `bot.start()`

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

Most of the working of the module is pre-defined, but you can customize the texts that the bot will use in the appropriate section of `config.py`


### Plugins - Admin

This is the administrative module for the bot, and it also has its section in the `config.py` file.

To configure this plugin, go to the appropriate section in `config.py` and change the default values in the `ADMINS` dictionary. Do **NOT** change the value of `ADMINS`, just update the dictionary as follows:

- Use the admin's Telegram ID as a key
- As a value choose the name that the users will see when that admin joins a chat


The available commands are:

- `/getuser ID`: Fetches user information by its Telegram ID
- `/getranduser`: Fetches a random user from the database
- `/ban ID`: Bans a user from using the bot, permanently
- `/unban ID`: Unbans a user from using the bot
- `/count`: Shows the current number of registered users
- `/global msg`: Broadcast `msg` to all users, supports HTML and markdown formatting
- `/whisper ID msg`: Send `msg` to a specific user given its ID. HTML and markdown formatting supported
- `/update ID`: Updates the user's info in the database, if they've changed
- `/busy`: Sets your admin status as busy/not busy to silence/unsilence support requests to you
- `/userbyname`: Same as `getuser`, but takes a username (case-insensitive, with or without the @) as input. Note that if the database contains multiple users with the same username, due to old data, for instance, only the first entry is returned.

### Plugins - Antiflood

The antiflood plugin is a well-designed protection system that works by accumulating a fixed number of messages from a user and then subtract their timestamps in groups of 2.

To configure this plugin and to know more about how it works, check the appropriate section in `config.py`

### Plugins - Start

This module is simple, it will reply to private messages containing the /start command with a pre-defined greeting and inline buttons

To configure it, check its section in the `config.py` file


## Extending the default functionality

Extending BotBase's functionality is easy, just create a pyrogram smart plugin in the `BotBase/modules` section, and you're ready to go!

If you don't know what a smart plugin is, check [this link](https://docs.pyrogram.org/topics/smart-plugins) from pyrogram's official documentation to know more.

There are some things to keep in mind, though:

- If you want to protect your plugin from flood, import the `BotBase.modules.antiflood.BANNED_USERS` filter (basically a `Filters.user()` object) and use it like this: `~BANNED_USERS`. This will restrict banned users from reaching your handler at all.
Please note that users banned with the `/ban` command are filtered with the custom filter `BotBase.config.user_banned`!
- To avoid repetition with try/except blocks, BotBase implements a wrapper object that performs automatic exception handling and log to the console, check the `METHODS.md` file in this repo to know more
- Nothing restricts you from changing how the default plugins work, but this is not advised. The default plugins have been designed to cooperate and breaking this might lead to obscure tracebacks and errors that are hard to debug.
- BotBase also has many default methods to handle database interaction, check the `DATABASE.md` file in this repo to know more


## License

This project is licensed under the Apache 2 License.<br/> 
License terms are available [here](https://github.com/alsoGAMER/BotBase/blob/master/LICENSE).

## Note

This is a fork of Nocturn9x's [BotBase](https://github.com/nocturn9x/BotBase).