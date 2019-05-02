from discord.ext import commands
import requests
import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = sql.create_engine('sqlite:///portfolio.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'
    id = sql.Column(sql.Integer, sql.Sequence('user_id_seq'), primary_key=True)
    name = sql.Column(sql.String(50))
    discord_id = sql.Column(sql.String(50))
    symbol = sql.Column(sql.String(50))
    quantity = sql.Column(sql.String(50))
    price = sql.Column(sql.String(50))

    def __repr__(self):
        return "<User(id='%s', name='%s', discord_id='%s', symbol='%s', quantity='%s'," \
               " price='%s')>" % (self.id, self.name, self.discord_id, self.symbol, self.quantity, self.price)


Base.metadata.create_all(engine)

# test = User(name='test', discord_id='5555', symbol='555', quantity='555', price='555')
#
# session.add(test)
# session.commit()
# session.close()


class Portfolio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_ticker = self.bot.config["CRYPTOTICKER"]
        self.supported_currencies = requests.get(self.config_ticker["SUPPORTED_CURRENCIES"]).json()
        self.supported_coins = requests.get('https://api.coingecko.com/api/v3/coins/list').json()

    @commands.command(pass_context=True)
    async def p(self, ctx, action, ticker=None, quantity=None, price=None):
        if action == 'positions':
            disc_id = str(ctx.message.author.id)
            exists = session.query(
                session.query(User).filter_by(discord_id=disc_id).exists()
            ).scalar()
            if exists is True:
                if ticker is None:
                    for discord_id, symbol, quantity, price, in session.query(User.discord_id, User.symbol,
                                                                              User.quantity, User.price).\
                                                                              filter(User.discord_id == disc_id):
                        await ctx.send(f'{symbol.upper()} {quantity} {price}')
                else:
                    for discord_id, symbol, quantity, price, in session.query(User.discord_id, User.symbol,
                                                                              User.quantity, User.price).\
                                                                              filter(User.discord_id == disc_id).\
                                                                              filter(User.symbol == ticker):
                        await ctx.send(f'{symbol.upper()} + {quantity} + {price}')
            else:
                await ctx.send('You have no positions')

        elif action == 'add':
            if ticker in str(self.supported_coins):
                user = User(name=ctx.message.author.name, discord_id=ctx.message.author.id, symbol=ticker.lower(),
                            quantity=quantity, price=price)
                print(f'adding {user} to database')
                session.add(user)
                session.commit()
                session.close()
                await ctx.send(f'Adding {ticker} {quantity} {price} for {ctx.message.author.name}')
            else:
                await ctx.send(f'Error: {ticker} is not a supported currency')

        elif action == 'remove':
            disc_id = str(ctx.message.author.id)
            session.query(User). \
                filter(User.name == str(ctx.message.author.name)). \
                filter(User.discord_id == disc_id). \
                filter(User.symbol == ticker). \
                filter(User.quantity == quantity). \
                filter(User.price == price). \
                delete()
            session.commit()
            session.close()
            await ctx.send(f'Removing {ticker} {quantity} {price} for {ctx.message.author.name}')

    @commands.command(pass_context=True)
    async def positions(self, ctx):
        disc_id = str(ctx.message.author.id)
        exists = session.query(
            session.query(User).filter_by(discord_id=disc_id).exists()
        ).scalar()
        if exists is True:
            for discord_id, symbol, quantity, price, in session.query(User.discord_id, User.symbol, User.quantity,
                                                                      User.price).filter(User.discord_id == disc_id):
                await ctx.send(f'{symbol} + {quantity} + {price}')
        else:
            await ctx.send('You have no positions')

    @commands.command(pass_context=True)
    async def positionadd(self, ctx, ticker, quantity, price):
        if ticker in str(self.supported_coins):
            user = User(name=ctx.message.author.name, discord_id=ctx.message.author.id, symbol=ticker,
                        quantity=quantity, price=price)
            print(f'adding {user} to database')
            session.add(user)
            session.commit()
            session.close()
            await ctx.send(f'Adding {ticker} {quantity} {price} for {ctx.message.author.name}')
        else:
            await ctx.send(f'Error: {ticker} is not a supported currency')

    @commands.command(pass_context=True)
    async def positionremove(self, ctx, ticker, quantity, price):
        disc_id = str(ctx.message.author.id)
        session.query(User).\
            filter(User.name == str(ctx.message.author.name)).\
            filter(User.discord_id == disc_id).\
            filter(User.symbol == ticker).\
            filter(User.quantity == quantity).\
            filter(User.price == price).\
            delete()
        session.commit()
        session.close()
        await ctx.send(f'Removing {ticker} {quantity} {price} for {ctx.message.author.name}')


def setup(bot):
    bot.add_cog(Portfolio(bot))
