import discord
from discord.ext import commands
from dotenv import load_dotenv
from google_images_search import GoogleImagesSearch
import logging
import asyncio
import os

load_dotenv()
GCS_DEVELOPER_KEY = os.getenv("GCS_DEVELOPER_KEY")
GCS_CX = os.getenv("GCS_CX")


class ImageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)

    @commands.hybrid_command(name='image', description="Search for images from Google.")
    async def search_image(self, ctx, *, query):
        try:
            _search_params = {
                'q': query,
                'num': 10,
                'safe': 'off',
            }
            self.gis.search(search_params=_search_params)

            if not self.gis.results():
                await ctx.send("No images found for your search.")
                return

            current_page = 0
            total_pages = (len(self.gis.results()) - 1) // 10

            def create_embed():
                embed = discord.Embed(title=f"Image search Results for '{
                                      query}' ({current_page+1}/{total_pages+1})")
                embed.set_image(url=self.gis.results()[current_page * 5].url)
                return embed

            message = await ctx.send(embed=create_embed())
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

                    await message.edit(embed=create_embed())
                    await message.remove_reaction(reaction, ctx.author)

                except asyncio.TimeoutError:
                    await message.clear_reactions()
                    break

        except Exception as e:
            logging.error(f"Error during image search: {e}")
            await ctx.send(f"An error occurred while searching for '{query}'.")


async def setup(bot):
    await bot.add_cog(ImageCog(bot))
