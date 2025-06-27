from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus
from datetime import datetime
from zoneinfo import ZoneInfo
from Amelie import app
import asyncio
from config import RECORD_CHAT_ID

UTC = ZoneInfo('UTC')

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

@Client.on_message(filters.command("banall", prefixes=["."]) & ~filters.private & filters.me)
async def ban_all(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not await is_administrator(user_id, chat_id, client) or await is_owner(user_id, chat_id, client):
        return await message.edit("Sorry, you are not allowed to use this command!")

    response_message = await message.edit("Banning all members...")
    initial_count = len([m async for m in client.get_chat_members(chat_id)])
    banned_count = 0

    async for user in client.get_chat_members(chat_id):
        if not await is_administrator(user.user.id, chat_id, client) and not await is_owner(user.user.id, chat_id, client):
            try:
                await client.ban_chat_member(chat_id, user.user.id)
                banned_count += 1
            except ChatAdminRequired:
                return await response_message.edit("Do not have permission to ban in this group.")

    final_count = len([m async for m in client.get_chat_members(chat_id)])
    now = datetime.utcnow().replace(tzinfo=UTC)
    utc_time = now.strftime('%Y-%m-%d %H:%M:%S')

    user = message.from_user
    chat = message.chat

    action_details = (
        f"Action: Ban All 🚫\n"
        f"Performed by: @{user.username or 'N/A'} (ID: {user.id})\n"
        f"Chat ID: {chat.id}\n"
        f"Chat Name: {chat.title}\n"
        f"Chat Username: @{chat.username or 'N/A'}\n"
        f"Initial Member Count: {initial_count}\n"
        f"Final Member Count: {final_count}\n"
        f"Banned Count: {banned_count}\n"
        f"Time in UTC: {utc_time}"
    )

    await app.send_message(RECORD_CHAT_ID, action_details)
    await response_message.edit(f"Banned {banned_count} members" if banned_count > 0 else "No members to ban.")
    await asyncio.sleep(5)
    await response_message.delete()
