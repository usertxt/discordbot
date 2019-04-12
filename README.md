# usertxt's Discord Bot
Simple Discord bot that uses CoinGecko's API to fetch cryptocurrency prices

## Installation

**Install required packages**

> Note: This app is written with the discord.py rewrite, some commands will not work on other versions. More information can be found here: https://discordpy.readthedocs.io/en/rewrite/migrating.html

**discord.py**

Linux/OS X:
```
 python3 -m pip install -U discord.py
```
Windows:
```
 py -3 -m pip install -U discord.py
```

## Configure

Configure the app using **config.ini**

Add your bot's token to:
```
token = 'YOUR_TOKEN'
```

Fiat is set to USD by default. Set your default fiat currency with:
```
default_fiat = 'CURRENCY'
```

## Commands
In the Discord chat channel your bot has joined, use the following command to prompt the bot:
```
!price <crypto> <fiat> 
```

**Examples:**

This command will return the price of Bitcoin vs the default currency you have chosen in your config:

```
!price bitcoin
```

And this command will return the price of Bitcoin vs the Australian dollar:

```
!price bitcoin aud
```

The setfiat command allows you to use the bot to change your default fiat currency:

```
!setfiat <fiat>
```

**Example:**

```
!setfiat aud
```
