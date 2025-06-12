from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

def register_userbot(client: Client):
    @client.on_message(filters.command(["del"], prefixes=["."]) & (filters.group | filters.channel | filters.private) & filters.me)
    async def purge(_, ctx: Message):
        try:
            repliedmsg = ctx.reply_to_message
            await ctx.delete()

            if not repliedmsg:
                error_msg = await ctx.reply_text("Reply to the message you want to delete.")
                await asyncio.sleep(2)
                await error_msg.delete()
                return

            chat_id = ctx.chat.id

            await _.delete_messages(
                chat_id=chat_id,
                message_ids=[repliedmsg.id],
                revoke=True
            )

            completion_msg = await ctx.reply_text("Message deleted.")
            await asyncio.sleep(2)
            await completion_msg.delete()

        except Exception as err:
            error_msg = await ctx.reply_text(f"ERROR: {err}")
            await asyncio.sleep(5)
            await error_msg.delete()