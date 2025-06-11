import asyncio
import importlib
import threading
from pyrogram import idle
from Scott import LOGGER, app, start_bot
from Scott.plugins import ALL_MODULES
from Scott.core.chat_tracker import verify_groups_command
from config import OWNER_ID

from Scott.core.webhook import app_webhook

class DummyUser:
    id = OWNER_ID

class DummyMessage:
    from_user = DummyUser()

    async def reply_text(self, *args, **kwargs):
        pass

def run_flask():
    app_webhook.run(host="0.0.0.0", port=5000)

async def init():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    await start_bot()

    for all_module in ALL_MODULES:
        importlib.import_module("Scott.plugins" + all_module)
    LOGGER("Scott.plugins").info("✅ Successfully imported all modules.")

    try:
        dummy_message = DummyMessage()
        await verify_groups_command(app, dummy_message)
        LOGGER("Scott").info("🔁 Automatically verified groups on startup.")
    except Exception as e:
        LOGGER("Scott").warning(f"⚠️ Failed to verify groups on startup: {e}")

    LOGGER("Scott").info("🚀 Scott Game Bot Started Successfully.")
    await idle()

    await app.stop()
    LOGGER("Scott").info("🛑 Stopping Scott Game Bot...")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())