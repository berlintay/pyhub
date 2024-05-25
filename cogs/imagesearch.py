from discord.ext import commands
from google_images_search import GoogleImagesSearch
import logging
import asyncio


config = configparser.ConfigParser()
config.read('config.ini')
GCS_DEVELOPER_KEY = config['GOOGLE']['GCS_DEVELOPER_KEY']
GCS_CX = config['GOOGLE']['GCS_CX']


class ImageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)

    @commands.hybrid_command(name='image', description="Search for images from Google.")
    async def search_image(self, ctx, *, query):
        try:
            _search_params = {
                'q': query,
                'num': 5,
                'safe': 'off',
            }
            self.gis.async_search(search_params=_search_params)

            if not self.gis.results():
                await ctx.send("No images found for your search.")
                return

            current_page = 0
            total_pages = (len(self.gis.results()) - 1) // 5

            def create_embed():
                embed = discord.Embed(title=f"Image search Results for '{
                                      query}' ({current_page+1}/{total_pages+1})")
                embed.set_image(url=self.gis.results()[current_page].url)
                return embed

        message = await ctx.send(embed=embed)
        await message.add_reaction('⬅️')
          await message.add_reaction('➡️')

           def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message == message

            while True:
                try:
                    reaction, _ = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                    if str(reaction.emoji) == '⬅️' and current_page > 0:
                        current_page -= 1
                    elif str(reaction.emoji) == '➡️' and current_page < total_pages:
                        current_page += 1
                        embed.set_image(url=self.gis.results()
                                        [current_page * 5].url)
                        embed.title = f"Results for '{
                            query}' ({current_page+1}/{total_pages+1})"
                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, ctx.author)

                    except asyncio.TimeoutError:
                        await message.clear_reactions()
                        break
            except Exception as e:
                logging.error(f"Error during image search: {e}")
                await ctx.send("An error occured while searching for '{query}'.")

    async def setup(bot):
        await bot.add_cog(ImageCog(bot))
import discord
from discord.ext import commands
from google_images_search import GoogleImagesSearch
import logging
import asyncio


config = configparser.ConfigParser()
config.read('config.ini')
GCS_DEVELOPER_KEY = config['GOOGLE']['GCS_DEVELOPER_KEY']
GCS_CX = config['GOOGLE']['GCS_CX']


class ImageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)

    @commands.hybrid_command(name='image', description="Search for images from Google.")
    async def search_image(self, ctx, *, query):
        try:
            _search_params = {
                'q': query,
                'num': 5,
                'safe': 'off',
            }
            self.gis.async_search(search_params=_search_params)

            if not self.gis.results():
                await ctx.send("No images found for your search.")
                return

            current_page = 0
            total_pages = (len(self.gis.results()) - 1) // 5

            def create_embed():
                embed = discord.Embed(title=f"Image search Results for '{query}' ({current_page+1}/{total_pages+1})")
                embed.set_image(url=self.gis.results()[current_page].url)
                return embed

        message = await ctx.send(embed=embed)
        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️'] and

        while True:
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                if str(reaction.emoji) == '⬅️' and current_page > 0:
                    current_page -= 1
                elif str(reaction.emoji) == '➡️' and current_page < total_pages:
                    current_page += 1

                    await message.edit(embed=create_embed())
                    await message.remove_reaction(reaction, ctx.author)

                except asyncio.TimeoutError:
                    await message.clear_reactions()
                    break
            except Exception as e:
                logging.error(f"Error during image search: {e}")
                await ctx.send("An error occured while searching for '{query}'.")

    async def setup(bot):
        await bot.add_cog(ImageCog(bot))
