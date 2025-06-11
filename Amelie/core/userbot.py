from pyrogram import Client
from config import (
    API_ID,
    API_HASH,
    String_client_1,
    String_client_2,
    String_client_3,
    mustjoin
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
            try:
                await client.join_chat(mustjoin)
                await client.send_message(
                    chat_id=mustjoin,
                    text=(
                        "✅ **Userbot is started**\n"
                        f"**Name:** {me.first_name}\n"
                        f"**Username:** @{me.username if me.username else 'N/A'}\n"
                        f"**User ID:** `{me.id}`"
                    )
                )
                print(f"📥 Joined and sent message in {mustjoin}")
            except Exception as join_err:
                print(f"⚠️ Failed to join or send message in {mustjoin}: {join_err}")
        except Exception as e:
            print(f"❌ Failed to restart userbot: {e}")