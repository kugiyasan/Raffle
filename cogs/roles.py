import discord
from discord.ext import commands

import json


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def role(self, ctx: commands.Context):
        """Add or remove some role from your profile!"""
        with open("config.json", "r") as configFile:
            roles = json.load(configFile)["roles"]


        roles = [ctx.guild.get_role(role) for role in roles]
        text = ("Choose the role you want to toggle by typing the name!\n"
                + "\n".join(role.name for role in roles))

        await ctx.send(text)

        def check(m):
            return (m.author == ctx.author
                    and m.channel == ctx.channel)

        answer = await self.bot.wait_for("message", check=check, timeout=60)

        for role in roles:
            if answer.content == role.name:
                if role not in ctx.author.roles:
                    await ctx.author.add_roles(role, reason=f"{self.bot.user.name} -role")
                    await ctx.send(f"{role.name} was added to your roles!")
                else:
                    await ctx.author.remove_roles(role, reason=f"{self.bot.user.name} -role")
                    await ctx.send(f"{role.name} was removed from your roles!")

                break

def setup(bot: commands.Bot):
    bot.add_cog(Roles(bot))
