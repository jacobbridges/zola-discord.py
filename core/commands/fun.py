from ..logger import logger


async def command_party(message, *args, **kwargs):
    client = command_party.client
    if message.content == '!party':
        logger.info('Run command !party')

        await client.send_message(
            message.channel,
            'https://media.giphy.com/media/NHFiGCmtY9lT2/giphy.gif'
        )
