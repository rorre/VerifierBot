import os, traceback, requests, re
from discord.ext import commands
from urllib.parse import urlparse

osutoken = os.environ['API_TOKEN']
token = os.environ['DISCORD_TOKEN']
initial_extensions = []


class VerifierBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!")
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception:
                print("Failed to load extension {extension}.")
                traceback.print_exc()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author.bot:
            return
        for role in message.guild.roles:
            if role.name == "Verified":
                verify = role
            if role.name == "Unverified":
                unverify = role
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                             message.content)
        if not urls:
            return
        for url in urls:
            parsed_url = urlparse(url)
            if parsed_url.netloc == "osu.ppy.sh" and (
                    parsed_url.path.startswith("/u/") or parsed_url.path.startswith("/users/")):
                user = parsed_url.path.split("/")[-1]
                try:
                    response = requests.get('https://osu.ppy.sh/api/get_user?k=%s&u=%s' % (osutoken, user)).json()
                except:
                    await message.channel.send("Huh, I got bad reply from osu!API, \
please ping moderator for manual verification.")
                if not response:
                    await message.channel.send('Can\'t seem to get data from osu! for username or user ID "{}",\n\
Did you link your name correctly? or are you restricted?'.format(user))
                    return
                await message.author.add_roles(verify)
                await message.author.remove_roles(unverify)
                await message.channel.send("Welcome, {}!".format(response[0]['username']))
                break


bot = VerifierBot()
bot.run(token)