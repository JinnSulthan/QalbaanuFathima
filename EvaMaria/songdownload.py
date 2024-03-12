from pyrogram import Client, filters
from pyrogram.types import Message

from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

import asyncio
import math
import os
import time
import wget

from config import HNDLR


@Client.on_message(filters.command(["song", "music"], prefixes=f"{HNDLR}"))
async def song_command(client, message: Message):
    url = get_text(message)
    if not url:
        await message.reply("⚠️ Check spelling!")
        return

    search = VideosSearch(url, limit=1)
    result = search.result()
    video_info = result["result"][0]

    video_link = video_info["link"]
    thumbnail_url = video_info["thumbnails"][0]

    thumbnail_path = wget.download(thumbnail_url)

    ydl_opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_link])
    except Exception as e:
        await message.reply(f"Failed to download the song. Error: {e}")
        return

    file_name = f"{video_info['id']}.mp3"

    caption = (
        f"🎵 **Title:** [{video_info['title']}]({video_link})\n"
        f"⏳ **Duration:** {video_info['duration']}\n"
        f"📸 **Thumbnail:** [Link]({thumbnail_url})"
    )

    await client.send_audio(
        message.chat.id,
        audio=file_name,
        title=video_info['title'],
        performer=video_info['channel']['name'],
        thumb=thumbnail_path,
        duration=video_info['duration'],
        caption=caption,
    )

    for file_path in [thumbnail_path, file_name]:
        if os.path.exists(file_path):
            os.remove(file_path)


@Client.on_message(filters.command(["vsong", "video"], prefixes=f"{HNDLR}"))
async def video_song_command(client, message: Message):
    url = get_text(message)
    if not url:
        await message.reply("⚠️ Check spelling!")
        return

    search = VideosSearch(url, limit=1)
    result = search.result()
    video_info = result["result"][0]

    video_link = video_info["link"]
    thumbnail_url = video_info["thumbnails"][0]

    thumbnail_path = wget.download(thumbnail_url)

    ydl_opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "quiet": True,
        "logtostderr": False,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_link])
    except Exception as e:
        await message.reply(f"Failed to download the video. Error: {e}")
        return

    file_name = f"{video_info['id']}.mp4"

    caption = (
        f"🎥 **Title:** [{video_info['title']}]({video_link})\n"
        f"⏳ **Duration:** {video_info['duration']}\n"
        f"📸 **Thumbnail:** [Link]({thumbnail_url})"
    )

    await client.send_video(
        message.chat.id,
        video=file_name,
        caption=caption,
    )

    for file_path in [thumbnail_path, file_name]:
        if os.path.exists(file_path):
            os.remove(file_path)


def get_text(message: Message) -> [None, str]:
    if message.text:
        text_parts = message.text.split(" ", 1)
        if len(text_parts) > 1:
            return text_parts[1]
    return None
