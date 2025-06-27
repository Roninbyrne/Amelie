import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType

@Client.on_message(filters.command("ucast", prefixes=".") & filters.me)
async def ucast_handler(client: Client, message: Message):
    send_text = None

    if message.reply_to_message:
        send_text = message.reply_to_message.text or message.reply_to_message.caption
        reply = message.reply_to_message
    else:
        parts = message.text.split(None, 1)
        if len(parts) == 2:
            send_text = parts[1]
            reply = None
        else:
            await message.edit_text("❌ Provide a message or reply to one.")
            await asyncio.sleep(3)
            await message.delete()
            return

    sent_count = 0
    fail_count = 0
    await message.edit_text("🔄 Ucasting with delay...")

    async for dialog in client.get_dialogs():
        chat = dialog.chat
        if chat.type == ChatType.PRIVATE:
            try:
                user = await client.get_users(chat.id)
                if user.is_bot:
                    continue

                if reply and reply.media:
                    await reply.copy(chat.id)
                else:
                    await client.send_message(chat.id, send_text)

                sent_count += 1
                await asyncio.sleep(1.2)
            except Exception:
                fail_count += 1
                await asyncio.sleep(0.5)

    await message.edit_text(
        f"✅ Ucast completed!\n\n"
        f"🟢 Success: `{sent_count}`\n"
        f"🔴 Failed: `{fail_count}`"
    )

    await asyncio.sleep(5)
    await message.delete()
