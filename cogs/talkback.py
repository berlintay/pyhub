import discord
from discord.ext import commands
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class TalkBackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.predefined_responses = {
            "hello": "Hi there! How can I assist you today?",
            "bye": "Goodbye! Have a great day!",
            "thanks": "You're welcome!",
            "help": "Sure, I'm here to help! What do you need assistance with?"
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Check for predefined responses
        for key, response in self.predefined_responses.items():
            if key in message.content.lower():
                await message.channel.send(response)
                return

        # If no predefined response, use chatbot API
        response = self.get_chatbot_response(message.content)
        await message.channel.send(response)

    def get_chatbot_response(self, user_input):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_input,
                max_tokens=150
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Sorry, I couldn't process that. Error: {e}"

async def setup(bot):
    await bot.add_cog(TalkBackCog(bot))
