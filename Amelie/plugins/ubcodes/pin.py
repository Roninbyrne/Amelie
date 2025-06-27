import asyncio
from pyrogram import filters, Client
from Amelie.plugins.ubcodes.admins import is_admin

@Client.on_message(filters.command("pin", ".") & ~filters.private & filters.me)
async def pin_msg(client, message):
    if not is_admin(message.from_user.id, message):
        response = await message.edit_text("You can't do that")
        await asyncio.sleep(5)
        await response.delete()
        return
    
    if message.reply_to_message:
        msg = message.reply_to_message
        try:
            await client.pin_chat_message(message.chat.id, msg.id)
            response = await message.edit_text("Pinned the message")
        except Exception as e:
            response = await message.edit_text(f"Error: {e}")
        
        await asyncio.sleep(5)
        await response.delete()

@Client.on_message(filters.command("unpin", ".") & ~filters.private & filters.me)
async def unpin_msg(client, message):
    if not is_admin(message.from_user.id, message):
        response = await message.edit_text("You can't do that")
        await asyncio.sleep(5)
        await response.delete()
        return
    
    if message.reply_to_message:
        msg = message.reply_to_message
        try:
            await client.unpin_chat_message(message.chat.id, msg.id)
            response = await message.edit_text("Unpinned the message")
        except Exception as e:
            response = await message.edit_text(f"Error: {e}")
        
        await asyncio.sleep(5)
        await response.delete()

@Client.on_message(filters.command("unpinall", ".") & filters.me)
async def unpin_all_chat_msg(client, message):
    if not is_admin(message.from_user.id, message):
        response = await message.edit_text("You can't do that")
        await asyncio.sleep(5)
        await response.delete()
        return

    try:
        await client.unpin_all_chat_messages(message.chat.id)
        response = await message.edit_text("Unpinned all messages")
    except Exception as e:
        response = await message.edit_text(f"Error: {e}")
    
    await asyncio.sleep(5)
    await response.delete()