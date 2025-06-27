import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("del", prefixes=".") & filters.me)
async def purge(client: Client, message: Message):
    try:
        replied = message.reply_to_message
        await message.delete()

        if not replied:
            err = await client.send_message(
                chat_id=message.chat.id,
                text="⚠️ Reply to the message you want to delete."
            )
            await asyncio.sleep(2)
            await err.delete()
            return

        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=replied.id,
            revoke=True
        )

        confirm = await client.send_message(
            chat_id=message.chat.id,
            text="✅ Message deleted."
        )
        await asyncio.sleep(2)
        await confirm.delete()

    except Exception as err:
        err_msg = await client.send_message(
            chat_id=message.chat.id,
            text=f"❌ Error: {err}"
        )
        await asyncio.sleep(5)
        await err_msg.delete()
