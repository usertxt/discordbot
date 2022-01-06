from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from discord_slash import cog_ext, SlashContext
from discord_slash.client import SlashCommand
from twitter import *
import asyncio
import logging
import random
import re
import json


class TwitStream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config["TWITSTREAM"]
        self.consumer_key = self.config["CONSUMER_KEY"]
        self.consumer_secret = self.config["CONSUMER_SECRET"]
        self.token_key = self.config["TOKEN_KEY"]
        self.token_secret = self.config["TOKEN_SECRET"]
        self.channel_id = self.config["CHANNEL_ID"]
        self.top_followed = self.config["TOP_FOLLOWED"]

        self.t = Twitter(auth=OAuth(self.token_key, self.token_secret, self.consumer_key, self.consumer_secret))

        self.tf_bg_task.start()

    guild_ids = json.load(open("config.json"))["DISCORD"]["GUILD_IDS"]

    async def twit(self, ctx, screen_name, count=None):
        if count is None:
            count = 1

        if count == "rand":
            count = random.randint(0, 50)

        if int(count) > 150:
            await ctx.send('[TwitStream Error]: Too many tweets requested')
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
        else:
            num = int(count) - 1
            data = self.t.statuses.user_timeline(screen_name=screen_name, count=count, tweet_mode="extended")
            twit_id = data[num]['id']

            await ctx.send(f'https://twitter.com/{screen_name}/status/{twit_id}')
            logging.info(f'[TwitStream Returned]: https://twitter.com/{screen_name}/status/{twit_id}')

            while data[num]['full_text'].endswith('...'):
                num -= 1
                twit_id = data[num]['id']
                await ctx.send(f'https://twitter.com/{screen_name}/status/{twit_id}')
                logging.info(f'[TwitStream Returned]: https://twitter.com/{screen_name}/status/{twit_id}')

            if "https://t.co" in data[num]['full_text'] and data[num]['entities'].get('media') is None:
                url = re.search("(?P<url>https?://[^\s]+)", data[num]['full_text']).group("url")
                await asyncio.sleep(3)
                await ctx.send(url)

    @cog_ext.cog_slash(name="twit", description="Get tweets by Twitter username", guild_ids=guild_ids)
    async def slash_twit(self, ctx: SlashContext, screen_name, count=None):
        await self.twit(ctx, screen_name, count)

    @commands.command(name="twit", pass_context=True)
    async def command_twit(self, ctx, screen_name, count=None):
        await self.twit(ctx, screen_name, count)

    @tasks.loop(seconds=43200)
    async def tf_bg_task(self):
        channel = self.bot.get_channel(self.channel_id)
        for x in self.top_followed:
            async with channel.typing():
                await channel.send(f"Latest tweet from {x}")
                await asyncio.sleep(1)
                await self.twit(channel, screen_name=x)
                await asyncio.sleep(3)

    @tf_bg_task.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(TwitStream(bot))
