import discord
from discord.ext import commands

class EmbedCreateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="create_embed", description="Create a social card embed.")
    async def create_embed(self, ctx, title: str, description: str, image_url: str):
        embed = discord.Embed(title=title, description=description)
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EmbedCreateCog(bot))
