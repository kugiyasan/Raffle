import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ["DISCORD_TOKEN"]


bot = commands.Bot(command_prefix="-")

extensions = (
    "cogs.raffle",
    "cogs.roles"
)

@commands.is_owner()
@bot.command()
async def reload(ctx):
    for ext in extensions:
        bot.reload_extension(ext)

    await ctx.send("Reload successful!")

for ext in extensions:
    bot.load_extension(ext)

bot.run(token)
