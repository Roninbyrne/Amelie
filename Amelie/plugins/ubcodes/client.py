from pyrogram import Client, filters
from config import OWNER_ID
import time
import logging

@Client.on_message(filters.command("client",".") & filters.user(OWNER_ID))
async def start(client, message):
    await message.reply_text(f"Client is alive")
    
    await message.delete()

bot_start_time = time.time()

logging.basicConfig(level=logging.INFO)