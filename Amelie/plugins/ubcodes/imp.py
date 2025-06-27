from pyrogram import Client, filters
import psutil
import time
from datetime import timedelta
import logging

@Client.on_message(filters.command("start", prefixes=".") & filters.me)
async def start(client, message):
    await message.edit_text(f"{message.from_user.first_name} is alive")
    
bot_start_time = time.time()

logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.command(["ping", "alive"], prefixes=".") & filters.me)
async def ping(client, message):
    try:
        uptime_seconds = time.time() - bot_start_time
        uptime = str(timedelta(seconds=int(uptime_seconds)))

        ram = psutil.virtual_memory()
        ram_usage = f"{ram.percent}% used ({ram.used / (1024 ** 3):.2f} GB of {ram.total / (1024 ** 3):.2f} GB)"

        cpu_usage = f"{psutil.cpu_percent()}%"

        disk = psutil.disk_usage('/')
        disk_usage = f"{disk.percent}% used ({disk.used / (1024 ** 3):.2f} GB of {disk.total / (1024 ** 3):.2f} GB)"

        response = (
            f"**System Stats**\n"
            f"Uptime: {uptime}\n"
            f"RAM Usage: {ram_usage}\n"
            f"CPU Usage: {cpu_usage}\n"
            f"Disk Usage: {disk_usage}"
        )

        await message.edit_text(response)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        error_message = "An error occurred while retrieving system stats."
        await message.edit_text(error_message)
    
@Client.on_message(filters.command("help", prefixes=".") & filters.me)
async def help(client, message):
    response = (
        """**ᴛʜᴇsᴇ ᴀʀᴇ ᴛʜᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ᴜꜱᴇʀʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs:**

⦿ `.stats` ➠ ɢᴇᴛ ᴜꜱᴇʀꜱ ᴄʜᴀᴛ ꜱᴛᴀᴛꜱ.
⦿ `.pen` ➠ ᴡʀɪᴛᴇ ꜱᴏᴍᴇᴛɪɴɢ..
⦿ `.ask` ➠ ᴄʜᴀᴛ ɢᴘᴛ ᴀꜱᴋ ᴀɴʏ ᴛʜɪɴɢ.
⦿ `.ping` ➠ ᴄʜᴇᴄᴋ ʙᴏᴛ ᴜᴘ ᴛᴏ ᴛɪᴍᴇ & ʟᴏᴀᴅ.
⦿ `.tgm` ➠ ɢᴇᴛ ɪᴍɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ.
⦿ `.tgt` ➠ ɢᴇᴛ text ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ.
⦿ `.tr` ➠ ᴛʀᴀɴꜱʟᴀᴛᴇ ᴀɴʏ ʟᴀɴɢᴜᴀɢᴇ.
⦿ `.logo` ➠ ɴᴏʀᴍᴀʟ ʟᴏɢᴏ ɢᴇɴ.
⦿ `.info` ➠ ɢᴇᴛ ᴜꜱᴇʀɪᴅ / ᴜꜱᴇʀɴᴀᴍᴇ ᴛᴏ ᴜꜱᴇʀɪɴꜰᴏ
⦿ `.superban` ➠  ᴜsᴇʀɴᴀᴍᴇ/ᴜꜱᴇʀɪᴅ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ
⦿ `.superunban` ➠   ᴜsᴇʀɴᴀᴍᴇ/ᴜꜱᴇʀɪᴅ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ
⦿ `.gban` ➠  ᴜsᴇʀɴᴀᴍᴇ/ᴜꜱᴇʀɪᴅ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ
⦿ `.ungban` ➠   ᴜsᴇʀɴᴀᴍᴇ/ᴜꜱᴇʀɪᴅ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ
⦿ `.gmute` ➠  ᴜsᴇʀɴᴀᴍᴇ/ᴜꜱᴇʀɪᴅ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ
⦿ `.ungmute` ➠   ᴜsᴇʀɴᴀᴍᴇ/ᴜꜱᴇʀɪᴅ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ
⦿ `.ubgbanlist` ➠  sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴜʙ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀs.
⦿ `.id` ➠ ɢᴇᴛ ᴜꜱᴇʀ ɪᴅ
⦿ `.info` ➠ ɢᴇᴛ ᴜꜱᴇʀɪɴꜰᴏ ʙʏ ᴜꜱᴇʀɴᴀᴍᴇ/ᴜꜱᴇʀɪᴅ ᴏꜰ ᴜꜱᴇʀ
⦿ `.ginfo` ➠ ɢᴇᴛ ɢʀᴏᴜᴘɪɴꜰᴏ ʙʏ ᴜꜱᴇʀɴᴀᴍᴇ/ᴜꜱᴇʀɪᴅ ᴏꜰ ᴛʜᴇ ɢʀᴏᴜᴘ
⦿ `.stats` ➠  ɢᴇᴛ ᴜꜱᴇʀ ꜱᴛᴀᴛꜱ.
⦿ `.block` ➠  ᴛᴏ ʙʟᴏᴄᴋ ᴛᴇʟᴇɢʀᴀᴍ ᴜꜱᴇʀꜱ.
⦿ `.unblock` ➠ ᴛᴏ ᴏᴘᴇɴ ᴛʜᴇ ᴜꜱᴇʀ ʏᴏᴜ ʙʟᴏᴄᴋᴇᴅ.
⦿ `.leaveall` ➠ ʟᴇꜰᴛ ᴀʟʟ ɢʀᴏᴜᴘꜱ & ᴄʜᴀɴɴᴇʟꜱ
⦿ `.join` ➠ ᴛᴏ ᴊᴏɪɴ ᴄʜᴀᴛ ᴠɪᴀ ᴜꜱᴇʀɴᴀᴍᴇ/ᴜꜱᴇʀɪᴅ
⦿ `.pm` ➠  .pm @username hello hii.
⦿ `.admins` ➠  ɢᴇᴛ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴ ʟɪꜱᴛꜱ.
⦿ `.botlist` ➠  ɢᴇᴛ Bot ʟɪꜱᴛꜱ.
⦿ `.fban` ➠ .ꜰᴇᴅʙᴀɴ {ʀᴇᴀꜱᴏɴ} ᴛᴏ ꜰᴇᴅʙᴀɴ ꜱᴏᴍᴇᴏɴᴇ 
⦿ `.funban` ➠ .ꜰᴜɴʙᴀɴ {ʀᴇᴀꜱᴏɴ} ᴛᴏ ꜰᴜɴʙᴀɴ  ꜱᴏᴍᴇᴏɴᴇ
⦿ `.zombies` ➠  ʙᴀɴ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄ ꜰʀᴏᴍ ɢʀᴏᴜᴘ.
⦿ `.del` ➠  ᴛᴏ ᴅᴇʟᴇᴛᴇ ꜱᴘᴇᴄɪꜰɪᴄ ᴍᴇꜱꜱᴀɢᴇ.
⦿ `.ban` / `.unban` ➠  ʙᴀɴ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀ ᴀɴᴅ ᴜɴʙᴀɴ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀ.
⦿ `.mute` / `.unmute` ➠  ᴍᴜᴛᴇ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀ ᴀɴᴅ ᴜɴᴍᴜᴛᴇ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀ.
⦿ `.tmute` ➠  .tmute ᴜꜱᴇʀɴᴀᴍᴇ/ᴜꜱᴇʀɪᴅ 1ꜱ  ꜱ (ꜱᴇᴄᴏɴᴅ), ᴍ (ᴍɪɴᴜᴛᴇꜱ, ʜ (ʜᴏᴜʀꜱ, ᴅ (ᴅᴀʏꜱ) ᴀɴᴅ ʟᴀᴛᴇʀ ᴡɪʟʟ ᴜɴᴍᴜᴛᴇᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ 
⦿ `.pin` / `.unpin` ➠  ᴘɪɴ ᴍᴇꜱꜱᴇɢᴇ ᴀɴᴅ ᴜɴᴘɪɴ ᴍᴇꜱꜱᴇɢᴇ.
⦿ `.unpinall` ➠  ᴜɴᴘɪɴ ᴀʟʟ ᴍᴇꜱꜱᴇɢᴇ.
⦿ `.kick` ➠  ᴋɪᴄᴋ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀ.
⦿ `.promote` / `.fullpromote` ➠  ɴᴏʀᴍᴀʟ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇᴍʙᴇʀ ᴀɴᴅ ꜰᴜʟʟ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇᴍʙᴇʀ.
⦿ `.demote` ➠  ᴘʀᴏᴍᴏᴛᴇᴅ ᴀᴅᴍɪɴ ᴅᴇᴍᴏᴛᴇ.
⦿ `.purge` ➠ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴍᴇꜱꜱᴀɢᴇꜱ ꜰʀᴏᴍ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ.
⦿ `.vcmembers` ➠ ɢᴇᴛ ᴠᴄ ᴍᴇᴍʙᴇʀꜱ ᴄᴏᴜɴᴛꜱ.
⦿ `.vcend` ➠ ᴇɴᴅ ᴛʜᴇ ᴠᴄ.
⦿ `.vcstart` ➠ ꜱᴛᴀʀᴛ ᴛʜᴇ ᴠᴄ.
⦿ `.vclink` ➠ ɢᴇᴛ ᴠᴄ ʟɪɴᴋ ᴏɴʟʏ ꜰᴏʀ ᴘᴜʙʟɪᴄ ɢʀᴏᴜᴘ .
⦿ `.banall` ➠  ʙᴀɴᴀʟʟ ᴍᴇᴍʙᴇʀꜱ ɪɴ ɢʀᴏᴜᴘꜱ.
⦿ `.forcebanall` ➠  ʙᴀɴ ᴀʟʟ ʙᴏᴛʜ ᴀᴅᴍɪɴꜱ ᴀɴᴅ ᴍᴇᴍʙᴇʀꜱ ꜰʀᴏᴍ ɢʀᴏᴜᴘ (ᴏɴʟʏ ꜰᴏʀ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ) .
⦿ `.unbanall` ➠  ᴜɴʙᴀɴᴀʟʟ ᴍᴇᴍʙᴇʀꜱ ɪɴ ɢʀᴏᴜᴘꜱ.
⦿ `.muteall` ➠  ᴍᴜᴛᴇ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ ɪɴ ɢʀᴏᴜᴘꜱ.
⦿ `.unmuteall` ➠  ᴜɴᴍᴜᴛᴇ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ ɪɴ ɢʀᴏᴜᴘꜱ.
⦿ `.kickall` ➠  ᴋɪᴄᴋᴀʟʟ ᴍᴇᴍʙᴇʀꜱ ɪɴ ɢʀᴏᴜᴘꜱ.
⦿ `.botall` ➠  ʙᴏᴛ ᴀᴅᴅ ᴀʟʟ ɢʀᴏᴜᴘꜱ ᴀᴜᴛᴏ (ᴏᴡɴᴇʀ).
⦿ `.allclient` ➠ ɢᴇᴛ ᴀʟʟ ᴛᴇᴀᴍ ᴍᴇᴍʙᴇʀꜱ ʟɪꜱᴛ (ᴏᴡɴᴇʀ).
⦿ `.setdesc` ➠  ꜱᴇᴛ ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ ᴏɴ ɢʀᴏᴜᴘ 
⦿ `.settitle` ➠ ꜱᴇᴛ ᴛɪᴛᴛʟᴇ ᴏɴ ɢʀᴏᴜᴘ.
⦿ `.bancodes` ➠ ᴛᴏ ɢᴇᴛ ᴛᴇᴀᴍ ʙᴀɴᴄᴏᴅᴇꜱ
⦿ `/start` ➠  ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴅᴏ ɪᴛ ᴇᴠᴇʀʏᴛɪᴍᴇ ᴡʜᴇɴᴇᴠᴇʀ ʏᴏᴜ ᴡɪʟʟ ᴄᴏᴍᴇ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴊᴜꜱᴛ ᴠɪꜱɪᴛ ᴛʜᴇ ᴅᴍ/ᴘᴍ ᴏꜰ ᴘᴀʀᴇɴᴛᴀʟ ʙᴏᴛ <a href="https://t.me/aronaYbot/43">Aʀᴏɴᴀ 爱</a> ᴀɴᴅ ᴛʏᴘᴇ /startub.
⦿ `.spam` ➠ ❱ ᴄʟɪᴄᴋ ᴛᴏ ɢᴇᴛ ᴛᴜᴛᴏʀɪᴀʟꜱ  <a href="https://t.me/arona_update/43">[ ᴄʟɪᴄᴋ ʜᴇʀᴇ] </a>
⦿ `.fspam` ➠ ❱ ᴄʟɪᴄᴋ ᴛᴏ ɢᴇᴛ ᴛᴜᴛᴏʀɪᴀʟꜱ  <a href="https://t.me/arona_update/44">[ ᴄʟɪᴄᴋ ʜᴇʀᴇ] </a> 
⦿ `.nspam` ➠ ❱ ᴄʟɪᴄᴋ ᴛᴏ ɢᴇᴛ ᴛᴜᴛᴏʀɪᴀʟꜱ  <a href="https://t.me/arona_update/45">[ ᴄʟɪᴄᴋ ʜᴇʀᴇ] </a>
⦿ `.plist` ➠ ❱ ᴄʟɪᴄᴋ ᴛᴏ ɢᴇᴛ ᴛᴜᴛᴏʀɪᴀʟꜱ  <a href="https://t.me/arona_update/26">[ ᴄʟɪᴄᴋ ʜᴇʀᴇ] </a>
⦿ `.broadcast` ➠  ❱ ᴄʟɪᴄᴋ ᴛᴏ ɢᴇᴛ ᴛᴜᴛᴏʀɪᴀʟꜱ  <a href="https://t.me/arona_update/48">[ ᴄʟɪᴄᴋ ʜᴇʀᴇ] </a>
⦿ `.leave` ➠  ❱ ᴄʟɪᴄᴋ ᴛᴏ ɢᴇᴛ ᴛᴜᴛᴏʀɪᴀʟꜱ  <a href="https://t.me/arona_update/48">[ ᴄʟɪᴄᴋ ʜᴇʀᴇ] </a>
⦿ `.copyright` ➠ ❱ ᴄʟɪᴄᴋ ᴛᴏ ɢᴇᴛ ᴛᴜᴛᴏʀɪᴀʟꜱ  <a href="https://t.me/arona_update/47">[ ᴄʟɪᴄᴋ ʜᴇʀᴇ] </a> ."""
    )
    
    await message.edit_text(response)