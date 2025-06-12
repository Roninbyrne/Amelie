import logging
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatPrivileges, Message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_userbot(client: Client):

    async def get_target_user_id(client, chat_id, message: Message):
        if message.reply_to_message:
            return message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            user = await client.get_users(message.command[1])
            return user.id
        return None

    @client.on_message(filters.command('demote', prefixes=".") & filters.group & filters.me)
    async def demote_user(client: Client, message: Message):
        chat_id = message.chat.id
        bot_user = await client.get_me()

        try:
            bot_member = await client.get_chat_member(chat_id, bot_user.id)
            if bot_member.status != ChatMemberStatus.ADMINISTRATOR:
                await message.edit_text("❌ I'm not an admin.")
                return
            if not bot_member.privileges.can_promote_members:
                await message.edit_text("❌ I can't demote users.")
                return
        except Exception as e:
            await message.edit_text(f"❌ Error checking my admin status: {e}")
            return

        target_user_id = await get_target_user_id(client, chat_id, message)
        if target_user_id is None:
            await message.edit_text("❌ Target user not found.")
            return

        try:
            target_user_member = await client.get_chat_member(chat_id, target_user_id)
        except Exception as e:
            await message.edit_text(f"❌ Can't fetch target user info: {e}")
            return

        if target_user_id == bot_user.id:
            await message.edit_text("❌ I won't demote myself.")
            return

        if target_user_member.status == ChatMemberStatus.OWNER:
            await message.edit_text("❌ I can't demote the group owner.")
            return

        if target_user_member.status != ChatMemberStatus.ADMINISTRATOR:
            await message.edit_text("ℹ️ This user is not an admin.")
            return

        if target_user_member.promoted_by and target_user_member.promoted_by.id != bot_user.id:
            await message.edit_text("❌ I didn't promote this user, so I can't demote them.")
            return

        if message.from_user.id == target_user_id:
            await message.edit_text("❌ You can't demote yourself.")
            return

        try:
            privileges = ChatPrivileges(
                can_change_info=False,
                can_invite_users=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False
            )

            await client.promote_chat_member(chat_id, target_user_id, privileges=privileges)

            target_name = target_user_member.user.first_name + (" " + target_user_member.user.last_name if target_user_member.user.last_name else "")
            admin_name = message.from_user.first_name + (" " + message.from_user.last_name if message.from_user.last_name else "")

            await message.edit_text(f"✅ {target_name} has been demoted by {admin_name}.")
        except Exception as e:
            await message.edit_text(f"❌ Failed to demote user: {e}")