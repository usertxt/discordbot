import discord
from discord.ext import commands
import asyncio
import logging


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def remindme(self, ctx, time):
        output = ctx.message.content.split()
        message = ''
        for word in output[2:]:
            message += word
            message += ' '

        logging.info(f'[RemindMe Prompted]: {ctx.message.author}: {time} {message}')

        if 's' in time:
            time = int(time.replace('s', ''))
            await ctx.send(f'Reminding you in {time} seconds to {message}')
            await ctx.message.add_reaction('\N{HAMMER AND WRENCH}')
            await asyncio.sleep(time)
            await discord.User.send(ctx.message.author, f'This is a reminder to {message}')
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

        if 'm' in time:
            time = int(time.replace('m', '')) * 60
            await ctx.send(f'Reminding you in {time / 60} minutes to {message}')
            await ctx.message.add_reaction('\N{HAMMER AND WRENCH}')
            await asyncio.sleep(time)
            await discord.User.send(ctx.message.author, f'This is a reminder to {message}')
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

        if 'h' in time:
            time = int(time.replace('h', '')) * 3600
            await ctx.send(f'Reminding you in {time / 3600} hours to {message}')
            await ctx.message.add_reaction('\N{HAMMER AND WRENCH}')
            await asyncio.sleep(time)
            await discord.User.send(ctx.message.author, f'This is a reminder to {message}')
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction('\N{THUMBS UP SIGN}')


def setup(bot):
    bot.add_cog(Reminder(bot))