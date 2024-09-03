import discord
from discord.ext import commands

import sys
sys.path.append("...")

from config import RateLimitedError

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, RateLimitedError):
            embed = discord.Embed(title=error.title, description=error.body, color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Something went wrong, try again later",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
