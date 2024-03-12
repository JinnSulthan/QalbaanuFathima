from pyrogram import Client
from pytgcalls import idle
from config import call_py

async def main():
    async with Client("my_account") as app:
        await call_py.start(app)
        print(
            """
        -------------------
       | Fathima Started! |
        -------------------
    """
        )
        await idle()

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
