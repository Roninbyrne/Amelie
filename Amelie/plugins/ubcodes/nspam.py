from pyrogram import Client, filters
import asyncio

photo_urls = [
    "https://graph.org//file/d1ae9c8cd06d025ec50d5.jpg",
    "https://graph.org//file/50bc0fe2f6f998394b309.jpg",
    "https://graph.org//file/833aa87a991d3f24103da.jpg",
]

@Client.on_message(filters.command(["nspam"], prefixes=["."]) & (filters.group | filters.channel | filters.private) & filters.me)
async def rspam(client, message):
    try:
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            await message.edit_text("Usage: .nspam {number_of_photos} {speed_in_seconds}")
            return

        number_of_photos = int(args[1])
        speed = float(args[2])

        if number_of_photos <= 0:
            await message.edit_text("Number of photos must be greater than 0.")
            return

        if speed <= 0:
            await message.edit_text("Speed must be a positive number.")
            return

        await message.delete()

        total_photos = len(photo_urls)
        for i in range(number_of_photos):
            photo_url = photo_urls[i % total_photos]
            await message.reply_photo(photo_url)
            await asyncio.sleep(speed)

    except ValueError:
        await message.edit_text("Please enter valid numbers for the number of photos and speed.")