from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import discord
from twitter import *
from datetime import datetime
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

        self.t = Twitter(auth=OAuth(self.token_key, self.token_secret, self.consumer_key, self.consumer_secret))

    guild_ids = json.load(open("config.json"))["DISCORD"]["GUILD_IDS"]

    async def twit(self, ctx, screen_name, count=None):
        logging.info(f"[TwitStream Prompted]: {ctx.author}: twit {screen_name} {count}")

        if count is None:
            count = 1

        if count == "rand":
            count = random.randint(1, 99)

        if int(count) < 100:
            num = int(count) - 1
            data = self.t.statuses.user_timeline(screen_name=screen_name, count=count, tweet_mode="extended")
            twit_id = data[num]["id"]
            corrected_screen_name = data[num]["user"]["screen_name"]
            reply_check_id = data[num]["in_reply_to_status_id"]

            if "retweeted_status" in data[num]:
                rt_screen_name = data[num]["retweeted_status"]["user"]["screen_name"]
                twit_id = data[num]["retweeted_status"]["id"]
                await ctx.send(f"{corrected_screen_name} retweeted: https://twitter.com/{rt_screen_name}/status/{twit_id}")
                logging.info(f"[TwitStream Returned]: {corrected_screen_name} retweeted: https://twitter.com/{rt_screen_name}/status/{twit_id}")
            elif type(reply_check_id) is int:
                twit_profile_photo = data[num]["user"]["profile_image_url_https"]
                twit_received = data[num]["full_text"]
                twit_timestamp = data[num]["created_at"]
                twit_timestamp = datetime.strptime(twit_timestamp, "%a %b %d %H:%M:%S %z %Y").strftime("%m/%d/%Y")
                real_name = data[num]["user"]["name"]
                reply_data = self.t.statuses.show(id=reply_check_id)
                reply_screen_name = reply_data["user"]["screen_name"]
                reply_timestamp = reply_data["created_at"]
                reply_timestamp = datetime.strptime(reply_timestamp, "%a %b %d %H:%M:%S %z %Y").strftime("%m/%d/%Y")

                e = discord.Embed(color=0x1DA1F2)
                e.set_thumbnail(url="https://i.imgur.com/T3Txqdz.png")
                e.set_author(name=f"{real_name} ({corrected_screen_name})", icon_url=twit_profile_photo, url=f"https://twitter.com/{corrected_screen_name}")
                e.add_field(name="\u200b", value=twit_received, inline=False)
                e.add_field(name="\u200b", value=f"Twitter • {twit_timestamp}")
                e.add_field(name="\u200b", value="Replied to:", inline=False)
                e.add_field(name=reply_screen_name, value=reply_data["text"], inline=False)
                e.add_field(name="\u200b", value=f"Twitter • {reply_timestamp}")

                await ctx.send(embed=e)
                logging.info(f"[TwitStream Returned]: Embed reply for https://twitter.com/{corrected_screen_name}/status/{twit_id}")
                logging.info(f"[TwitStream Returned]: Includes embed reply for https://twitter.com/{reply_screen_name}/status/{reply_check_id}")
            else:
                await ctx.send(f"https://twitter.com/{corrected_screen_name}/status/{twit_id}")
                logging.info(f"[TwitStream Returned]: https://twitter.com/{corrected_screen_name}/status/{twit_id}")

            while data[num]["full_text"].endswith("..."):
                num -= 1
                twit_id = data[num]["id"]
                await ctx.send(f"https://twitter.com/{corrected_screen_name}/status/{twit_id}")
                logging.info(f"[TwitStream Returned]: https://twitter.com/{corrected_screen_name}/status/{twit_id}")

            if "https://t.co" in data[num]["full_text"] and data[num]["entities"].get("media") is None:
                url = re.search("(?P<url>https?://[^\s]+)", data[num]["full_text"]).group("url")
                await asyncio.sleep(3)
                await ctx.send(url)
        else:
            await ctx.send("[TwitStream Error]: Too many tweets requested")
            logging.info("[TwitStream Error]: Too many tweets requested")

    async def twitsearch(self, ctx, search_term, result_type=None):
        logging.info(f"[TwitStream Prompted]: {ctx.author} twitsearch {search_term} {result_type}")

        result_type_options = ["mixed", "recent", "popular"]

        if result_type is None:
            result_type = "popular"

        if result_type in result_type_options:
            num = 0
            data = self.t.search.tweets(q=search_term, lang="en", result_type=result_type, count=1)

            if data["statuses"] == []:
                logging.info(f"[TwitStream]: No results found for \"{search_term}\"")
                return await ctx.send(f"[TwitStream]: No results found for \"{search_term}\"")

            twit_id = data["statuses"][num]["id"]
            screen_name = data["statuses"][num]["user"]["screen_name"]

            if "retweeted_status" in data["statuses"][num].keys():
                retweet_id = data["statuses"][num]["retweeted_status"]
                twit_id = retweet_id["id"]
                screen_name = retweet_id["user"]["screen_name"]
                
            reply_check_id = data["statuses"][num]["in_reply_to_status_id"]

            if type(reply_check_id) is int:
                twit_profile_photo = data["statuses"][num]["user"]["profile_image_url_https"]
                twit_received = data["statuses"][num]["text"]
                twit_timestamp = data["statuses"][num]["created_at"]
                twit_timestamp = datetime.strptime(twit_timestamp, "%a %b %d %H:%M:%S %z %Y").strftime("%m/%d/%Y")
                real_name = data["statuses"][num]["user"]["name"]
                reply_data = self.t.statuses.show(id=reply_check_id)
                reply_screen_name = reply_data["user"]["screen_name"]
                reply_timestamp = reply_data["created_at"]
                reply_timestamp = datetime.strptime(reply_timestamp, "%a %b %d %H:%M:%S %z %Y").strftime("%m/%d/%Y")

                e = discord.Embed(color=0x1DA1F2)
                e.set_thumbnail(url="https://i.imgur.com/T3Txqdz.png")
                e.set_author(name=f"{real_name} ({screen_name})", icon_url=twit_profile_photo, url=f"https://twitter.com/{screen_name}")
                e.add_field(name="\u200b", value=twit_received, inline=False)
                e.add_field(name="\u200b", value=f"Twitter • {twit_timestamp}")
                e.add_field(name="\u200b", value="Replied to:", inline=False)
                e.add_field(name=reply_screen_name, value=reply_data["text"], inline=False)
                e.add_field(name="\u200b", value=f"Twitter • {reply_timestamp}")

                await ctx.send(embed=e)
                logging.info(f"[TwitStream Returned]: Embed reply for https://twitter.com/{screen_name}/status/{twit_id}")
                logging.info(f"[TwitStream Returned]: Includes embed reply for https://twitter.com/{reply_screen_name}/status/{reply_check_id}")
            else:
                await ctx.send(f"https://twitter.com/{screen_name}/status/{twit_id}")
                logging.info(f"[TwitStream Returned]: https://twitter.com/{screen_name}/status/{twit_id}")
        else:
            await ctx.send(f"result_type options are [mixed, recent, popular]")

    @cog_ext.cog_slash(name="twit", description="Get tweets by Twitter username", guild_ids=guild_ids)
    async def slash_twit(self, ctx: SlashContext, screen_name, count=None):
        await self.twit(ctx, screen_name, count)

    @commands.command(name="twit", pass_context=True, brief="Get tweets by Twitter username")
    async def command_twit(self, ctx, screen_name, count=None):
        await self.twit(ctx, screen_name, count)

    @cog_ext.cog_slash(name="twitsearch", description="Search tweets - result_type options are popular (default), mixed, or recent", guild_ids=guild_ids)
    async def slash_twitsearch(self, ctx: SlashContext, search_term, result_type=None):
        await self.twitsearch(ctx, search_term, result_type)

    @commands.command(name="twitsearch", pass_context=True, brief="Search tweets")
    async def command_twitsearch(self, ctx, search_term, result_type=None):
        await self.twitsearch(ctx, search_term, result_type)


def setup(bot):
    bot.add_cog(TwitStream(bot))
