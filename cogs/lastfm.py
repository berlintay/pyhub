import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import logging
import os

load_dotenv()
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")


class LastFMCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="lastfm_user", description="Fetch and display user information from Last.fm")
    async def fetch_user_info(self, ctx, username: str):
        try:
            response = requests.get(
                f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={LASTFM_API_KEY}&format=json"
            )
            response.raise_for_status()
            data = response.json()

            if 'user' in data:
                user_info = data['user']
                embed = discord.Embed(title=f"Last.fm User: {user_info['name']}")
                embed.add_field(name="Playcount", value=user_info['playcount'])
                embed.add_field(name="Country", value=user_info.get('country', 'N/A'))
                embed.add_field(name="Profile URL", value=user_info['url'])
                await ctx.send(embed=embed)
            else:
                await ctx.send("User not found on Last.fm.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching user info from Last.fm: {e}")
            await ctx.send("An error occurred while fetching user information from Last.fm.")
        except Exception as e:
            logging.error(f"Unexpected error in 'lastfm_user' command: {e}")
            await ctx.send("An unexpected error occurred.")

    @commands.hybrid_command(name="lastfm_recent", description="Fetch and display user's recent tracks from Last.fm")
    async def fetch_recent_tracks(self, ctx, username: str):
        try:
            response = requests.get(
                f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={LASTFM_API_KEY}&format=json"
            )
            response.raise_for_status()
            data = response.json()

            if 'recenttracks' in data and 'track' in data['recenttracks']:
                tracks = data['recenttracks']['track']
                embed = discord.Embed(title=f"Recent Tracks for {username}")
                for track in tracks[:5]:  # Display up to 5 recent tracks
                    embed.add_field(name=track['name'], value=track['artist']['#text'], inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("No recent tracks found for this user on Last.fm.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching recent tracks from Last.fm: {e}")
            await ctx.send("An error occurred while fetching recent tracks from Last.fm.")
        except Exception as e:
            logging.error(f"Unexpected error in 'lastfm_recent' command: {e}")
            await ctx.send("An unexpected error occurred.")


async def setup(bot):
    await bot.add_cog(LastFMCog(bot))
