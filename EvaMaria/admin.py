from pyrogram import Client, filters
from pyrogram.types import Message

from config import HNDLR, call_py
from EvaMaria.helpers.decorators import authorized_users_only
from EvaMaria.helpers.handlers import skip_current_song, skip_item
from EvaMaria.helpers.queues import QUEUE, clear_queue


@Client.on_message(filters.command(["skip"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def skip_command(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply_text("**🙄 There's nothing in the queue to skip!**")
        elif op == 1:
            await m.reply_text("**😩 Empty Queue, Leaving Voice Chat**")
        else:
            await m.reply_text(
                f"**⏭ Skipped**\n**🎧 Now playing** - [{op[0]}]({op[1]}) | `{op[2]}`",
                disable_web_page_preview=True,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "**🗑️ Removed the following songs from the Queue: -**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#⃣{x}** - {hm}"
            await m.reply_text(OP)


@Client.on_message(filters.command(["end", "stop"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def stop_command(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply_text("**😐 End**")
        except Exception as e:
            await m.reply_text(f"**ERROR**\n`{e}`")
    else:
        await m.reply_text("**🤨 Nothing is playing!**")


@Client.on_message(filters.command(["pause"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def pause_command(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply_text(
                f"**⏸ Paused.**\n\n• To resume playback, use the command » {HNDLR}resume"
            )
        except Exception as e:
            await m.reply_text(f"**ERROR**\n`{e}`")
    else:
        await m.reply_text("**🤨 Nothing is playing!**")


@Client.on_message(filters.command(["resume"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def resume_command(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply_text(
                f"**▶ Resumed**\n\n• To pause playback, use the command » {HNDLR}pause"
            )
        except Exception as e:
            await m.reply_text(f"**ERROR**\n`{e}`")
    else:
        await m.reply_text("**🙄 Nothing is currently paused!**")
