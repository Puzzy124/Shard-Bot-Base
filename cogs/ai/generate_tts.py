from discord.ext import commands
from discord import app_commands
import discord
from io import BytesIO

import sys
sys.path.append("...")

from helpers.ai.elevenlabs import ElevenLabs
from helpers.common import rate_limit
from config import RateLimitedError

import traceback

COG: bool = True

class GenTTSCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="generate-tts", description="Generate an TTS message")
    @app_commands.describe(prompt="What do you want to generate?")
    @app_commands.choices(
        voice=[
            app_commands.Choice(name="👧 Alice", value="alice"),
            app_commands.Choice(name="👦 Bill", value="bill"),
            app_commands.Choice(name="👨 Brian", value="brian"),
            app_commands.Choice(name="👦 Callum", value="callum"),
            app_commands.Choice(name="👩 Charlie", value="charlie"),
            app_commands.Choice(name="👧 Charlotte", value="charlotte"),
            app_commands.Choice(name="👨 Chris", value="chris"),
            app_commands.Choice(name="👨 Daniel", value="daniel"),
            app_commands.Choice(name="👦 George", value="george"),
            app_commands.Choice(name="👦 Liam", value="liam"),
            app_commands.Choice(name="👧 Lily", value="lily"),
            app_commands.Choice(name="👧 Matilda", value="matilda"),
        ]
    )
    @rate_limit('ai', 5)
    async def generate_image_cmd(self, interaction: discord.Interaction, prompt: str, voice: app_commands.Choice[str]):
        try:
            await interaction.response.defer()
            speech_bytes = BytesIO(await ElevenLabs.speech(prompt, voice.value))

            file = discord.File(speech_bytes, 'tts.mp3', spoiler=False)

            embed = discord.Embed(title=f"Generated TTS for {interaction.user.display_name}!")
            await interaction.followup.send(embed=embed, file=file)
        except:
            traceback.print_exc()
            raise ValueError
        
async def setup(bot):
    await bot.add_cog(GenTTSCog(bot))
