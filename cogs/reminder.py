from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import asyncio
import logging
import json


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    guild_ids = json.load(open("config.json"))["DISCORD"]["GUILD_IDS"]

    async def remindme(self, ctx, duration, message, slash_check=False):
        logging.info(f'[RemindMe Prompted]: {ctx.author}: {duration} {message}')

        if 's' in duration:
            duration = int(duration.replace('s', ''))
            if slash_check:
                await ctx.send(f'Reminding you in {duration} seconds to {message}', hidden=True)
            else:
                await ctx.send(f'Reminding you in {duration} seconds to {message}')
            await asyncio.sleep(duration)
            await ctx.author.send(f'This is a reminder to {message}')
        elif 'm' in duration:
            duration = int(duration.replace('m', '')) * 60
            if slash_check:
                await ctx.send(f'Reminding you in {duration / 60} minutes to {message}', hidden=True)
            else:
                await ctx.send(f'Reminding you in {duration / 60} minutes to {message}')
            await asyncio.sleep(duration)
            await ctx.author.send(f'This is a reminder to {message}')
        elif 'h' in duration:
            duration = int(duration.replace('h', '')) * 3600
            if slash_check:
                await ctx.send(f'Reminding you in {duration / 3600} hours to {message}', hidden=True)
            else:
                await ctx.send(f'Reminding you in {duration / 3600} hours to {message}')
            await asyncio.sleep(duration)
            await ctx.author.send(f'This is a reminder to {message}')

    @cog_ext.cog_slash(name="remindme", description="Set a reminder", guild_ids=guild_ids)
    async def slash_remindme(self, ctx: SlashContext, duration, message):
        await ctx.defer(hidden=True)
        await self.remindme(ctx, duration, message, slash_check=True)

    @commands.command(name="remindme", pass_context=True, brief="Set a reminder", 
    description="Example: !remindme 10s \"This is an example\" will make the bot wait 10 seconds, then send you a direct message saying \"This is an example\"")
    async def command_remindme(self, ctx, duration, message):
        await self.remindme(ctx, duration, message)


def setup(bot):
    bot.add_cog(Reminder(bot))