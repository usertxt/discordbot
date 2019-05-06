from discord.ext import commands
import requests
import discord
import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from statistics import mean
from .cryptoticker import CryptoTicker
from pprint import pprint

engine = sql.create_engine('sqlite:///portfolio.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'
    id = sql.Column(sql.Integer, sql.Sequence('user_id_seq'), primary_key=True)
    name = sql.Column(sql.String(50))
    discord_id = sql.Column(sql.String(50))
    coin = sql.Column(sql.String(50))
    symbol = sql.Column(sql.String(50))
    quantity = sql.Column(sql.String(50))
    price = sql.Column(sql.String(50))

    def __repr__(self):
        return "<User(id='%s', name='%s', discord_id='%s', coin='%s', symbol='%s', quantity='%s'," \
               " price='%s')>" % (self.id, self.name, self.discord_id, self.coin, self.symbol, self.quantity, self.price)


Base.metadata.create_all(engine)


class Portfolio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_ticker = self.bot.config["CRYPTOTICKER"]
        self.url = self.config_ticker["URL"]
        self.base_currency = self.config_ticker["BASE_CURRENCY"]
        self.coin_list = requests.get(self.config_ticker["COIN_LIST"]).json()
        self.supported_currencies = requests.get(self.config_ticker["SUPPORTED_CURRENCIES"]).json()

    @commands.command(pass_context=True)
    async def p(self, ctx, action, ticker=None, quantity=None, price=None):
        if action == 'positions':
            disc_id = str(ctx.message.author.id)
            # exists = session.query(
            #     session.query(User).filter_by(discord_id=disc_id).exists()
            # ).scalar()

            for coin in self.coin_list:
                if ticker == coin['symbol']:
                    ticker = coin['id']

            id_query = session.query(User.discord_id, User.coin, User.symbol, User.quantity, User.price). \
                filter(User.discord_id == disc_id)
            coin_query = session.query(User.discord_id, User.coin, User.symbol, User.quantity, User.price). \
                filter(User.discord_id == disc_id). \
                filter(User.coin == ticker)
            result1 = [r.discord_id for r in id_query]
            result2 = [r.coin for r in coin_query]
            response = '```fix\n'
            try:
                if disc_id in result1:
                    response += f'{ticker.upper()} positions for {ctx.message.author.name}\n'
                    response += 'SYM QTY PRICE\n'
                    if ticker is None:
                        for discord_id, coin, symbol, quantity, price in id_query:
                            response += f'{symbol.upper()} {quantity}   {price}\n'
                    elif ticker in result2:
                        for discord_id, coin, symbol, quantity, price in coin_query:
                            response += f'{symbol.upper()} {quantity}   {price}\n'
                else:
                    response += 'You have no positions'
                    response += '```'
            finally:
                if ticker is None:
                    avg = [int(n.price) for n in id_query]
                    avg = mean(avg)
                    response += f'Average cost: {avg:,.2f}'
                    response += '```'

                elif ticker in result2:
                    url_response = requests.get(self.url + ticker + '&vs_currency=usd')
                    fetched = url_response.json()
                    current_price = fetched[0]['current_price']
                    current_worth = [float(n.quantity) * current_price for n in coin_query]
                    current_worth = sum(current_worth)
                    total_price = [float(n.price) for n in coin_query]
                    total_price = sum(total_price)
                    if current_worth < total_price:
                        loss = total_price - current_worth
                        response += f'Total cost: {total_price:,.2f} Total worth: {current_worth:,.2f} Loss: {loss:,.2f}'
                    elif current_worth > total_price:
                        profit = current_worth - total_price
                        response += f'Total cost: {total_price:,.2f} Total worth: {current_worth:,.2f} Profit: {profit:,.2f}'
                    response += '```'
            await ctx.send(response)

        elif action == 'add':
            if ticker is None:
                await ctx.send('Please supply a currency')
            elif ticker in str(self.coin_list):
                for coin in self.coin_list:
                    if ticker == coin['symbol']:
                        ticker = coin['id']
                        user = User(name=ctx.message.author.name, discord_id=ctx.message.author.id, coin=coin['id'],
                                    symbol=coin['symbol'],
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
            if ticker == 'all':
                session.query(User).filter(User.discord_id == disc_id).delete()
                session.commit()
            for coin in self.coin_list:
                if ticker == coin['symbol']:
                    ticker = coin['id']
                    session.query(User). \
                        filter(User.name == str(ctx.message.author.name)). \
                        filter(User.discord_id == disc_id). \
                        filter(User.coin == coin['id']). \
                        filter(User.symbol == coin['symbol']). \
                        filter(User.quantity == quantity). \
                        filter(User.price == price). \
                        delete()
                    session.commit()
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
        if ticker in str(self.coin_list):
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
