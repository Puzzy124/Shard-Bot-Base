import os
import asyncio
import importlib
import traceback
from typing import Optional
from dotenv import load_dotenv

from discord.ext.commands import Bot
import discord

from config import settings

load_dotenv()

BOT: Bot = Bot(command_prefix=',', help_command=None, intents=discord.Intents.all())

# load all cogs dynamically from ./cogs
async def load_cogs(bot: Bot) -> None:
    for root, _, files in os.walk("cogs"):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                cog_path = os.path.relpath(os.path.join(root, file)).replace(os.path.sep, '.')[:-3]
                try:
                    module = importlib.import_module(cog_path)
                    if getattr(module, "COG", False):
                        await bot.load_extension(cog_path)
                        print(f"Loaded cog: {cog_path}")
                except Exception:
                    traceback.print_exc()

async def main() -> None:
    await load_cogs(BOT)
    await BOT.start(settings.token)


if __name__ == "__main__":
    asyncio.run(main())