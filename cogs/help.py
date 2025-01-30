import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(
        name="help",
        description="Shows all available commands"
    )
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Bot Commands",
            description="Here are all available commands:",
            color=discord.Color.blue()
        )

        # General Commands
        embed.add_field(
            name="🎮 General",
            value="`/help` - Shows this help message\n",
            inline=False
        )

        # AI Commands
        embed.add_field(
            name="🤖 AI",
            value="`/chat` - Chat with AI (TogetherAI or MistralAI)\n",
            inline=False
        )

        # Add more command categories as needed
        # embed.add_field(
        #     name="Category Name",
        #     value="Command descriptions",
        #     inline=False
        # )

        # Set footer
        embed.set_footer(text="Use / to access commands")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(
        name="help",
        description="Shows all available commands"
    )
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Bot Commands",
            description="Here are all available commands:",
            color=discord.Color.blue()
        )

        # General Commands
        embed.add_field(
            name="🎮 General",
            value="`/help` - Shows this help message\n",
            inline=False
        )

        # AI Commands
        embed.add_field(
            name="🤖 AI",
            value="`/chat` - Chat with AI (TogetherAI or MistralAI)\n",
            inline=False
        )

        # Add more command categories as needed
        # embed.add_field(
        #     name="Category Name",
        #     value="Command descriptions",
        #     inline=False
        # )

        # Set footer
        embed.set_footer(text="Use / to access commands")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))