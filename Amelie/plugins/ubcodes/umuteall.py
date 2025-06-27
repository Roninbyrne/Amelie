import asyncio
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus
from pyrogram.types import ChatPermissions

@Client.on_message(filters.command("unmuteall", prefixes=["."]) & ~filters.private & filters.me)
async def unmute_all(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    async for admin in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if admin.user.id == user_id:
            break
    else:
        return await message.edit("Sorry, you are not an admin!")

    response_message = await message.edit("Unmuting all members...")
    unmuted = 0

    async for member in client.get_chat_members(chat_id):
        if member.status == ChatMemberStatus.RESTRICTED:
            try:
                await client.restrict_chat_member(
                    chat_id,
                    member.user.id,
                    permissions=ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True,
                        can_send_polls=True,
                        can_add_web_page_previews=True,
                    ),
                )
                unmuted += 1
            except ChatAdminRequired:
                return await response_message.edit("Do not have permission to unmute in this group.")

    await response_message.edit(f"Unmuted {unmuted} members" if unmuted else "No members to unmute.")
    await asyncio.sleep(5)
    await response_message.delete()
