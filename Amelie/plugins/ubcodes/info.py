from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode, ChatMemberStatus
import logging

@Client.on_message(filters.command("info", prefixes=".") & filters.me)
async def userinfo_handler(client: Client, message: Message):
    chat = message.chat
    reply = message.reply_to_message
    user_id = None

    if len(message.command) == 2:
        user_input = message.text.split(None, 1)[1].strip()
        try:
            user = await client.get_users(user_input)
            user_id = user.id
        except Exception:
            await message.edit_text("❌ This user doesn't exist.")
            return
    elif reply and reply.from_user:
        user_id = reply.from_user.id
    else:
        await message.edit_text("❌ Provide a username/user ID or reply to a user.")
        return

    try:
        user = await client.get_users(user_id)

        text = (
            f"**👤 User Info:**\n"
            f"**ID:** `{user.id}`\n"
            f"**Name:** {user.first_name or 'No name'}\n"
            f"**Username:** @{user.username if user.username else 'No username'}\n"
            f"**User Link:** [Click Here](tg://user?id={user.id})\n"
            f"**DC ID:** `{getattr(user, 'dc_id', 'N/A')}`\n"
            f"**Premium:** {'Yes' if user.is_premium else 'No'}\n"
        )

        if chat.type.name != "PRIVATE":
            try:
                member = await client.get_chat_member(chat.id, user_id)
                status_map = {
                    ChatMemberStatus.ADMINISTRATOR: "Admin",
                    ChatMemberStatus.OWNER: "Owner",
                    ChatMemberStatus.MEMBER: "Member",
                    ChatMemberStatus.RESTRICTED: "Restricted",
                    ChatMemberStatus.BANNED: "Banned"
                }
                user_status = status_map.get(member.status, "Left/Unknown")
                text = text.replace("DC ID:", f"**Status:** {user_status}\n**DC ID:**")
            except Exception as e:
                logging.error(f"Failed to get member status: {e}")
                text = text.replace("DC ID:", "**Status:** Unknown\n**DC ID:**")

        await message.edit_text(
            text,
            disable_web_page_preview=True,
            parse_mode=ParseMode.MARKDOWN
        )

    except Exception as e:
        await message.edit_text(f"❌ Error: {e}")
