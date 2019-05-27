from discord.ext import commands
import logging


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config["DISCORD"]
        self.admin_id = int(self.config["ADMIN_ID"])

    @commands.command()
    async def clearlog(self, ctx):
        if ctx.message.author.id == self.admin_id:
            with open('bot.log', 'w'):
                pass
            await ctx.send('Clearing log file')
            logging.info(f'[Admin]: Log file cleared by {ctx.message.author}[{ctx.message.author.id}]')
        else:
            await ctx.send('You are not authorized to clear the log file')
            logging.info(f'[Admin]: Attempted log file clear by {ctx.message.author}[{ctx.message.author.id}]')

    @commands.command()
    async def reload(self, ctx, module):
        if ctx.message.author.id == self.admin_id:
            try:
                self.bot.reload_extension(module)
                await ctx.send(f'Successfully reloaded extension: {module}')
                logging.info(f'[Admin]: Reloaded extension: {module}')
            except commands.ExtensionError as e:
                await ctx.send(f'{e.__class__.__name__}: {e}')
                logging.info(f'[Admin Error]: {e.__class__.__name__}: {e}')
            else:
                await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        else:
            await ctx.send('You are not authorized to reload an extension')
            logging.info(f'[Admin]: Attempted extension reload by {ctx.message.author}[{ctx.message.author.id}]')


def setup(bot):
    bot.add_cog(Admin(bot))
