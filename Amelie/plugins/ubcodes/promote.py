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
            target_username = message.command[1]
            user = await client.get_users(target_username)
            return user.id
        else:
            return None

    async def promote_user_common(client: Client, message: Message, full: bool = False):
        chat_id = message.chat.id
        bot_user = await client.get_me()
        logger.info(f"Bot ID: {bot_user.id}, Chat ID: {chat_id}")

        try:
            bot_member = await client.get_chat_member(chat_id, bot_user.id)

            if bot_member.status != ChatMemberStatus.ADMINISTRATOR:
                await message.edit_text("❌ I'm not an admin in this group.")
                return
            if not bot_member.privileges.can_promote_members:
                await message.edit_text("❌ I don't have rights to promote users.")
                return
        except Exception as e:
            await message.edit_text(f"⚠️ Error retrieving my status: {e}")
            logger.error(f"Error retrieving bot status: {e}")
            return

        target_user_id = await get_target_user_id(client, chat_id, message)
        if target_user_id is None:
            await message.edit_text("❌ Could not find the target user.")
            return

        if target_user_id == bot_user.id:
            await message.edit_text("😐 Promoting myself? I'm flattered.")
            return

        if message.from_user.id == target_user_id:
            await message.edit_text("❌ You can't promote yourself.")
            return

        try:
            if full:
                privileges = ChatPrivileges(
                    can_change_info=True,
                    can_invite_users=True,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                    can_manage_chat=True,
                    can_manage_video_chats=True
                )
            else:
                privileges = ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=True,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_pin_messages=True,
                    can_promote_members=False,
                    can_manage_chat=False,
                    can_manage_video_chats=False
                )

            await client.promote_chat_member(chat_id, target_user_id, privileges=privileges)

            target_user = await client.get_users(target_user_id)
            promoter = message.from_user

            await message.edit_text(
                f"✅ {target_user.first_name} has been {'fully ' if full else ''}promoted by {promoter.first_name}."
            )

        except Exception as e:
            await message.edit_text(f"❌ Failed to promote user: {str(e)}")
            logger.error(f"Failed to promote user: {str(e)}")

    @client.on_message(filters.command('promote', prefixes=".") & filters.group & filters.me)
    async def partial_promote(client: Client, message: Message):
        await promote_user_common(client, message, full=False)

    @client.on_message(filters.command('fullpromote', prefixes=".") & filters.group & filters.me)
    async def full_promote(client: Client, message: Message):
        await promote_user_common(client, message, full=True)