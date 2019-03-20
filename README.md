# InstagramPostBot
Automatically share instagram's posts on Telegram.

How to use:

First clone the repository using `git clone https://github.com/unizLike/InstagramPostBot && cd InstagramPostBot`
Then you need to install the required dependencies with `pip install -r requirements.txt`

Open `settings.py` file and edit the following fields:
 - Put your username in `USERNAME` field. Note that the account must be public, otherwise this bot won't work.
 - Put the bot token in `BOT_TOKEN` field. You can obtain this from [
](https://t.me/BotFather) on Telegram
 - Put the chat_id in `CHAT_ID` field. The bot must has permissions to send message in the desired chat_id, otherwise an error will be raised.

In order to start the bot, use `python3 .` command.
