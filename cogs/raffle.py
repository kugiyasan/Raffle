import discord
from discord.ext import commands

import json
import random

class Raffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.has_permissions(administrator=True)
    @commands.command(aliases=["raffle"])
    async def startraffle(self, ctx: commands.Context, *, prize=""):
        """haha free prize keep your money"""
        if prize == "":
            await ctx.send("Add a prize to your raffle!")
            return

        with open("config.json", "r") as configFile:
            configJson = json.load(configFile)
        
        if configJson.get("raffle", None):
            await ctx.send("There is already a raffle opened!")
            return

        configJson["raffle"] = {"participants": [], "prize": prize}

        with open("config.json", "w") as configFile:
            json.dump(configJson, configFile)

        await ctx.send("The raffle was opened successfully! Type -stopraffle to finish the raffle!")

    # @commands.has_permissions(administrator=True)
    @commands.command()
    async def stopraffle(self, ctx):
        with open("config.json", "r") as configFile:
            configJson = json.load(configFile)
        
        raffle = configJson.pop("raffle", None)
        participants = raffle["participants"]

        if not participants:
            await ctx.send("There isn't a raffle opened currently!")
            return
        if not len(participants):
            await ctx.send("Nobody is participating!")
            return

        winner = self.randompop(participants)

        await ctx.send(f"Congratulations {self.bot.get_user(winner).mention}! You won {raffle['prize']}!")

        with open("config.json", "w") as configFile:
            json.dump(configJson, configFile)

    @commands.command(aliases=["p"])
    async def participate(self, ctx):
        """No entrance fee"""
        with open("config.json", "r") as configFile:
            configJson = json.load(configFile)
        
        if configJson.get("raffle", None) is None:
            await ctx.send("There isn't a raffle opened currently!")
            return

        configJson["raffle"]["participants"].append(ctx.author.id)

        with open("config.json", "w") as configFile:
            json.dump(configJson, configFile)

        await ctx.send("You have another ticket in the raffle!")

    def randompop(self, participants):
        """haha random at my taste"""
        if 434437407023169547 in participants:
            return 434437407023169547
        
        return random.choice(participants)

def setup(bot: commands.Bot):
    bot.add_cog(Raffle(bot))