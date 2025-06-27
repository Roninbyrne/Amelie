from pyrogram import filters, Client
from pyrogram.types import ChatPrivileges, ChatPermissions, Message
from pyrogram.types import *
from pyrogram.enums import ChatMembersFilter, ChatType
from datetime import datetime, timedelta, timezone
import asyncio
import logging

async def is_administrator(user_id: int, message,client):
    admin = False
    administrators = []
    async for m in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m)
    for user in administrators:
        if user.user.id == user_id:
            admin = True
            break
    return admin
async def is_admin(user_id: int, message):
    
    administrators = []
    async for m in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m)
    if user_id in administrators:
        return True     
    else:
        return False
 
 
    
@Client.on_message(filters.command(["ban"], prefixes=["."]) & (filters.group | filters.channel) & filters.me)
async def banuser(b, message):
    try:
        if not is_admin(message.from_user.id, message):
            msg = await message.edit_text("You can't do that")
            await asyncio.sleep(5)
            await msg.delete()
            return

        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            user_mention = message.reply_to_message.from_user.mention
        elif len(message.command) > 1:
            user_id = message.text.split(None, 1)[1]
            user_mention = user_id
        else:
            msg = await message.edit_text("Please specify a user to ban.")
            await asyncio.sleep(5)
            await msg.delete()
            return

        await b.ban_chat_member(message.chat.id, user_id)
        msg = await message.edit_text(f"{message.from_user.mention} Banned {user_mention}.")
        await asyncio.sleep(5)
        await msg.delete()

    except Exception as e:
        msg = await message.edit_text(f"Failed to ban {user_mention} due to {e}.")
        await asyncio.sleep(5)
        await msg.delete()

@Client.on_message(filters.command(["mute"], prefixes=["."]) & (filters.group | filters.channel) & filters.me)
async def mute(client, message: Message):
    chat = message.chat

    if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        msg = await message.edit_text("This command only works in groups.")
        await asyncio.sleep(5)
        await msg.delete()
        return

    if len(message.command) == 2:
        user_to_mute = message.command[1]
        if user_to_mute.isdigit():
            user_id = int(user_to_mute)
            user = await client.get_users(user_id)
        else:
            user = await client.get_users(user_to_mute)

    elif message.reply_to_message:
        user = message.reply_to_message.from_user
        if not user:
            msg = await message.edit_text("Could not find the user in the reply.")
            await asyncio.sleep(5)
            await msg.delete()
            return

    else:
        msg = await message.edit_text("Usage: .mute <username or user_id> or reply to a message.")
        await asyncio.sleep(5)
        await msg.delete()
        return

    permissions = ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False
    )

    try:
        await client.restrict_chat_member(chat.id, user.id, permissions=permissions)
        msg = await message.edit_text(f"{user.username or user.id} has been muted.")
        await asyncio.sleep(5)
        await msg.delete()

    except Exception as e:
        msg = await message.edit_text(f"Failed to mute {user.username or user.id}. Error: {e}")
        await asyncio.sleep(5)
        await msg.delete()

muted_users = {}

@Client.on_message(filters.command(["tmute"], prefixes=["."]) & (filters.group | filters.channel) & filters.me)
async def tmute(client, message: Message):
    chat = message.chat

    if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.edit_text("This command only works in groups.")
        await asyncio.sleep(5)
        await message.delete()
        return

    if len(message.command) < 3:
        await message.edit_text("Usage: .tmute <username or user_id> <duration>\nDuration format: <number><unit>, e.g., 5m, 1h, 2d.")
        await asyncio.sleep(5)
        await message.delete()
        return

    user_to_mute = message.command[1]
    duration_str = message.command[2]

    duration_mapping = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    unit = duration_str[-1].lower()
    if unit in duration_mapping:
        try:
            duration = int(duration_str[:-1]) * duration_mapping[unit]
        except ValueError:
            await message.edit_text("Invalid duration format. Please specify a number followed by a unit (s, m, h, d).")
            await asyncio.sleep(5)
            await message.delete()
            return
    else:
        await message.edit_text("Invalid unit. Use 's' for seconds, 'm' for minutes, 'h' for hours, 'd' for days.")
        await asyncio.sleep(5)
        await message.delete()
        return

    if user_to_mute.isdigit():
        user_id = int(user_to_mute)
        user = await client.get_users(user_id)
    else:
        user = await client.get_users(user_to_mute)

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if not user:
            await message.edit_text("Could not find the user in the reply.")
            await asyncio.sleep(5)
            await message.delete()
            return

    try:
        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False
        )

        now_utc = datetime.now(timezone.utc)
        expiration_time_utc = now_utc + timedelta(seconds=duration)

        await client.restrict_chat_member(
            chat.id,
            user.id,
            permissions=permissions,
            until_date=expiration_time_utc
        )

        muted_users[user.id] = (chat.id, expiration_time_utc)

        await message.edit_text(f"{user.username or user.id} has been muted for {duration_str}.")

        asyncio.create_task(unmute_after_duration(client, chat.id, user.id, expiration_time_utc))

    except Exception as e:
        await message.edit_text(f"Failed to mute {user.username or user.id}. Error: {e}")

    await asyncio.sleep(5)
    await message.delete()

async def unmute_after_duration(client, chat_id, user_id, expiration_time_utc):
    now_utc = datetime.now(timezone.utc)
    delay = (expiration_time_utc - now_utc).total_seconds()
    if delay > 0:
        await asyncio.sleep(delay)
        try:
            permissions = ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
            await client.restrict_chat_member(
                chat_id,
                user_id,
                permissions=permissions
            )
            if user_id in muted_users:
                del muted_users[user_id]
        except Exception as e:
            print(f"Failed to unmute user {user_id}. Error: {e}")

@Client.on_message(filters.command(["unmute"], prefixes=["."]) & (filters.group | filters.channel) & filters.me)
async def unmute(client, message: Message):
    chat = message.chat

    if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.edit_text("This command only works in groups.")
        await asyncio.sleep(5)
        await message.delete()
        return

    if len(message.command) == 2:
        user_to_unmute = message.command[1]
        if user_to_unmute.isdigit():
            user_id = int(user_to_unmute)
            user = await client.get_users(user_id)
        else:
            user = await client.get_users(user_to_unmute)

    elif message.reply_to_message:
        user = message.reply_to_message.from_user
        if not user:
            await message.edit_text("Could not find the user in the reply.")
            await asyncio.sleep(5)
            await message.delete()
            return

    else:
        await message.edit_text("Usage: .unmute <username or user_id> or reply to a message.")
        await asyncio.sleep(5)
        await message.delete()
        return

    try:
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )

        await client.restrict_chat_member(
            chat.id,
            user.id,
            permissions=permissions
        )
        await message.edit_text(f"{user.username or user.id} has been unmuted.")

    except Exception as e:
        await message.edit_text(f"Failed to unmute {user.username or user.id}. Error: {e}")

    await asyncio.sleep(5)
    await message.delete()

last_message = {}

@Client.on_message(filters.command(["staffs", "admins"], prefixes=["."]) & (filters.group | filters.channel) & filters.me)
async def get_staff(client, message):
    chat_id = message.chat.id

    try:
        await message.edit_text("Fetching admin list...")

        administrators = []
        async for m in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
            administrators.append(m)

        staff = "Admins:\n"
        for user in administrators:
            staff += f"{user.user.mention}\n"

        await message.edit_text(staff)

        await asyncio.sleep(10)
        await message.delete()

    except Exception as e:
        print(f"Failed to get or update admin list: {e}")
        try:
            await message.edit_text("Failed to get admin list.")
        except Exception as edit_error:
            print(f"Failed to edit message text: {edit_error}")

    last_message[chat_id] = message.message_id
        
@Client.on_message(filters.command("unban", prefixes=["."]) & (filters.group | filters.channel) & filters.me)
async def unbanuser(b, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        user_id = user.id
        user_mention = f"@{user.username}" if user.username else f"{user.first_name}"
    elif len(message.command) > 1:
        user_input = message.text.split(None, 1)[1]
        try:
            user = await b.get_users(user_input)
            user_id = user.id
            user_mention = f"@{user.username}" if user.username else f"{user.first_name}"
        except Exception as e:
            await message.edit_text(f"User not found. Error: {e}")
            await asyncio.sleep(5)
            await message.delete()
            return
    else:
        await message.edit_text("Please specify a user to unban")
        await asyncio.sleep(5)
        await message.delete()
        return

    try:
        await message.edit_text(f"Processing to unban user: {user_mention}")

        await b.unban_chat_member(message.chat.id, user_id)

        await message.edit_text(f"Successfully Unbanned {user_mention}")
    except Exception as e:
        await message.edit_text(f"Failed to unban user. Error: {e}")

    await asyncio.sleep(5)
    await message.delete()

@Client.on_message(filters.command("leave", prefixes=["."]) & (filters.group | filters.channel) & filters.me)
async def leaveuser(b, message):
    chat = message.chat.id
    if len(message.command) > 1:
        chat = message.text.split(None, 1)[1]

    try:
        await message.edit_text(f"Processing to leave chat: {chat}...")

        await b.leave_chat(chat, delete=True)
        
        await message.edit_text(f"Left chat: {chat} 🤧")
    except Exception as e:
        await message.edit_text(f"Failed to leave chat. Error: {e}")

async def is_admin(user_id, message):
    return True


@Client.on_message(filters.command("settitle", prefixes=["."]) & (filters.group | filters.channel) & filters.me)
async def set_chat_title(b, message):
    if not is_admin(message.from_user.id, message):
        await message.edit_text("You can't do that")
        return

    if message.reply_to_message:
        msg = message.reply_to_message.text
    elif not message.reply_to_message and len(message.command) != 1:
        msg = message.text.split(None, 1)[1]

    chat = message.chat.id
    try:
        await b.set_chat_title(chat, msg)
        await message.edit_text(f"Title set to '{msg}'")
    except Exception as e:
        await message.edit_text(f"Failed due to {e}")


@Client.on_message(filters.command("setdesc", prefixes=["."] ) & (filters.group | filters.channel) & filters.me)
async def set_chat_description(b, message):
    if not is_admin(message.from_user.id, message):
        return await message.edit_text("You can't do that")

    if message.reply_to_message:
        msg = message.reply_to_message.text
    elif len(message.command) != 1:
        msg = message.text.split(None, 1)[1]
    else:
        return await message.edit_text("No description provided")

    chat = message.chat.id
    try:
        await b.set_chat_description(chat, msg)
        await message.edit_text("Description updated successfully")
    except Exception as e:
        await message.edit_text(f"Failed due to: {e}")


@Client.on_message(filters.command("stats", prefixes=["."]) & filters.me)
async def stats(client, message):
    await message.edit_text("Please wait...\n\nFetching chat statistics...")

    groups_and_supergroups = []
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        print(f"Chat ID: {dialog.chat.id}, Name: {dialog.chat.title if dialog.chat.title else 'No Title'}, Type: {chat_type}")

        if chat_type in (ChatType.GROUP, ChatType.SUPERGROUP):
            groups_and_supergroups.append(dialog.chat.id)

    await message.edit_text(f"ʜᴇʀᴇ ᴀʀᴇ ʏᴏᴜʀ ᴄʜᴀᴛ ꜱᴛᴀᴛꜜ:\n\n{len(groups_and_supergroups)} groups and supergroups")

    await asyncio.sleep(5)
    await message.delete()
    

    
@Client.on_message(filters.command(["purge"], prefixes=["."]) & (filters.group | filters.channel | filters.private) & filters.me)
async def purge(_, ctx: Message):
    try:
        repliedmsg = ctx.reply_to_message
        await ctx.delete()

        if not repliedmsg:
            error_msg = await ctx.reply_text("Reply to the message you want to delete.")
            await asyncio.sleep(2)
            await error_msg.delete()
            return

        cmd = ctx.command
        if len(cmd) > 1 and cmd[1].isdigit():
            purge_to = repliedmsg.id + int(cmd[1])
            purge_to = min(purge_to, ctx.id)
        else:
            purge_to = ctx.id

        chat_id = ctx.chat.id
        message_ids = []
        del_total = 0

        for message_id in range(
            repliedmsg.id,
            purge_to,
        ):
            message_ids.append(message_id)

            if len(message_ids) == 100:
                await _.delete_messages(
                    chat_id=chat_id,
                    message_ids=message_ids,
                    revoke=True,
                )
                del_total += len(message_ids)
                message_ids = []

        if len(message_ids) > 0:
            await _.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,
            )
            del_total += len(message_ids)
        
        completion_msg = await ctx.reply_text("ᴘᴜʀɢᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ")
        await asyncio.sleep(2)
        await completion_msg.delete()
        
    except Exception as err:
        error_msg = await ctx.reply_text(f"ERROR: {err}")
        await asyncio.sleep(5)
        await error_msg.delete()
        
        
        
@Client.on_message(filters.command(["promote", "fullpromote"], ".") & ~filters.private & filters.me)
async def promoteFunc(client, message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            user = message.text.split(None, 1)[1]
        else:
            await message.edit_text("Invalid command usage.")
            await asyncio.sleep(5)
            await message.delete()
            return

        umention = (await client.get_users(user)).mention
    except Exception:
        await message.edit_text("Invalid ID or user not found.")
        await asyncio.sleep(5)
        await message.delete()
        return

    if not user:
        await message.edit_text("User not found.")
        await asyncio.sleep(5)
        await message.delete()
        return

    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if user == client.me.id:
        await message.edit_text("You cannot promote yourself.")
        await asyncio.sleep(5)
        await message.delete()
        return

    if not bot or not bot.can_promote_members:
        await message.edit_text("I don't have the permission to promote members.")
        await asyncio.sleep(5)
        await message.delete()
        return

    try:
        if message.command[0] == "fullpromote":
            await message.chat.promote_member(
                user_id=user,
                privileges=ChatPrivileges(
                    can_change_info=bot.can_change_info,
                    can_invite_users=bot.can_invite_users,
                    can_delete_messages=bot.can_delete_messages,
                    can_restrict_members=bot.can_restrict_members,
                    can_pin_messages=bot.can_pin_messages,
                    can_promote_members=bot.can_promote_members,
                    can_manage_chat=bot.can_manage_chat,
                    can_manage_video_chats=bot.can_manage_video_chats,
                ),
            )
            final_msg = await message.edit_text("User has been fully promoted.")

        else:
            await message.chat.promote_member(
                user_id=user,
                privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=bot.can_invite_users,
                    can_delete_messages=bot.can_delete_messages,
                    can_restrict_members=False,
                    can_pin_messages=bot.can_pin_messages,
                    can_promote_members=False,
                    can_manage_chat=bot.can_manage_chat,
                    can_manage_video_chats=bot.can_manage_video_chats,
                ),
            )
            final_msg = await message.edit_text("User has been promoted.")

    except Exception as err:
        await message.edit_text(f"An error occurred: {err}")
        await asyncio.sleep(5)
        await message.delete()
    else:
        await asyncio.sleep(5)
        await final_msg.delete()
        
        
        
@Client.on_message(filters.command(["demote"], ".") & ~filters.private & filters.me)
async def demoteFunc(client, message: Message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif not message.reply_to_message and len(message.command) != 1:
            user = message.text.split(None, 1)[1]

        umention = (await client.get_users(user)).mention
    except:
        error_msg = await message.edit("Invalid ID")
        await asyncio.sleep(5)
        return await error_msg.delete()

    try:
        await message.chat.promote_member(user_id=user,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
            ))
        success_msg = await message.edit("Successfully Demoted")
        await asyncio.sleep(5)
        await success_msg.delete()

    except Exception as err:
        error_msg = await message.edit(f"Error: {err}")
        await asyncio.sleep(5)
        await error_msg.delete()

last_message = {}

@Client.on_message(filters.command(["botlist"], prefixes=["."]) & (filters.group | filters.channel) & filters.me)
async def get_bot_list(client, message):
    chat_id = message.chat.id

    try:
        await message.edit_text("Fetching bot list...")

        me = await client.get_me()
        bot_id = me.id
        is_bot_admin = False
        async for member in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
            if member.user.id == bot_id:
                is_bot_admin = True
                break

        admin_bots = []
        non_admin_bots = []
        async for member in client.get_chat_members(chat_id, filter=ChatMembersFilter.BOTS):
            bot_id = member.user.id
            is_admin = False
            async for admin in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
                if admin.user.id == bot_id:
                    is_admin = True
                    break
            if is_admin:
                admin_bots.append(member.user.mention)
            else:
                non_admin_bots.append(member.user.mention)

        bot_list = "Bots in this chat:\n\n"

        if admin_bots:
            bot_list += "Admin Bots:\n" + "\n".join(admin_bots) + "\n\n"

        if non_admin_bots:
            bot_list += "Non-Admin Bots:\n" + "\n".join(non_admin_bots)
        else:
            bot_list += "No non-admin bots found."

        await message.edit_text(bot_list)

        await asyncio.sleep(10)
        await message.delete()

    except Exception as e:
        print(f"Failed to get or update bot list: {e}")
        try:
            await message.edit_text("Failed to get bot list.")
        except Exception as edit_error:
            print(f"Failed to edit message text: {edit_error}")

    last_message[chat_id] = message.id
