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

    @client.on_message(filters.command('demote', prefixes=".") & filters.group & filters.me)
    async def demote_user(client: Client, message: Message):
        chat_id = message.chat.id
        bot_user = await client.get_me()
        logger.info(f"Bot ID: {bot_user.id}, Chat ID: {chat_id}")

        try:
            bot_member = await client.get_chat_member(chat_id, bot_user.id)
            logger.info(f"Bot Member Privileges: {bot_member.privileges}")

            if bot_member.status != ChatMemberStatus.ADMINISTRATOR:
                await message.reply_text("I am not an admin.")
                return
            if not bot_member.privileges.can_promote_members:
                await message.reply_text("I don't have rights to demote users.")
                return
        except Exception as e:
            await message.reply_text(f"Error retrieving bot status: {e}")
            logger.error(f"Error retrieving bot status: {e}")
            return

        target_user_id = await get_target_user_id(client, chat_id, message)
        if target_user_id is None:
            await message.reply_text("Could not find the target user.")
            return

        target_user_member = await client.get_chat_member(chat_id, target_user_id)
        logger.info(f"Target User ID: {target_user_id}, Status: {target_user_member.status}, Privileges: {target_user_member.privileges}")

        if target_user_id == bot_user.id:
            await message.reply_text("Isn't it rude to demote me, huh?")
            return

        if target_user_member.status == ChatMemberStatus.OWNER:
            await message.reply_text("mmm..nope I can't demote group owner.")
            return

        if target_user_member.status != ChatMemberStatus.ADMINISTRATOR:
            await message.reply_text("This user is already not an admin.")
            return

        if target_user_member.promoted_by and target_user_member.promoted_by.id != bot_user.id:
            await message.reply_text("I can't demote cuz I'm not the one who promoted him.")
            return

        if message.from_user.id == target_user_id:
            await message.reply_text("You can't demote yourself.")
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

            target_user_full_name = target_user_member.user.first_name + " " + (target_user_member.user.last_name if target_user_member.user.last_name else "")
            admin_or_owner_full_name = message.from_user.first_name + " " + (message.from_user.last_name if message.from_user.last_name else "")

            await message.reply_text(f"{target_user_full_name} has been demoted by {admin_or_owner_full_name}.")
        except Exception as e:
            await message.reply_text(f"Failed to demote user: {str(e)}")
            logger.error(f"Failed to demote user: {str(e)}")