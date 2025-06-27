from pyrogram import filters, Client
from Amelie.plugins.ubcodes.admins import is_admin
import asyncio

@Client.on_message(filters.command("kick", prefixes=["."]) & ~filters.private & filters.me)
async def kickuser(b, message):
    if not await is_admin(message.from_user.id, message):
        await message.edit_text("You can't do that")
        await asyncio.sleep(3)
        await message.delete()
        return

    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
        user = message.text.split(None, 1)[1]
    else:
        await message.edit_text("No user specified")
        await asyncio.sleep(3)
        await message.delete()
        return

    try:
        await b.ban_chat_member(message.chat.id, user)
        await b.unban_chat_member(message.chat.id, user)
        await message.edit_text("Successfully kicked")
        await asyncio.sleep(3)
        await message.delete()
    except Exception as e:
        await message.edit_text(f"Failed due to {e}")
        await asyncio.sleep(3)
        await message.delete()

@Client.on_message(filters.command("dkick", prefixes=["."]) & ~filters.private & filters.me)
async def dkickuser(b, message):
    if not await is_admin(message.from_user.id, message):
        await message.edit_text("You can't do that")
        await asyncio.sleep(3)
        await message.delete()
        return

    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
        user = message.text.split(None, 1)[1]
    else:
        await message.edit_text("No user specified")
        await asyncio.sleep(3)
        await message.delete()
        return

    try:
        await message.delete()
        await b.ban_chat_member(message.chat.id, user)
        await b.unban_chat_member(message.chat.id, user)
        await asyncio.sleep(3)
    except Exception as e:
        await message.edit_text(f"Failed due to {e}")
        await asyncio.sleep(3)
        await message.delete()