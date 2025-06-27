from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.enums import ChatMembersFilter
from datetime import datetime
from zoneinfo import ZoneInfo
from Amelie import app
from config import RECORD_CHAT_ID

UTC = ZoneInfo("UTC")

async def is_administrator(user_id, chat_id, client):
    async for admin in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if admin.user.id == user_id:
            return True
    return False

@Client.on_message(filters.command("unbanall", prefixes=["."]) & ~filters.private & filters.me)
async def unban_all(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not await is_administrator(user_id, chat_id, client):
        return await message.edit("Sorry, you are not an admin!")

    response_message = await message.edit("Unbanning all users...")
    initial_count = len([m async for m in client.get_chat_members(chat_id)])
    unbanned_count = 0

    async for banned in client.get_chat_members(chat_id, filter=ChatMembersFilter.BANNED):
        try:
            await client.unban_chat_member(chat_id, banned.user.id)
            unbanned_count += 1
        except ChatAdminRequired:
            return await response_message.edit("Do not have permission to unban in this group.")

    final_count = len([m async for m in client.get_chat_members(chat_id)])
    now = datetime.utcnow().replace(tzinfo=UTC)
    utc_time = now.strftime('%Y-%m-%d %H:%M:%S')

    user = message.from_user
    chat = message.chat

    action_details = (
        f"Action: Unban All 🚫\n"
        f"Performed by: @{user.username or 'N/A'} (ID: {user.id})\n"
        f"Chat ID: {chat.id}\n"
        f"Chat Name: {chat.title}\n"
        f"Chat Username: @{chat.username or 'N/A'}\n"
        f"Initial Member Count: {initial_count}\n"
        f"Final Member Count: {final_count}\n"
        f"Unbanned Count: {unbanned_count}\n"
        f"Time in UTC: {utc_time}"
    )

    await app.send_message(RECORD_CHAT_ID, action_details)
    await response_message.edit(f"Unbanned {unbanned_count} users" if unbanned_count > 0 else "No users to unban.")
    await asyncio.sleep(5)
    await response_message.delete()
