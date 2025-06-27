from pyrogram import Client, filters
from Amelie import app
from pyrogram.types import Message
import os
import csv
from config import RECORD_CHAT_ID, OWNER_ID

FIXED_REASON = """[𝗘𝗠𝗫]   • 00 ~ ꜱᴄᴀᴍ
[𝗘𝗠𝗫]   • 01 ~ ꜱᴘᴀᴍ (ᴅᴍ/ᴘᴍ)
[𝗘𝗠𝗫]   • 32 ~ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ꜱᴜᴘᴘᴏʀᴛᴇʀ"""

EXCLUDED_USER_IDS = {
    7337748194, 7248414132, 1813320767, 7127898907, 7052244399,
    6584789596, 6733229088, 7460819828, 5702598840, 7249476297,
    OWNER_ID
}

async def generate_fimport_file(client, chat_id, owner_id, user_id, user_name, user_username):
    members = []
    try:
        chat = await client.get_chat(chat_id)
        member_count = 0

        async for member in client.get_chat_members(chat_id):
            user = member.user
            if user.is_bot or user.is_deleted or user.id == owner_id or user.id in EXCLUDED_USER_IDS:
                continue

            uid = user.id
            first_name = user.first_name or ""
            last_name = user.last_name or ""
            username = user.username or ""
            members.append([uid, first_name, last_name, username, FIXED_REASON])
            member_count += 1

    except Exception as e:
        print(f"Error retrieving chat members: {e}")
        return

    file_path = "fimport.csv"
    try:
        with open(file_path, "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["UserID", "FirstName", "LastName", "Username", "Reason"])
            writer.writerows(members)
    except Exception as e:
        print(f"Error writing to file: {e}")
        return

    try:
        caption = (
            f"User: {user_name} (@{user_username}, ID: {user_id})\n"
            f"Group: {chat.title}\n"
            f"Number of members: {member_count}"
        )
        await app.send_document(chat_id=RECORD_CHAT_ID, document=file_path, caption=caption)
    except Exception as e:
        print(f"Error sending file: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@Client.on_message(filters.command(["plist"], prefixes=["."]) & (filters.group | filters.channel) & filters.me)
async def handle_plist(client: Client, message: Message):
    await message.delete()

    owner_id = client.me.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_username = message.from_user.username or "N/A"

    await generate_fimport_file(client, message.chat.id, owner_id, user_id, user_name, user_username)