from discord.ext import commands
from discord import app_commands
import discord
from io import BytesIO

import sys
sys.path.append("...")

from helpers.ai import image_generator
from helpers.common import rate_limit
from config import RateLimitedError

import traceback

COG: bool = True

class AskAICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="generate-image", description="Generate an AI image")
    @app_commands.describe(prompt="What do you want to generate?")
    async def generate_image_cmd(self, interaction: discord.Interaction, prompt: str):
        try:
            await interaction.response.defer()
            image_bytes = BytesIO(await image_generator.ImageGenerator.main(prompt))

            file = discord.File(image_bytes, 'image.png', spoiler=True)

            embed = discord.Embed(title=f"Generated image for {interaction.user.display_name}!")
            await interaction.followup.send(embed=embed, file=file)
        except:
            traceback.print_exc()
            raise ValueError
        
async def setup(bot):
    await bot.add_cog(AskAICog(bot))
