from pyrogram import Client, filters
import asyncio

@Client.on_message(filters.command(["fspam"], prefixes=["."]) & (filters.group | filters.channel | filters.private) & filters.me)
async def fspam(client, message):
    try:
        args = message.text.split()
        if len(args) < 4:
            await message.edit_text("Usage: .fspam {reason} {number_of_messages} {delay_in_seconds}")
            return

        try:
            number_of_messages = int(args[-2])
            delay = float(args[-1])
        except ValueError:
            await message.edit_text("Please enter valid numbers for the number of messages and delay.")
            return

        reason = " ".join(args[1:-2])

        if number_of_messages <= 0:
            await message.edit_text("Number of messages must be greater than 0.")
            return
        if delay <= 0:
            await message.edit_text("Delay must be greater than 0.")
            return

        await message.delete()

        for _ in range(number_of_messages):
            await message.reply_text(reason)
            await asyncio.sleep(delay)

    except Exception as e:
        await message.edit_text(f"An error occurred: {str(e)}")