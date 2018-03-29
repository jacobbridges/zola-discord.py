import asyncio

import discord

from core.commands import all_commands
from core.logger import logger

# Create the discord client
client = discord.Client()


@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user.name} #{client.user.id}')
    setattr(client, 'zen', {})

    # Attach all server emojis to the client for easy reference
    client.zen['emoji_map'] = {}
    for emoji in client.get_all_emojis():
        client.zen['emoji_map'][emoji.name] = emoji


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    for command in all_commands:
        if await command(message, client) is True:
            return

try:
    token = open('./token').read()
    client.run(token)
except Exception as E:
    logger.error(E)
    logger.error('Could not load auth_token from token file!')
    logger.error('SHUTDOWN')
