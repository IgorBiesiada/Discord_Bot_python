import nextcord
from nextcord.ext import commands
import nextcord.iterators

bot = commands.Bot()

SERVER_ID = "there you must paste your discord id sever"

@bot.event
async def ready():
    print("Bot status: online")

@bot.slash_command(description="you can write here what you want", guild_ids=[SERVER_ID])
async def help(interaction: nextcord.Interaction):
    await interaction.response.send_message("How can i help you")

bot.run("Here paste your bot token. Dont show this token to anyone")

