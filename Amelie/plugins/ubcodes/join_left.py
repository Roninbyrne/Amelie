from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatType

@Client.on_message(filters.command("join", ".") & filters.me)
async def join_chatSS(_, message: Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = message.text.split(None, 1)[1]
    
    try:
        processing_message = await message.edit_text(f"Processing to join chat {text}...")
        
        await _.join_chat(chat_id=text)
        
        await processing_message.edit_text(f"Successfully joined chat {text}")
    except Exception as e:
        await processing_message.edit_text(f"Failed to join chat. Error: {e}")

@Client.on_message(filters.command("left", ".") & ~filters.private & filters.me)
async def left_chatSS(_, message: Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = message.text.split(None, 1)[1]
    
    try:
        processing_message = await message.edit_text(f"Processing to leave chat {text}...")
        
        await _.leave_chat(chat_id=text, delete=True)
        
        await processing_message.edit_text(f"Successfully left chat {text}")
    except Exception as e:
        await processing_message.edit_text(f"Failed to leave chat. Error: {e}")

@Client.on_message(filters.command("pm", ".") & filters.me)
async def pm_msg(_, message: Message):
    if len(message.text.split(None, 1)) < 2:
        return await message.edit_text("Provide username/id and message")

    args = message.text.split(None, 1)[1].strip()
    if " " not in args:
        return await message.edit_text("Please provide both a username/id and a message.")
    
    user, text = args.split(None, 1)
    
    if user.startswith("@"):
        user = user[1:]
    
    try:
        processing_message = await message.edit_text(f"Processing to send message to {user}...")
        
        await _.send_message(user, text)
        
        await processing_message.edit_text(f"Message sent to {user}")
    except Exception as e:
        await processing_message.edit_text(f"Failed to send message. Error: {e}")