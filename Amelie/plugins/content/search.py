from pyrogram import filters
from pyrogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from Amelie import app
from Amelie.core.mongo import session_db, register_data_db, video_channels_collection, user_states_collection
import logging
import paypalrestsdk
from config import PAYPAL_CLIENT_ID, PAYPAL_SECRET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

paypalrestsdk.configure({
    "mode": "live",
    "client_id": PAYPAL_CLIENT_ID,
    "client_secret": PAYPAL_SECRET
})

user_states = {}

class InPostingFlow(filters.Filter):
    def __init__(self):
        super().__init__()

    async def __call__(self, client, message):
        user_id = message.from_user.id
        state = user_states.get(user_id)
        return state and state.get("step") in [
            "awaiting_description",
            "awaiting_photo",
            "get_video_link",
            "set_price",
            "get_description",
            "get_cover_photo"
        ]

in_posting_flow = InPostingFlow()

@app.on_callback_query(filters.regex("search_user_status"))
async def search_user_status(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    session = await session_db.find_one({"_id": user_id})
    if not session or not session.get("logged_in"):
        return await callback_query.message.edit_text("❌ You are not logged in. Please log in first using your Login ID.")
    login_id = session.get("login_id")
    if not login_id:
        return await callback_query.message.edit_text("⚠️ Login ID not found in session. Please log in again.")
    register_data = await register_data_db.find_one({"_id": login_id})
    if not register_data:
        return await callback_query.message.edit_text("⚠️ Registration data not found. Please complete your setup.")

    private_channel = register_data.get("private_channel")
    public_channel = register_data.get("public_channel")

    if not private_channel and not public_channel:
        text = "🔗 You're logged in, but no channels are linked. Please link a group or channel."
    else:
        text = "✅ Login verified!"
        if private_channel:
            text += f"\n🔒 Private Channel ID: <code>{private_channel}</code>"
        if public_channel:
            text += f"\n🌐 Public Channel ID: <code>{public_channel}</code>"

    await callback_query.message.edit_text(text)

    if public_channel:
        user_states[user_id] = {
            "step": "get_video_link",
            "public_channel": public_channel,
            "private_channel": private_channel
        }
        await client.send_message(user_id, "📝 Please send the video message link to upload.")

@app.on_message(filters.private & filters.text & in_posting_flow)
async def handle_text_messages(client, message: Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    if not state:
        return

    step = state.get("step")

    if step == "get_video_link":
        state["video_link"] = message.text.strip()
        state["step"] = "set_price"
        await message.reply("✅ Please enter the minimum price in USD (min $0.01):")

    elif step == "set_price":
        try:
            price = float(message.text.strip())
            if price < 0.01:
                return await message.reply("❌ Minimum price is $0.01. Enter a valid amount.")
            state["price"] = price
            state["step"] = "get_description"
            await message.reply(f"✅ Price set to ${price}. Now provide a description.")
        except ValueError:
            await message.reply("❌ Invalid price. Please enter a number.")

    elif step == "get_description":
        state["description"] = message.text.strip()
        state["step"] = "get_cover_photo"
        await message.reply("Please send the cover photo.")

@app.on_message(filters.private & filters.photo & in_posting_flow)
async def handle_photo_messages(client, message: Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    if not state:
        return

    if state.get("step") == "get_cover_photo":
        cover_photo = message.photo.file_id
        video_link = state.get("video_link")
        description = state.get("description")
        public_channel = state.get("public_channel")
        private_channel = state.get("private_channel")
        video_id = video_link.split("/")[-1]
        price = state.get("price")

        await post_video_to_channel(user_id, public_channel, video_id, description, cover_photo, price)

        await video_channels_collection.update_one(
            {"video_id": video_id},
            {"$set": {
                "public_channel": public_channel,
                "private_channel": private_channel,
                "price": price,
                "file_id": video_link,
                "user_id": user_id,
                "status": "pending"
            }},
            upsert=True
        )
        await message.reply("✅ Video details uploaded to the public channel!")
        user_states.pop(user_id, None)

async def post_video_to_channel(user_id, public_channel, video_id, description, cover_photo, price):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton(
            f"💳 Pay ${price} to Download",
            url=(
                f"https://www.paypal.com/cgi-bin/webscr"
                f"?cmd=_xclick"
                f"&business=roninnn1406@gmail.com"
                f"&item_name=Video_{video_id}"
                f"&amount={price}"
                f"&currency_code=USD"
                f"&custom={user_id}_{video_id}"
                f"&return=https://t.me/{app.me.username}?start=vid_{video_id}"
            )
        )]]
    )

    caption_text = f"{description}\n\n❱ Support Chat: <a href='https://t.me/phoenixXsupport'>Click here</a>"

    await app.send_photo(
        chat_id=public_channel,
        photo=cover_photo,
        caption=caption_text,
        reply_markup=button,
        parse_mode=ParseMode.HTML
    )
