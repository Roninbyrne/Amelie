
from gpytranslate import SyncTranslator
from pyrogram import filters, Client
from pyrogram.enums import ParseMode

trans = SyncTranslator()

@Client.on_message(filters.command("tr", ".") & filters.me)
async def totranslate(client, message):
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text(
            "ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇs ᴏʀ ᴡʀɪᴛᴇ ᴍᴇssᴀɢᴇs ғʀᴏᴍ ᴏᴛʜᴇʀ ʟᴀɴɢᴜᴀɢᴇs ғᴏʀ ᴛʀᴀɴsʟᴀᴛɪɴɢ ɪɴᴛᴏ ᴛʜᴇ ɪɴᴛᴇɴᴅᴇᴅ ʟᴀɴɢᴜᴀɢᴇ\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/tr en-hi` ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ ғʀᴏᴍ ᴇɴɡʟɪsʜ ᴛᴏ ʜɪɴᴅɪ\n"
            "ᴏʀ ᴜsᴇ: `/tr en` ғᴏʀ ᴀᴜᴛᴏᴍᴀᴛɪᴄ ᴅᴇᴛᴇᴄᴛɪᴏɴ ᴀɴᴅ ᴛʀᴀɴsʟᴀᴛɪɴɢ ɪᴛ ɪɴᴛᴏ ᴇɴɢʟɪsʜ.\n"
            "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ sᴇᴇ [ʟɪsᴛ ᴏғ ᴀᴠᴀɪʟᴀʙʟᴇ ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇs](https://t.me/PhoenixXsupport/114706).",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        return

    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    else:
        await message.edit_text("Nothing to translate.")
        return

    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = trans.detect(to_translate)
            dest = args
    except IndexError:
        source = trans.detect(to_translate)
        dest = "en"
    
    try:
        translation = trans(to_translate, sourcelang=source, targetlang=dest)
        reply = (
            f"<b>ᴛʀᴀɴsʟᴀᴛᴇᴅ ғʀᴏᴍ {source} ᴛᴏ {dest}</b> :\n"
            f"<code>{translation.text}</code>"
        )
    except Exception as e:
        reply = f"<b>ᴇʀʀᴏʀ:</b> <code>{str(e)}</code>"

    await message.edit_text(reply, parse_mode=ParseMode.HTML)