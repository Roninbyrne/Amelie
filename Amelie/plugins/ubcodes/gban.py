from pyrogram import Client, filters
from Amelie import app
import asyncio
import logging
from config import API_ID, API_HASH
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pytz import timezone
from datetime import timedelta, datetime
import base64
from Amelie.core.userbot import userbot_clients 

reason_storage = {}
next_reason_id = 1

def store_reason(reason):
    global next_reason_id
    reason_id = next_reason_id
    reason_storage[reason_id] = reason
    next_reason_id += 1
    return reason_id

def get_readable_time(delta: timedelta) -> str:
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

AUTHORS = [7337748194, 7202110938, 7512713188, 1813320767]
SUPPORT_CHAT_ID = -1002408883218
SUPPORT_CHANNEL_ID = -1002059806687

async def get_user_id(user_query):
    try:
        if user_query.isdigit():
            return int(user_query)
        user_query = user_query.lstrip('@')
        user = await app.get_users(user_query)
        return user.id
    except Exception as e:
        logging.error(f"Error fetching user ID for {user_query}: {e}")
        return None

async def send_request_message(user, reason, action, message):
    reason_id = store_reason(reason) if reason else None

    chat_name = message.chat.title if message.chat.title else "Private Chat"
    chat_id = message.chat.id
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    encoded_reason = base64.b64encode(str(reason_id).encode()).decode() if reason_id else ""

    request_message = await app.send_message(
        SUPPORT_CHAT_ID,
        f"""ᴀᴘᴘʀᴏᴠᴇ ɢʟᴏʙᴀʟʙᴀɴ ꜰᴏʀ ᴜꜱᴇʀ :
{user.first_name}
ᴜꜱᴇʀ ɪᴅ : {user.id}

ʀᴇQᴜᴇꜱᴛ ꜰʀᴏᴍ ᴄʜᴀᴛ ɪᴅ : {chat_id}
ʀᴇQᴜᴇꜱᴛ ꜰʀᴏᴍ ᴄʜᴀᴛ ɴᴀᴍᴇ : {chat_name}

ʀᴇᴀꜱᴏɴ : {reason if reason else "No reason provided"}

ʀᴇQᴜᴇꜱᴛ ʙʏ : {message.from_user.first_name}

ᴅᴀᴛᴇ & ᴛɪᴍᴇ : {ind_time}
ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {utc_time}

ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @AronaYbot
        """,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✯ ᴀᴘᴘʀᴏᴠᴇ ✯", callback_data=f"{action}_approve_{user.id}_{encoded_reason}")],
            [InlineKeyboardButton("✯ ᴅᴇᴄʟɪɴᴇ ✯", callback_data=f"{action}_decline_{user.id}_{encoded_reason}")]
        ])
    )
    return request_message

@Client.on_message(filters.command(["gban"], prefixes=["."]) & (filters.group | filters.channel | filters.private) & filters.me)
async def global_ban(_, message):
    reason = None
    user_id = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        reason = message.reply_to_message.text
    else:
        msg_parts = message.text.split(None, 1)
        if len(msg_parts) > 1:
            user_query = msg_parts[1].split()[0]
            user_id = await get_user_id(user_query)
            reason = " ".join(msg_parts[1].split()[1:]) if len(msg_parts[1].split()) > 1 else None

    if user_id is None:
        await message.reply("Please specify a user ID, username, or reply to a message.")
        return

    try:
        user = await app.get_users(user_id)
    except Exception as e:
        logging.error(f"Error fetching user with ID {user_id}: {e}")
        await message.reply("User not found or inaccessible.")
        return

    request_message = await send_request_message(user, reason, "Global_Ban", message)
    utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    response_message = f"""ʏᴏᴜʀ ɢʟᴏʙᴀʟʙᴀɴ ʀᴇQᴜᴇꜱᴛ ʜᴀꜱ ʙᴇᴇɴ ꜱᴇɴᴅᴇᴅ ᴛᴏ ᴛᴇᴀᴍ

ʀᴇQᴜᴇꜱᴛ ᴛᴏ ɢʟᴏʙᴀʟʙᴀɴ
ᴜꜱᴇʀ : {user.first_name}

ʀᴇᴀꜱᴏɴ : {reason if reason else "No reason provided"}

ʀᴇQᴜᴇꜱᴛ ʙʏ : {message.from_user.first_name}

ʏᴏᴜʀ ʀᴇQᴜᴇꜱᴛ ᴡɪʟʟ ʙᴇ ᴄʜᴇᴄᴋᴇᴅ ᴀɴᴅ ɪꜰ ɪᴛ'ꜱ ɢᴇɴᴜɪɴ ᴛʜᴇɴ ʙᴇ ꜱᴜʀᴇ ɪᴛ ᴡɪʟʟ ʙᴇ ᴀᴘᴘʀᴏᴠᴇᴅ.
ᴛʜᴀɴᴋꜜs ꜰᴏʀ ʏᴏᴜʀ ɢʟᴏʙᴀʟʙᴀɴ ʀᴇQᴜᴇꜱᴛ

ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {utc_time}

ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ : @TeamArona

ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @AronaYbot"""

    response_msg = await message.reply(response_message)
    await message.delete()
    await asyncio.sleep(10)
    try:
        await response_msg.delete()
    except Exception as e:
        logging.error(f"Failed to delete response message: {e}")

@app.on_callback_query(filters.regex(r'^Global_Ban_(approve|decline)_(\d+)_(.*)$'))
async def handle_global_ban_callback(client: Client, query: CallbackQuery):
    try:
        data_parts = query.data.split("_")
        if len(data_parts) != 5:
            raise ValueError("Callback data format is incorrect")

        action = data_parts[1]
        status = data_parts[2]
        user_id_str = data_parts[3]
        user_id = int(user_id_str)
        reason_id = base64.b64decode(data_parts[4]).decode()
        reason = reason_storage.get(int(reason_id), "No reason provided")

        user = await app.get_users(user_id)

    except ValueError as e:
        logging.error(f"Error parsing callback data: {e}")
        await query.answer("Failed to process request. Please try again.", show_alert=True)
        return
    except Exception as e:
        logging.error(f"Error fetching user details: {e}")
        await query.answer("Error retrieving user information.", show_alert=True)
        return

    if query.from_user.id not in AUTHORS:
        await query.answer("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴜᴛʜᴏʀ", show_alert=True)
        return

    approval_author = query.from_user.first_name

    try:
        if status == "approve":
            await query.answer("ɢʟᴏʙᴀʟʙᴀɴ ᴀᴘᴘʀᴏᴠᴇᴅ.", show_alert=True)
            asyncio.create_task(global_ban_action(user_id, query.message, approval_author, reason))

            approved_message = f"""ʏᴏᴜʀ ɢʟᴏʙᴀʟʙᴀɴ ʀᴇQᴜᴇꜱᴛ ʜᴀꜱ ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ, ɴᴏᴡ ꜱᴛᴀʀᴛɪɴɢ ɢʟᴏʙᴀʟʙᴀɴ.....

ʀᴇQᴜᴇꜱᴛ  ᴛᴏ ɢʟᴏʙᴀʟʙᴀɴ
ᴜꜱᴇʀ : {user.first_name}

ʀᴇᴀꜱᴏɴ : {reason}
ᴀᴘᴘʀᴏᴠᴇᴅ ʙʏ ᴀᴜᴛʜᴏʀ  {approval_author}

ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}

ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ : @TeamArona
ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @AronaYbot"""
            await query.message.edit(approved_message)
            notify = await app.send_message(SUPPORT_CHAT_ID, f"ɢʟᴏʙᴀʟʙᴀɴ ᴀᴘᴘʀᴏᴠᴇᴅ ʙʏ {approval_author}.")
            await asyncio.sleep(10)
            await query.message.delete()
            await notify.delete()

        elif status == "decline":
            await query.answer("ɢʟᴏʙᴀʟʙᴀɴ ᴅᴇᴄʟɪɴᴇᴅ.", show_alert=True)

            declined_message = f"""ʏᴏᴜʀ ɢʟᴏʙᴀʟʙᴀɴ ʀᴇQᴜᴇꜱᴛ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇᴄʟɪɴᴇᴅ 

ʀᴇQᴜᴇꜱᴛ  ᴛᴏ ɢʟᴏʙᴀʟʙᴀɴ
ᴜꜱᴇʀ : {user.first_name}

ʀᴇᴀꜱᴏɴ : {reason}
ᴅᴇᴄʟɪɴᴇᴅ ʙʏ ᴀᴜᴛʜᴏʀ  {approval_author}

ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}

ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ : @TeamArona
ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @AronaYbot"""
            await query.message.edit(declined_message)
            notify = await app.send_message(SUPPORT_CHAT_ID, f"ɢʟᴏʙᴀʟʙᴀɴ ᴅᴇᴄʟɪɴᴇᴅ ʙʏ {approval_author}.")
            await asyncio.sleep(10)
            await query.message.delete()
            await notify.delete()

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await query.answer("An unexpected error occurred. Please try again.", show_alert=True)

async def global_ban_action(user_id, message, approval_author, reason):
    try:
        logging.info(f"Starting global ban action for user ID {user_id}...")
        user = await app.get_users(user_id)

        number_of_chats = 0
        start_time = datetime.utcnow()

        async def ban_user_in_all_chats(client):
            nonlocal number_of_chats
            async for dialog in client.get_dialogs():
                try:
                    await client.ban_chat_member(dialog.chat.id, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1.5)
                except Exception as e:
                    logging.warning(f"[{client.me.id}] Failed to ban in {dialog.chat.id}: {e}")

        tasks = [ban_user_in_all_chats(client) for client in userbot_clients]
        await asyncio.gather(*tasks)

        end_time = datetime.utcnow()
        time_taken = end_time - start_time
        readable_time = get_readable_time(time_taken)

        final_message = f"""
ɢʟᴏʙᴀʟʙᴀɴ ɪꜱ ᴄᴏᴍᴘʟᴇᴛᴇᴅ.

ᴜꜱᴇʀ : {user.first_name}
ᴜꜱᴇʀ ɪᴅ : {user.id}

ʀᴇᴀꜱᴏɴ : {reason}
ᴛᴏᴛᴀʟ ʙᴀɴ ɪɴ ꜰᴇᴅꜱ : {number_of_chats}

ᴀᴘᴘʀᴏᴠᴇᴅ ʙʏ : {approval_author}

ᴜɴɪᴠᴇʀꜱᴀʟ ᴛɪᴍᴇ : {end_time.strftime('%Y-%m-%d %H:%M:%S')}
ᴛɪᴍᴇ ᴛᴀᴋᴇɴ : {readable_time}

ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ : @TeamArona
ᴘᴏᴡᴇʀᴇᴅ ʙʏ : @AronaYbot"""

        await app.send_message(SUPPORT_CHANNEL_ID, final_message)

    except Exception as e:
        logging.error(f"Error during global ban action for user ID {user_id}: {e}")
