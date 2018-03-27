import logging

import discord
import asyncio

# Configure some logging
logger = logging.getLogger('zola')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('zola.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

# Create the discord client
client = discord.Client()

@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user.name} #{client.user.id}')

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

try:
    token = open('./token').read()
    client.run(token)
except Exception as E:
    logger.error(E)
    logger.error('Could not load auth_token from token file!')
    logger.error('SHUTDOWN')