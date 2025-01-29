import discord
from discord.ext import commands
import pylast
import os
from dotenv import load_dotenv

load_dotenv()

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_API_SECRET = os.getenv("LASTFM_API_SECRET")

class LastFM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.network = pylast.LastFMNetwork(
            api_key=LASTFM_API_KEY,
            api_secret=LASTFM_API_SECRET
        )
        
    @commands.command(name="nowplaying", aliases=["np"])
    async def now_playing(self, ctx, username=None):
        if username is None:
            return await ctx.send("Please provide a Last.fm username!")
            
        try:
            user = self.network.get_user(username)
            current_track = user.get_now_playing()
            
            if current_track is None:
                return await ctx.send(f"{username} is not currently playing anything!")
            
            # Create embed
            embed = discord.Embed(
                title="Now Playing",
                color=discord.Color.purple()  # You can customize the color
            )
            
            # Add track information
            embed.add_field(
                name="Track",
                value=current_track.get_title(),
                inline=False
            )
            embed.add_field(
                name="Artist",
                value=current_track.get_artist().get_name(),
                inline=True
            )
            
            # Try to get album info
            try:
                album = current_track.get_album()
                if album:
                    embed.add_field(
                        name="Album",
                        value=album.get_name(),
                        inline=True
                    )
            except:
                pass
                
            # Set thumbnail if available
            try:
                cover = current_track.get_album().get_cover_image()
                if cover:
                    embed.set_thumbnail(url=cover)
            except:
                pass
                
            embed.set_footer(text=f"Last.fm: {username}")
            
            await ctx.send(embed=embed)
            
        except pylast.WSError:
            await ctx.send("User not found or Last.fm API error!")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(LastFM(bot))