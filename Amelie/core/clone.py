from pyrogram import Client
from config import (
    API_ID,
    API_HASH,
    String_client_1,
    String_client_2,
    String_client_3,
)

userbots = []

def create_userbot(session_string):
    return Client(
        name=f"userbot_{session_string[-5:]}",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )

string_sessions = [String_client_1, String_client_2, String_client_3]
for session in string_sessions:
    if session:
        client = create_userbot(session)
        userbots.append(client)

async def restart_bots():
    print("🔄 Restarting all userbots...")
    for client in userbots:
        try:
            await client.stop()
            await client.start()
            me = await client.get_me()
            print(f"✅ Restarted userbot: {me.first_name} (@{me.username})")
        except Exception as e:
            print(f"❌ Failed to restart userbot: {e}")