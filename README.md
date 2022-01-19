# girl friend helper telegram bot 🦔

[![Telegram](https://img.shields.io/badge/telegram-ready-brightgreen.svg)](https://t.me/girlfriendhelper_bot)

A telegram bot to help my girlfriend with tasks like being more punctual.

## Why this project
The main motivation for creating this project was that my girlfriend would frequently be late when we went out and this was a big deal of frustration for me as I would often be the one waiting for her. 

## Features
- Calculates sleep and wake times using the [90 minute rule](https://www.youtube.com/watch?v=Ewajc2eXZr0) `/sleep` 
- Time calculator so estimate when to leave the house `/est`


 More features in the works!
- [ ] Scheduled telegram reminders
- [ ] Route planner
- [ ] random hedgehog pictures (because my girlfriend loves hedgehogs) 


🐛 Found a bug?
file an issue [here](https://github.com/shawnlimjunhe/gfhelper_bot/issues)

---

### Testing gfhelper_bot locally
This guide assumes that you already have git and python 3.9 installed. 
To check whether you have git and python installed properly:

```bash
$ git --version
```

```bash
$ python --version
```

### 1. Clone the gfhelper_bot locally
Go the the directory where you want to store the cinnabot code, and run this command to download the gfhelper_bot repository into a new directory called 'gfhelper_bot' or any name of your choosing: 

```bash
$ git clone https://github.com/shawnlimjunhe/gfhelper_bot.git
```

### 2. Install the required python libraries
To run this bot, we will need to install two python libraries
1) python-telegram-bot
2) python-dotenv

[python-telegram-bot](https://pypi.org/project/python-telegram-bot/) [(github)](https://github.com/python-telegram-bot/python-telegram-bot) is a Python wrapper for the [Telegram Bot API](https://core.telegram.org/bots/api) and simplifies the development of Telegram bots using Python. 

To install python-telegram-bot using pip, run:
```bash
$ pip install python-telegram-bot
```

[python-dotenv](https://pypi.org/project/python-dotenv/) allows us to read key-value pairs from a `.env` file.

To install python-dotenv using pip, run:
```bash
$ pip install python-dotenv
```

### 3. Register for an API token with Botfather
Pay your respects to [Botfather](https://t.me/botfather) 

To create your own bot, send the following commands to BotFather

1) /start
2) /newbot

After naming your bot (non-unique) and giving it username (must be unique), Botfather will give your an API token.

### 4. Create a `.env` file
In the gfhelper_bot root directory, create a `.env` file using the following command

```
# unix
$ cp .env.example .env

# windows
$ copy .env.example .env
```


Load up your IDE of choice and replace the dummy API token with the API token that you have just created.

### 5. Running the script
```bash
$ python main.py
```

Your bot should be running! Open up telegram and search for your bot with the username that you gave and have fun! 

When you're done, press <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop the bot.

Hope that it helps your significant other too! 🦔

#### 5.1 Enabling Developer error messages
To allow the bot to send error logs to you, obtain your chat_id by paste the following code at the end of any command
```
print(update.effective_chat.id)
```

Paste the following into the `.env` file:
```
DEVELOPER_CHAT_ID = YOUR_CHAT_ID
```

---
Licensed under the [MIT License](LICENSE)