import asyncio
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus
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

async def is_owner(user_id, chat_id, client):
    async for admin in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if admin.status == ChatMemberStatus.CREATOR:
            return admin.user.id == user_id
    return False

@Client.on_message(filters.command("kickall", prefixes=["."]) & ~filters.private & filters.me)
async def kick_all(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not await is_administrator(user_id, chat_id, client) or await is_owner(user_id, chat_id, client):
        return await message.edit("Sorry, you are not allowed to use this command!")

    response_message = await message.edit("Kicking all members...")
    initial_count = len([m async for m in client.get_chat_members(chat_id)])
    kicked_count = 0

    async for member in client.get_chat_members(chat_id):
        if not await is_administrator(member.user.id, chat_id, client) and not await is_owner(member.user.id, chat_id, client):
            try:
                await client.ban_chat_member(chat_id, member.user.id)
                await client.unban_chat_member(chat_id, member.user.id)
                kicked_count += 1
            except ChatAdminRequired:
                return await response_message.edit("Do not have permission to kick in this group.")

    final_count = len([m async for m in client.get_chat_members(chat_id)])
    now = datetime.utcnow().replace(tzinfo=UTC)
    utc_time = now.strftime('%Y-%m-%d %H:%M:%S')

    user = message.from_user
    chat = message.chat

    action_details = (
        f"Action: Kick All 🚫\n"
        f"Performed by: @{user.username or 'N/A'} (ID: {user.id})\n"
        f"Chat ID: {chat.id}\n"
        f"Chat Name: {chat.title}\n"
        f"Chat Username: @{chat.username or 'N/A'}\n"
        f"Initial Member Count: {initial_count}\n"
        f"Final Member Count: {final_count}\n"
        f"Kicked Count: {kicked_count}\n"
        f"Time in UTC: {utc_time}"
    )

    await app.send_message(RECORD_CHAT_ID, action_details)
    await response_message.edit(f"Kicked {kicked_count} members" if kicked_count > 0 else "No members to kick.")
    await asyncio.sleep(5)
    await response_message.delete()
