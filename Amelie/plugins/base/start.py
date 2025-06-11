from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from Amelie import app
from Amelie.core.mongo import global_userinfo_db, video_channels_collection
from Amelie.plugins.base.logging_toggle import is_logging_enabled

from config import (
    SUPPORT_CHAT,
    SUPPORT_CHANNEL,
    START_VIDEO,
    HELP_MENU_VIDEO,
    HELP_VIDEO_1,
    HELP_VIDEO_2,
    HELP_VIDEO_3,
    HELP_VIDEO_4,
    LOGGER_ID
)

@app.on_message(filters.command("start") & filters.private)
async def start_pm(client, message: Message):
    user = message.from_user
    args = message.text.split(maxsplit=1)

    userinfo = {  
        "_id": user.id,  
        "first_name": user.first_name,  
        "last_name": user.last_name,  
        "username": user.username,  
        "is_bot": user.is_bot  
    }  
    await global_userinfo_db.update_one({"_id": user.id}, {"$set": userinfo}, upsert=True)  

    if await is_logging_enabled():  
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()  
        username = f"@{user.username}" if user.username else "N/A"  
        log_text = (  
            f"📩 <b>User Started the Bot</b>\n\n"  
            f"👤 <b>Name:</b> {full_name}\n"  
            f"🆔 <b>User ID:</b> <code>{user.id}</code>\n"  
            f"🔗 <b>Username:</b> {username}"  
        )  
        await client.send_message(LOGGER_ID, log_text)  

    if len(args) > 1 and args[1].startswith("vid_"):  
        video_id = args[1][4:]  
        video_data = await video_channels_collection.find_one({"video_id": video_id})  

        if not video_data:  
            return await message.reply("❌ Video not found. Please contact support.")  

        if video_data.get("status") != "paid":  
            return await message.reply("⚠️ Payment not yet confirmed. Please wait or contact support.")  

        video_file_id = video_data.get("file_id")  
        if not video_file_id:  
            return await message.reply("❌ Video file not available. Please contact support.")  

        try:  
            await client.send_video(chat_id=user.id, video=video_file_id)  
            return  
        except Exception as e:  
            return await message.reply(f"❌ Failed to send video: {e}")  

    text = (  
        f"<b>๏ нєу {user.first_name}.\n\n"  
        f"๏ ɪᴍ ꜱᴄᴏᴛᴛ 花 子 — ᴀ ʙᴏᴛ ʜᴇʟᴘ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ᴜʀ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴛʜᴇ ᴄᴏɴᴛᴇɴᴛ.\n"  
        f"๏ ᴀʟꜱᴏ ʜᴇʟᴘ ᴛᴏ ꜱᴇʟʟ ᴜʀ ᴄᴏɴᴛᴇɴᴛ ᴜꜱɪɴɢ ᴘᴀʏᴘᴀʟ ɪɴᴛᴇʀꜰᴀᴄᴇ.</b>"  
    )  

    keyboard = InlineKeyboardMarkup([  
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴄʜᴀɴɴᴇʟ ➕", url=f"https://t.me/{app.me.username}?startgroup=true")],  
        [  
            InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ", url=SUPPORT_CHAT),  
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=SUPPORT_CHANNEL)  
        ],  
        [  
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help_menu"),  
            InlineKeyboardButton("ᴜᴘʟᴏᴀᴅ", callback_data="search_user_status")  
        ],  
        [InlineKeyboardButton("ʀᴇɢɪꜱᴛᴇʀ & ʟᴏɢɪɴ", callback_data="command_menu")]  
    ])  

    await message.reply(  
        f"{text}\n\n<a href='{START_VIDEO}'>๏ ʟᴇᴛ'ꜱ ʙᴇɢɪɴ ᴛᴏ ꜱᴇᴄᴜʀᴇ ! 🛍️</a>",  
        reply_markup=keyboard  
    )

@app.on_callback_query(filters.regex("help_menu"))
async def help_menu(client, callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("𝗣ᴀʏᴘᴀʟ", callback_data="help_1"), InlineKeyboardButton("𝗥ᴇɢɪꜱᴛᴇʀ", callback_data="help_2")],
        [InlineKeyboardButton("ꜱᴏᴏɴ", callback_data="help_3"), InlineKeyboardButton("ꜱᴏᴏɴ", callback_data="help_4")],
        [InlineKeyboardButton("❌ Close", callback_data="close")]
    ])

    await callback_query.message.edit_text(
        f"<a href='{HELP_MENU_VIDEO}'>๏ 𝗛ᴇʟᴘ 𝗦ᴇᴄᴛɪᴏɴ</a>\n\n"
        "𝗖ʜᴏᴏꜱᴇ 𝗧ʜᴇ 𝗖ᴀᴛᴇɢᴏʀʏ 𝗙ᴏʀ 𝗪ʜɪᴄʜ 𝗬ᴏᴜ 𝗪ᴀɴɴᴀ 𝗚ᴇᴛ 𝗛ᴇʟᴩ.\n\n"
        "𝗔ꜱᴋ 𝗬ᴏᴜʀ 𝗗ᴏᴜʙᴛꜱ 𝗔ᴛ 𝗦ᴜᴘᴘᴏʀᴛ 𝗖ʜᴀᴛ:",
        reply_markup=keyboard,
        disable_web_page_preview=False
    )

@app.on_callback_query(filters.regex(r"help_[1-4]"))
async def show_help_section(client, callback_query: CallbackQuery):
    section = callback_query.data[-1]

    help_texts = {
        "1": "๏ <b>𝗣ᴀʏᴍᴇɴᴛ 𝗦ᴜᴘᴘᴏʀᴛ</b>\n\n𝗪ᴇ ᴀʀᴇ ᴘʟᴇᴀꜱᴇᴅ ᴛᴏ ɪɴꜰᴏʀᴍ ᴛʜᴀᴛ 𝘄ᴇ ꜱᴜᴘᴘᴏʀᴛ 𝗣ᴀʏ𝗣ᴀʟ ᴀꜱ 𝗚ʟᴏʙᴀʟ 𝗣ᴀʏᴍᴇɴᴛ ꜱᴜᴘᴘᴏʀᴛ, 𝗪ᴇ ᴡɪʟʟ ɪɴᴄʟᴜᴅᴇ ᴍᴏʀᴇ ᴘᴀʏᴍᴇɴᴛ ᴡᴀʟʟꜱ ꜱᴏᴏɴ.",
        
        "2": """ <b>ʀᴇɢɪꜱᴛʀᴀᴛɪᴏɴ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ </b>

๏  ᴛᴏ ʟᴏɢ ɪɴ ᴀɴᴅ ᴜsᴇ ʙᴏᴛ ғᴜɴᴄᴛɪᴏɴs, ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇɢɪsᴛᴇʀ ғɪʀsᴛ.
๏ ᴘᴀʀᴀ ɪɴɪᴄɪᴀʀ sᴇsɪᴏ‌ɴ ʏ ᴜsᴀʀ ʟᴀs ғᴜɴᴄɪᴏɴᴇs ᴅᴇʟ ʙᴏᴛ, ᴅᴇʙᴇs ʀᴇɢɪsᴛʀᴀʀᴛᴇ ᴘʀɪᴍᴇʀᴏ.

✹ ʜᴇʀᴇ ɪs ᴡʜᴀᴛ ʏᴏᴜ ᴡɪʟʟ ʙᴇ ᴀsᴋᴇᴅ ғᴏʀ:
✹ ᴇsᴛᴏ ᴇs ʟᴏ ǫᴜᴇ sᴇ ᴛᴇ ᴘᴇᴅɪʀᴀ‌:

[1] ᴀ ʀᴇᴀʟ ɢᴍᴀɪʟ ɪᴅ  
[1] ᴜɴᴀ ᴄᴜᴇɴᴛᴀ ʀᴇᴀʟ ᴅᴇ ɢᴍᴀɪʟ  
[2] ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ɪᴅ ᴡʜᴇʀᴇ ʙᴏᴛ sʜᴏᴜʟᴅ ʙᴇ ᴀᴅᴅᴇᴅ (ᴅᴀᴛᴀ ᴡɪʟʟ ʙᴇ sᴛᴏʀᴇᴅ ʜᴇʀᴇ)  
[2] ɪᴅ ᴅᴇ ᴄᴀɴᴀʟ ᴘʀɪᴠᴀᴅᴏ ᴅᴏɴᴅᴇ sᴇ ᴀɢʀᴇɢᴀʀᴀ‌ ᴇʟ ʙᴏᴛ (ᴀǫᴜɪ sᴇ ᴀʟᴍᴀᴄᴇɴᴀʀᴀ‌ ʟᴀ ɪɴғᴏʀᴍᴀᴄɪᴏ‌ɴ)  
[3] ᴘᴜʙʟɪᴄ ᴄʜᴀɴɴᴇʟ ɪᴅ ᴡʜᴇʀᴇ ʙᴏᴛ sʜᴏᴜʟᴅ ʙᴇ ᴀᴅᴅᴇᴅ (ᴜᴘʟᴏᴀᴅs ʜᴀᴘᴘᴇɴ ʜᴇʀᴇ)  
[3] ɪᴅ ᴅᴇ ᴄᴀɴᴀʟ ᴘᴜ‌ʙʟɪᴄᴏ ᴅᴏɴᴅᴇ sᴇ ᴀɢʀᴇɢᴀʀᴀ‌ ᴇʟ ʙᴏᴛ (ᴀǫᴜɪ sᴇ sᴜʙɪʀᴀ‌ ᴛᴏᴅᴏ)

[✓] ᴀғᴛᴇʀ ᴀʟʟ, ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ʏᴏᴜʀ ʟᴏɢɪɴ ɪᴅ ᴀɴᴅ ᴘᴀꜱꜱᴡᴏʀᴅ.
[✓] ᴀʟ ꜰɪɴᴀʟ, ʀᴇᴄɪʙɪʀᴀ‌s ᴛᴜ ɪᴅ ᴅᴇ ɪɴɪᴄɪᴏ ʏ ᴄᴏɴᴛʀᴀꜱᴇɴ‌ᴀ
""",

        "3": "📗 <b>Help Topic 3</b>\n\nExplain game roles or admin commands here.",
        "4": "📕 <b>Help Topic 4</b>\n\nAdd advanced gameplay or dev info here."
    }

    help_videos = {
        "1": HELP_VIDEO_1,
        "2": HELP_VIDEO_2,
        "3": HELP_VIDEO_3,
        "4": HELP_VIDEO_4
    }

    await callback_query.message.edit_text(
        f"<a href='{help_videos[section]}'>𝗛ᴇʟᴘ 𝗦ᴇᴄᴛɪᴏɴ</a>\n\n{help_texts[section]}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="help_menu")]
        ]),
        disable_web_page_preview=False
    )

@app.on_callback_query(filters.regex("close"))
async def close_menu(client, callback_query: CallbackQuery):
    await callback_query.message.delete()