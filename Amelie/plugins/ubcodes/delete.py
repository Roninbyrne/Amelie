from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

def register_userbot(client: Client):
    @client.on_message(
        filters.command(["del"], prefixes=["."]) & filters.me
    )
    async def purge(c: Client, m: Message):
        try:
            repliedmsg = m.reply_to_message
            await m.delete()

            if not repliedmsg:
                error_msg = await c.send_message(
                    chat_id=m.chat.id,
                    text="Reply to the message you want to delete."
                )
                await asyncio.sleep(2)
                await error_msg.delete()
                return

            await c.delete_messages(
                chat_id=m.chat.id,
                message_ids=repliedmsg.id,
                revoke=True
            )

            confirmation = await c.send_message(
                chat_id=m.chat.id,
                text="Message deleted."
            )
            await asyncio.sleep(2)
            await confirmation.delete()

        except Exception as err:
            error_msg = await c.send_message(
                chat_id=m.chat.id,
                text=f"ERROR: {err}"
            )
            await asyncio.sleep(5)
            await error_msg.delete()