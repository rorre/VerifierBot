from discord.ext import commands

class Setting:
    """Sets user role

    Commands:
        add     Adds game mode role
        remove  Removes game mode role"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, *arguments):
        """Adds game mode role

        Gamemode Cheatsheet:
        std : standard
        mna : mania
        ctb : catch
        tko : taiko

        You can add multiple roles at once, just separate them with a space

        Example:
            !add std ctb mna - This will add standard, catch, and mania roles to you."""
        standard = None
        catch = None
        mania = None
        taiko = None
        for role in ctx.guild.roles:
            if role.name == "Standard":
                standard = role
            if role.name == "Catch":
                catch = role
            if role.name == "Mania":
                mania = role
            if role.name == "Taiko":
                taiko = role
        options = {
            'std': standard,
            'mna': mania,
            'ctb': catch,
            'tko': taiko
        }
        added = []
        for mode in arguments:
            try:
                await ctx.message.author.add_roles(options[mode])
                added.append(options[mode].name)
            except KeyError:
                await ctx.send("Please input valid game mode! (Check the cheatsheet in !help add)")
                return
        await ctx.send("Done! Added " + ' '.join(added))

    @commands.command()
    async def remove(self, ctx, *arguments):
        """Removes game mode role

        Game mode Cheatsheet:
        std : standard
        mna : mania
        ctb : catch
        tko : taiko

        You can add multiple roles at once, just separate them with a space

        Example:
            !add std ctb mna - This will add standard, catch, and mania roles to you."""
        standard = None
        catch = None
        mania = None
        taiko = None
        for role in ctx.guild.roles:
            if role.name == "Standard":
                standard = role
            if role.name == "Catch":
                catch = role
            if role.name == "Mania":
                mania = role
            if role.name == "Taiko":
                taiko = role
        options = {
            'std': standard,
            'mna': mania,
            'ctb': catch,
            'tko': taiko
        }
        added = []
        for mode in arguments:
            try:
                await ctx.message.author.remove_roles(options[mode])
                added.append(options[mode].name)
            except KeyError:
                await ctx.send("Please input valid game mode! (Check the cheatsheet in !help add)")
                return
        await ctx.send("Done! Removed " + ' '.join(added))


def setup(bot):
    bot.add_cog(Setting(bot))
