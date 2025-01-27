import discord
from discord.ext import commands
import tweepy
import os

class SocialSearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitter_api = self.authenticate_twitter()

    def authenticate_twitter(self):
        auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET_KEY"))
        auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))
        return tweepy.API(auth)

    @commands.hybrid_command(name="search_tweets", description="Search for tweets based on a query.")
    async def search_tweets(self, ctx, *, query):
        try:
            tweets = self.twitter_api.search(q=query, count=10, tweet_mode='extended')
            if not tweets:
                await ctx.send("No tweets found for your query.")
                return

            embed = discord.Embed(title=f"Search results for '{query}'")
            for tweet in tweets:
                embed.add_field(name=f"@{tweet.user.screen_name}", value=tweet.full_text, inline=False)

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred while searching for tweets: {e}")

async def setup(bot):
    await bot.add_cog(SocialSearchCog(bot))
