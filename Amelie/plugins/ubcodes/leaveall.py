
import asyncio
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message

@Client.on_message(filters.command(["leaveall", "assleaveall"], ".") & filters.me)
async def leaveall_chats(client, message: Message):
    lear = await message.edit_text("» sᴛᴀʀᴛᴇᴅ ʟᴇᴀᴠɪɴɢ ᴄʜᴀᴛs...")
    
    left = 0
    failed = 0
    chats = []
    
    async for dialog in client.get_dialogs():
        chats.append(int(dialog.chat.id))
    
    for i in chats:
        try:
            await client.leave_chat(int(i))
            left += 1
        except FloodWait as e:
            flood_time = int(e.value)
            if flood_time > 200:
                continue
            await asyncio.sleep(flood_time)
        except Exception:
            failed += 1
            continue

    try:
        await lear.edit_text(
            f"<u>**»  sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ ᴄʜᴀᴛs :**</u>\n\n**ʟᴇғᴛ :** `{left}`\n**ғᴀɪʟᴇᴅ :** `{failed}`"
        )
    except:
        await message.reply_text(
            f"<u>**»  sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ ᴄʜᴀᴛs :**</u>\n\n**ʟᴇғᴛ :** `{left}`\n**ғᴀɪʟᴇᴅ :** `{failed}`"
        )