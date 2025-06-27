from pyrogram import Client, filters
import asyncio

@Client.on_message(filters.command(["spam"], prefixes=["."]) & (filters.group | filters.channel | filters.private) & filters.me)
async def spam(client, message):
    try:
        args = message.text.split()
        if len(args) < 3:
            await message.edit_text("Usage: .spam {reason} {number_of_messages}")
            return

        try:
            number_of_messages = int(args[-1])
        except ValueError:
            await message.edit_text("Please enter a valid number of messages.")
            return

        reason = " ".join(args[1:-1])

        if number_of_messages <= 0:
            await message.edit_text("Number of messages must be greater than 0.")
            return

        await message.delete()

        for _ in range(number_of_messages):
            await message.reply_text(reason)
            await asyncio.sleep(2)

    except Exception as e:
        await message.edit_text(f"An error occurred: {str(e)}")