import discord
from discord.ext import commands
from discord import app_commands
import os
from together import Together
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.together_client = Together(os.getenv('TOGETHERAI_TOKEN'))
        self.mistral_client = MistralClient(api_key=os.getenv('MISTRALAI_KEY'))

    @app_commands.command(name="chat", description="Chat with an AI (TogetherAI or MistralAI)")
    @app_commands.choices(model=[
        app_commands.Choice(name="TogetherAI", value="together"),
        app_commands.Choice(name="MistralAI", value="mistral")
    ])
    async def chat(self, interaction: discord.Interaction, model: app_commands.Choice[str], message: str):
        await interaction.response.defer()

        try:
            if model.value == "together":
                response = self.together_client.chat(
                    messages=[{"role": "user", "content": message}],
                    model="mistral-7b-instruct"
                )
                ai_response = response['output']['content']

            else:  # mistral
                messages = [ChatMessage(role="user", content=message)]
                response = self.mistral_client.chat(
                    model="mistral-tiny",
                    messages=messages
                )
                ai_response = response.choices[0].message.content

            # Split response if it exceeds Discord's limit
            if len(ai_response) > 2000:
                chunks = [ai_response[i:i+2000] for i in range(0, len(ai_response), 2000)]
                for chunk in chunks:
                    await interaction.followup.send(chunk)
            else:
                await interaction.followup.send(ai_response)

        except Exception as e:
            await interaction.followup.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(AIChat(bot))import discord
from discord.ext import commands
from discord import app_commands
import os
from together import Together
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.together_client = Together(os.getenv('TOGETHERAI_TOKEN'))
        self.mistral_client = MistralClient(api_key=os.getenv('MISTRALAI_KEY'))

    @app_commands.command(name="chat", description="Chat with an AI (TogetherAI or MistralAI)")
    @app_commands.choices(model=[
        app_commands.Choice(name="TogetherAI", value="together"),
        app_commands.Choice(name="MistralAI", value="mistral")
    ])
    async def chat(self, interaction: discord.Interaction, model: app_commands.Choice[str], message: str):
        await interaction.response.defer()

        try:
            if model.value == "together":
                response = self.together_client.chat(
                    messages=[{"role": "user", "content": message}],
                    model="mistral-7b-instruct"
                )
                ai_response = response['output']['content']

            else:  # mistral
                messages = [ChatMessage(role="user", content=message)]
                response = self.mistral_client.chat(
                    model="mistral-tiny",
                    messages=messages
                )
                ai_response = response.choices[0].message.content

            # Split response if it exceeds Discord's limit
            if len(ai_response) > 2000:
                chunks = [ai_response[i:i+2000] for i in range(0, len(ai_response), 2000)]
                for chunk in chunks:
                    await interaction.followup.send(chunk)
            else:
                await interaction.followup.send(ai_response)

        except Exception as e:
            await interaction.followup.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(AIChat(bot))