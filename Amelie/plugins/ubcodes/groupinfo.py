from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode, ChatType

@Client.on_message(filters.command("ginfo", prefixes=".") & filters.me)
async def groupinfo_handler(client: Client, message: Message):
    chat = message.chat

    if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.edit_text("❌ This command can only be used in groups or supergroups.")
        return

    try:
        group_title = chat.title
        group_id = chat.id
        group_username = f"@{chat.username}" if chat.username else "No username"
        member_count = await client.get_chat_members_count(group_id)
        description = chat.description or "No description"

        text = (
            f"**👥 Group Info:**\n"
            f"**Title:** {group_title}\n"
            f"**ID:** `{group_id}`\n"
            f"**Username:** {group_username}\n"
            f"**Members:** `{member_count}`\n"
            f"**Description:**\n{description}"
        )

        await message.edit_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.edit_text(f"❌ Error: {e}")
