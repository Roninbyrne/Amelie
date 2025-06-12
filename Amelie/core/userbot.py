from pyrogram import Client, idle
from pyrogram.errors import SessionRevoked, AuthKeyInvalid
from Amelie import LOGGER
from config import (
    API_ID,
    API_HASH,
    String_client_1,
    String_client_2,
    String_client_3,
    Mustjoin
)
import importlib
import pkgutil
from Amelie.plugins import ubcodes

string_sessions = [String_client_1, String_client_2, String_client_3]
userbot_clients = []

def load_userbot_handlers(client: Client):
    for _, module_name, _ in pkgutil.iter_modules(ubcodes.__path__):
        full_module = f"Amelie.plugins.ubcodes.{module_name}"
        try:
            module = importlib.import_module(full_module)
            if hasattr(module, "register_userbot"):
                module.register_userbot(client)
        except Exception as e:
            LOGGER("Userbot").warning(f"⚠️ Failed to load {full_module}: {e}")

async def restart_bots():
    LOGGER("Userbot").info("🔄 Restarting all userbots...")
    for i, session in enumerate(string_sessions, start=1):
        if not session:
            LOGGER("Userbot").warning(f"⚠️ String_client_{i} is empty or not set, skipping...")
            continue

        try:
            client = Client(
                name=f"userbot_{i}",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=session,
            )
            await client.start()
            load_userbot_handlers(client)
            me = await client.get_me()
            LOGGER("Userbot").info(f"🟢 String_client_{i} started as {me.first_name} (@{me.username})")

            try:
                await client.join_chat(Mustjoin)
                LOGGER("Userbot").info(f"📥 {me.first_name} joined {Mustjoin}")
                await client.send_message(
                    chat_id=Mustjoin,
                    text=(
                        "✅ **Userbot is started**\n"
                        f"**Name:** {me.first_name}\n"
                        f"**Username:** @{me.username if me.username else 'N/A'}\n"
                        f"**User ID:** `{me.id}`"
                    )
                )
            except Exception as join_err:
                LOGGER("Userbot").warning(f"⚠️ {me.first_name} failed to join/send in {Mustjoin}: {join_err}")

            userbot_clients.append(client)

        except (SessionRevoked, AuthKeyInvalid):
            LOGGER("Userbot").error(f"🧟‍♂️ String_client_{i} is dead or revoked. Please generate a new one.")
        except Exception as e:
            LOGGER("Userbot").error(f"❌ Failed to start String_client_{i}: {e}")

    if userbot_clients:
        await idle()