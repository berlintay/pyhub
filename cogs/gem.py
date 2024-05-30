import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import logging

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class GemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="gem", description="Ask a question to Gemini Pro")
    async def ask_gemini_slash(self, ctx, question: str):
        try:
            headers = {'Authorization': f'Bearer {GEMINI_API_KEY}'}
            response = requests.post(
                'https://api.gemini.com/v1/completions',
                headers=headers,
                json={'prompt': question}
            )
            response.raise_for_status()
            data = response.json()

            if 'choices' in data and len(data['choices']) > 0:
                answer = data['choices'][0]['text']
                embed = discord.Embed(title="Gem says:", description=answer)
                await ctx.send(embed=embed)
            else:
                logging.error(
                    "The API response format for Gemini Pro has changed, Unable to extract response.")
                await ctx.send("Unexpected response from gem <:SatisfiedCheems:1230175084912840734>")
        except requests.exceptions.RequestException as e:  # Moved except block out of the if/else
            logging.error(f"Error communicating with Gemini API: {e}")
            await ctx.send("An error occurred while communicating with Gemini Pro. Try again.")
        except Exception as e:  # Moved except block out of the if/else
            logging.error(f"Random error in 'gem' command: {e}")
            await ctx.send("Gem is not working at the moment.")


async def setup(bot):
    await bot.add_cog(GemCog(bot))
