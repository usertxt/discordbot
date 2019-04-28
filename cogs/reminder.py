import discord
from discord.ext import commands
import asyncio


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def remindme(self, ctx, msg, time):
        if 's' in time:
            time = int(time.replace('s', ''))
            await ctx.send(f'Reminding you in {time} seconds to {msg}')
            await ctx.message.add_reaction('\N{HAMMER AND WRENCH}')
            await asyncio.sleep(time)
            await discord.User.send(ctx.message.author, f'This is a reminder to {msg}')
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

        if 'm' in time:
            time = int(time.replace('m', '')) * 60
            await ctx.send(f'Reminding you in {time / 60} minutes to {msg}')
            await ctx.message.add_reaction('\N{HAMMER AND WRENCH}')
            await asyncio.sleep(time)
            await discord.User.send(ctx.message.author, f'This is a reminder to {msg}')
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

        if 'h' in time:
            time = int(time.replace('h', '')) * 3600
            await ctx.send(f'Reminding you in {time / 3600} hours to {msg}')
            await ctx.message.add_reaction('\N{HAMMER AND WRENCH}')
            await asyncio.sleep(time)
            await discord.User.send(ctx.message.author, f'This is a reminder to {msg}')
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction('\N{THUMBS UP SIGN}')


def setup(bot):
    bot.add_cog(Reminder(bot))