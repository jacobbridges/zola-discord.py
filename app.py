import json

from aiohttp import AsyncResolver, ClientSession, TCPConnector
from discord import Game
from discord.ext.commands import when_mentioned_or

from core.zola import Zola

token = open('./token').readline().strip()
config = json.load(open('./config.json'))
zola = Zola(
    command_prefix=when_mentioned_or('!', '>>> '),
    activity=Game(name='List of commands: !help'),
    config=config
)

# Global aiohttp session for all cogs - uses asyncio for DNS resolution
# instead of threads, so we don't *spam threads*
zola.http_session = ClientSession(connector=TCPConnector(resolver=AsyncResolver()))

# Load extensions
zola.load_extension('core.cogs.logging')
zola.load_extension('core.cogs.events')
zola.load_extension('core.cogs.utility')
zola.load_extension('core.cogs.fun')
zola.load_extension('core.cogs.moderation')
zola.load_extension('core.cogs.youtube_dl')

zola.run(token)
zola.http_session.close()  # Close the aiohttp session when the bot finishes running
