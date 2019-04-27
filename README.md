# usertxt's Discord Bot
A Discord bot

Written in Python 3.7.2

## Installation

**Install required packages**

> Note: This app is written with the discord.py rewrite, some commands will not work on other versions. More information can be found here: https://discordpy.readthedocs.io/en/rewrite/migrating.html

```
 pip install -r requirements.txt
```


## Configure

Configure the app using **config.json**

Add your bot's token to:
```
"TOKEN": "YOUR_TOKEN"
```

Fiat is set to USD by default. Set your default fiat currency with:
```
"BASE_CURRENCY: "CURRENCY"
```
>Note: Use the lowercase three letter symbol for your BASE_CURRENCY currency or the API won't fetch the information properly.

## Cogs

### CryptoTicker
This extension uses CoinGecko's API to fetch cryptocurrency prices.

**Commands:**

In the Discord chat channel your bot has joined, use the following command to prompt the bot:
```
!price <ticker> [base_currency] 
```

**Examples:**

This command will return the price of Bitcoin vs the base currency you have chosen in your config:

```
!price btc
```
> Note: You are able to use the symbol or the full name of the currency. BTC or Bitcoin.

And this command will return the price of Bitcoin vs the Australian dollar:

```
!price btc aud
```

The basecurrency command allows you to use the bot to change your default base currency:

```
!basecurrency <currency>
```

**Example:**

```
!basecurrency aud
```

### TwitStream
TwitStream fetches user's tweets and relays them to your Discord channel.

**Commands:**

The following command will fetch a tweet from the user's timeline:

```
!twit <screen_name> [count]
```

>The optional count parameter will return the user's tweet based on order the tweet is in their timeline. None or 1 is the most recent tweet, and 2 would be the user's second most recent tweet, etc.