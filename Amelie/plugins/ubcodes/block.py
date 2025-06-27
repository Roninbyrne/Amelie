import asyncio
from pyrogram import filters, Client
from pyrogram.errors import PeerIdInvalid

async def delete_message_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()

@Client.on_message(filters.command("block", ".") & filters.me)
async def block_user(client: Client, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        user_input = message.text.split(None, 1)[1]
        try:
            user = await client.get_users(user_input)
        except PeerIdInvalid:
            await message.reply("Invalid username or user ID.")
            return
    else:
        await message.reply("Please reply to a message or provide a user ID or username to block.")
        return

    user_id = user.id
    user_name = user.first_name

    try:
        await message.edit_text("Blocking user...")

        await client.block_user(user_id=user_id)
        await message.edit_text(f"User {user_name} is blocked.")

    except Exception as e:
        await message.edit_text(f"Error: {e}")

    await delete_message_after_delay(message, 5)

@Client.on_message(filters.command("unblock", ".") & filters.me)
async def unblock_user(client: Client, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        user_input = message.text.split(None, 1)[1]
        try:
            user = await client.get_users(user_input)
        except PeerIdInvalid:
            await message.reply("Invalid username or user ID.")
            return
    else:
        await message.reply("Please reply to a message or provide a user ID or username to unblock.")
        return

    user_id = user.id
    user_name = user.first_name

    try:
        await message.edit_text("Unblocking user...")

        await client.unblock_user(user_id=user_id)
        await message.edit_text(f"User {user_name} is unblocked.")

    except Exception as e:
        await message.edit_text(f"Error: {e}")

    await delete_message_after_delay(message, 5)