from discord.ext import commands

COG: bool = True

class OnReadyCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        tree = await self.bot.tree.sync()
        print("Synced {cmds} commands".format(cmds=len(tree)))
        print(f'Logged in as {self.bot.user}')
        print('------')

async def setup(bot):
    await bot.add_cog(OnReadyCog(bot))
