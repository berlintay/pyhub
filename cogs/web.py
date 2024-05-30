import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
import logging
import asyncio

load_dotenv()
GCS_DEVELOPER_KEY = os.getenv("GCS_DEVELOPER_KEY")
GCS_CX = os.getenv("GCS_CX")


class WebSearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='search', description="Search google")
    async def search_web(self, ctx, *, query):
        try:
            search_params = {
                'q': query,
                'cx': GCS_CX,
                'key': GCS_DEVELOPER_KEY,
                'num': 10,
            }
            response = requests.get(
                "https://www.googleapis.com/customsearch/v1", params=search_params)
            response.raise_for_status()
            data = response.json()

            if 'items' not in data:
                await ctx.send("No results found for your search")
                return

            current_page = 0
            total_pages = len(data['items']) - 1

            def create_embed():
                item = data['items'][current_page]
                embed = discord.Embed(
                    title=item['title'], url=item['link'], description=item['snippet'])
                embed.set_footer(
                    text=f"Page {current_page+1} of {total_pages+1}")
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

        except requests.exceptions.RequestException as e:
            logging.error(f"Error during web search: {e}")
            await ctx.send("An error occurred while searching the web.")
        except Exception as e:
            logging.error(f"Unexpected error in web search: {e}")
            await ctx.send("An unexpected error occurred.")


async def setup(bot):
    await bot.add_cog(WebSearchCog(bot))
