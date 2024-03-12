from pyrogram import Client, filters
from pyrogram.types import Message

from EvaMaria.helpers.get_file_id import get_file_id
from EvaMaria.config import HNDLR


# Command to show user or chat ID
@app.on_message(filters.command(["id"], prefixes=f"{HNDLR}"))
async def show_id(client, message: Message):
    chat_type = message.chat.type

    if chat_type == "private":
        user_id = message.chat.id
        await message.reply_text(f"<code>{user_id}</code>", parse_mode="html")

    elif chat_type in ["group", "supergroup"]:
        chat_id = message.chat.id
        reply_user_id = None
        file_info = None

        if message.reply_to_message:
            reply_user_id = message.reply_to_message.from_user.id
            file_info = get_file_id(message.reply_to_message)
        else:
            reply_user_id = message.from_user.id
            file_info = get_file_id(message)

        text = f"<b>ID group:</b> <code>{chat_id}</code>\n"
        text += f"<b>ID User:</b> <code>{reply_user_id}</code>\n"

        if file_info:
            text += f"<b>{file_info.message_type}:</b> <code>{file_info.file_id}</code>\n"

        await message.reply_text(text, parse_mode="html")
