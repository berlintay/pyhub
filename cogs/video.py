import discord
from discord.ext import commands
from dotenv import load_dotenv
from googleapiclient.discovery import build
import asyncio
import logging

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


class VideoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    @commands.hybrid_command(name='video', description="search youtube videos.")
    async def search_video(self, ctx, *, query):
        try:
            request = self.youtube.search().list(
                part="snippet",
                maxResults=10,
                q=query,
                type='video'
            )
            response = request.execute()

            if not response['items']:
                await ctx.send("No videos found for your query.")
                return

            current_page = 0
            total_pages = len(response['items']) - 1

            def create_embed():
                item = response['items'][current_page]
                video_id = item['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                embed = discord.Embed(
                    title=item['snippet']['title'], url=video_url)
                embed.set_image(url=item['snippet']
                                ['thumbnails']['high']['url'])
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

        except Exception as e:
            logging.error(f"Error during video search: {e}")
            await ctx.send("An error occurred while searching for videos.")


async def setup(bot):
    await bot.add_cog(VideoCog(bot))
