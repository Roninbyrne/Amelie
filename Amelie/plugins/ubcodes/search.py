import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from MukeshAPI import api
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def question(message):
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        try:
            text = message.text.split(None, 1)[1]
        except IndexError:
            return await message.reply("Please provide a query.")
    return text

@Client.on_message(
    filters.command(["gpt", "ask"], prefixes=["."]) & filters.me
)
async def chatgpt_reply(b, message):
    query = await question(message)
    if not query:
        return

    await message.edit("Processing your request...", parse_mode=ParseMode.MARKDOWN)

    start_time = time.time()

    try:
        search_result = await asyncio.to_thread(api.gemini, query)
        elapsed_time = time.time() - start_time
        logger.info(f"Query processed in {elapsed_time:.2f}s. Query: {query}")
        
        if not search_result or not search_result.get("results"):
            await message.edit("No results found for your query.")
            return

        formatted_result = format_search_results(search_result["results"])
        await message.edit(formatted_result, parse_mode=ParseMode.MARKDOWN)
    
    except Exception as e:
        logger.error(f"Error while processing the request: {e}")
        await message.edit(f"Error occurred while processing the request: {str(e)}")

def format_search_results(results):
    if isinstance(results, list) and len(results) > 0:
        formatted = "\n\n".join([f"• {result}" for result in results])
        return formatted[:4000] if len(formatted) > 4000 else formatted
    elif isinstance(results, dict):
        return "\n".join([f"{key}: {value}" for key, value in results.items()])
    else:
        return str(results)