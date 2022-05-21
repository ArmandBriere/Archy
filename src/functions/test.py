from discord.ext import commands


class ModerationCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="kick")
    async def my_kick_command(self, ctx):
        print(f"Nice try {ctx.author}, i'll kick you instead")
        await ctx.send(f"Nice try <@{ctx.author.id}>, i'll kick you instead")


def setup(client):
    client.add_cog(ModerationCommands(client))
