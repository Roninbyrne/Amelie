import asyncio
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid
from pyrogram.enums import ChatMemberStatus

@Client.on_message(filters.command("zombies", prefixes=["."]) & ~filters.private & filters.me)
async def rm_deletedacc(client, message):
    del_u = 0
    chat_id = message.chat.id
    user_id = message.from_user.id

    async for admin in client.get_chat_members(chat_id, filter="administrators"):
        if admin.user.id == user_id:
            break
    else:
        return await message.edit("Sorry, you are not an admin!")

    response_message = await message.edit("Removing deleted accounts...")

    async for user in client.get_chat_members(chat_id):
        if user.user.is_deleted:
            try:
                await client.ban_chat_member(chat_id, user.user.id)
                await client.unban_chat_member(chat_id, user.user.id)
                del_u += 1
            except ChatAdminRequired:
                return await response_message.edit("Do not have permission to ban in this group.")
            except UserAdminInvalid:
                del_u -= 1

    del_status = f"Cleaned {del_u} Zombies" if del_u > 0 else "No deleted accounts found."
    await response_message.edit(del_status)
    await asyncio.sleep(5)
    await response_message.delete()
