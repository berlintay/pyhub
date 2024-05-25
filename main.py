import discord
from discord.ext import commands
import asyncio
import configparser
import logging
import requests
from google_images_search import GoogleImagesSearch
from googleapiclient.discovery import build
from googleapiclient import errors
# Logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Discord config
TOKEN = config['DISCORD']['TOKEN']
ROLE_ID = int(config['DISCORD']['ROLE_ID'])
LOG_CHANNEL_ID = int(config['DISCORD']['LOG_CHANNEL_ID'])
WELCOME_CHANNEL_ID = int(config['DISCORD']['WELCOME_CHANNEL_ID'])
ROLE_DURATION_SECONDS = 604800

# Google Images Search config
GCS_DEVELOPER_KEY = config['GOOGLE']['GCS_DEVELOPER_KEY']
GCS_CX = config['GOOGLE']['GCS_CX']
YOUTUBE_API_KEY = config['GOOGLE']['YOUTUBE_API_KEY']
GEMINI_API_KEY = config['GOOGLE']['GEMINI_API_KEY']
# Discord bot setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# New member join event


@bot.event
async def on_member_join(member):
    try:
        logging.info(f"New member joined: {member.name} (ID: {member.id})")

        role = discord.utils.get(member.guild.roles, id=ROLE_ID)
        if role is None:
            raise ValueError(f"Role with ID {ROLE_ID} not found.")

        logging.info(f"Assigning role '{role.name}' to {member.name}")
        await member.add_roles(role)

        welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
        if welcome_channel:
            logging.info(f"Sending welcome message to #{welcome_channel.name}")
            await welcome_channel.send(
                f"aha ! <:rizzhotsexy:1195895549199663275> , {
                    member.mention} Looks like you been given the <@&{ROLE_ID}> Role, for 7 days !"
            )
        else:
            logging.error(
                f"Welcome channel (ID: {WELCOME_CHANNEL_ID}) not found.")

        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            logging.info(f"Sending log message to #{log_channel.name}")
            await log_channel.send(
                f"User {member.mention} (ID: {
                                         member.id}) has been assigned the \"New Victim\" role for 7 days."
            )
        else:
            logging.error(f"Log channel (ID: {LOG_CHANNEL_ID}) not found.")

        logging.info(f"Waiting for {ROLE_DURATION_SECONDS} seconds...")
        await asyncio.sleep(ROLE_DURATION_SECONDS)

        logging.info(f"Removing role '{role.name}' from {member.name}")
        await member.remove_roles(role)

    except discord.Forbidden as e:
        logging.error(f"Forbidden error: {e} (Missing permissions?)")
    except ValueError as ve:
        logging.error(ve)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


@bot.command(name='search')
async def search_web(ctx, *, query):
    try:
        # Perform the search
        search_params = {
            'q': query,
            'cx': GCS_CX,  # Use your Custom Search Engine ID
            'key': GCS_DEVELOPER_KEY,
            'num': 1,  # Get top 3 results
        }
        response = requests.get("https://www.googleapis.com/customsearch/v1", params=search_params)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()

        # Check if results were found
        if 'items' not in data:
            raise ValueError("No results found for your query.")

        # Format and send results
        for item in data['items']:
            await ctx.send(f"**{item['title']}**\n{item['link']}\n{item['snippet']}\n")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during web search: {e}")
        await ctx.send("An error occurred while searching the web.")
    except ValueError as ve:
        logging.error(f"Error during web search: {ve}")
        await ctx.send(str(ve))
    except Exception as e:
        logging.error(f"Error during web search: {e}")
        await ctx.send("An error occurred while searching the web.")

@bot.command(name='video')
async def search_video(ctx, *, query):
    try:
        # Search for videos
        request = youtube.search().list(
            part="snippet",
            maxResults=1, 
            q=query,
            type='video'
        )
        response = request.execute()

        # Check if results were found
        if not response['items']:
            raise ValueError("No videos found for your query.")

        # Extract and send video URL
        video_id = response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        await ctx.send(video_url)

    except ValueError as ve:
        logging.error(f"Error during video search: {ve}")
        await ctx.send(str(ve))
    except Exception as e:
        logging.error(f"Error during video search: {e}")
        await ctx.send("An error occurred while searching for videos.")



class EmbedModal(discord.ui.Modal, title='Create Embed'):
    title = discord.ui.TextInput(label='Embed Title', style=discord.TextStyle.short, required=True)
    description = discord.ui.TextInput(label='Description', style=discord.TextStyle.paragraph, required=True)
    color = discord.ui.TextInput(label='Color (hex or name)', style=discord.TextStyle.short, required=False)
    thumbnail = discord.ui.TextInput(label='Thumbnail URL', style=discord.TextStyle.short, required=False)
    image = discord.ui.TextInput(label='Image URL', style=discord.TextStyle.short, required=False)
    author_name = discord.ui.TextInput(label='Author Name', style=discord.TextStyle.short, required=False)
    author_icon = discord.ui.TextInput(label='Author Icon URL', style=discord.TextStyle.short, required=False)
    footer_text = discord.ui.TextInput(label='Footer Text', style=discord.TextStyle.short, required=False)
    footer_icon = discord.ui.TextInput(label='Footer Icon URL', style=discord.TextStyle.short, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.title.value, description=self.description.value)
        if self.color.value:
            try:
                embed.color = discord.Color.from_str(self.color.value)
            except ValueError:
                pass  # Use default color
        if self.thumbnail.value:
            embed.set_thumbnail(url=self.thumbnail.value)
        if self.image.value:
            embed.set_image(url=self.image.value)
        if self.author_name.value or self.author_icon.value:
            embed.set_author(name=self.author_name.value, icon_url=self.author_icon.value)
        if self.footer_text.value or self.footer_icon.value:
            embed.set_footer(text=self.footer_text.value, icon_url=self.footer_icon.value)

        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.slash_command(description="Create a custom embed")
async def create_embed(ctx):
    """Slash command to trigger the embed creation modal."""
    if not ctx.author.guild_permissions.manage_messages:  # Permissions check
        await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        return
    await ctx.send_modal(EmbedModal())


bot.run(TOKEN)

