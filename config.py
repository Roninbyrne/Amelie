import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

# Load environment variables from .env file
load_dotenv()

# Telegram API credentials (from https://my.telegram.org)
API_ID = 20948356
API_HASH = "6b202043d2b3c4db3f4ebefb06f2df12"

# Bot token from @BotFather
BOT_TOKEN = "7964387907:AAHpPVsxt7ep99o-cZFgWOqsYZlWLAKCGtQ"

# MongoDB connection string
MONGO_DB_URI = "mongodb+srv://Combobot:Combobot@combobot.4jbtg.mongodb.net/?retryWrites=true&w=majority&appName=Combobot"

# --------------start.py-------------

START_VIDEO = "https://i.ibb.co/nsyp67FS/Img2url-bot.jpg"
HELP_MENU_VIDEO = "https://i.ibb.co/Z64Z3yCR/Img2url-bot.jpg"
HELP_VIDEO_1 = "https://i.ibb.co/8gkx23jt/Img2url-bot.jpg"
HELP_VIDEO_2 = "https://i.ibb.co/S7Z4fHJt/Img2url-bot.jpg"
HELP_VIDEO_3 = "https://unitedcamps.in/Images/file_11453.jpg"
HELP_VIDEO_4 = "https://unitedcamps.in/Images/file_11454.jpg"

#------------------------------------

LOGGER_ID = -1002059639505
STATS_VIDEO = "https://unitedcamps.in/Images/file_5250.jpg"
OWNER_ID = 7394132959

# Heroku deployment
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# GitHub repo
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/Roninbyrne/Amelie-bot")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")
GIT_TOKEN = getenv("git_token", None)

# Support
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/PacificArc")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/phoenixXsupport")

# Validate URLs
if SUPPORT_CHANNEL:
    if not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit("[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://")

if SUPPORT_CHAT:
    if not re.match(r"(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit("[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://")