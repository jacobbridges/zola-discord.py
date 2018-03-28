import discord
import pydash

from ..logger import logger
from ..constants import PARTY_HARDER_GIFS, SLAPPABLE_ITEMS, \
    SLAPPABLE_REACTIONS, SLAPPABLE_STRINGS
from ..decorators import parse_command_args


async def command_party(message, *args, **kwargs):
    """
    Return a random party harder gif.
    """
    client = command_party.client
    if message.content == '!party':
        logger.info('Run command !party')

        # Create an embed for the gif response
        gif_embed = discord.Embed()
        gif_embed.type = 'rich'
        gif_embed.set_image(url=pydash.sample(PARTY_HARDER_GIFS))

        await client.send_message(
            message.channel,
            embed=gif_embed
        )
        return True
    return False


async def command_slap(message, *args, **kwargs):
    """
    Return a random slap text.
    """
    client = command_slap.client
    if message.content.startswith('!slap'):
        template = pydash.sample(SLAPPABLE_STRINGS)
        reaction = pydash.sample(SLAPPABLE_REACTIONS)
        if reaction.startswith(':'):
            reaction = pydash.trim(reaction, ':')
            reaction = client.zen['emojis'].get(reaction, 'Umm..')
        item = pydash.sample(SLAPPABLE_ITEMS)
        slapper = getattr(message.author, 'nickname') or \
                  getattr(message.author, 'username', 'null')

        # Get the slappee
        slappee = pydash.chain(message.content)\
            .replace('!slap', '')\
            .trim()\
            .value()

        # If the slappee wasn't specified, the slapper gets slapped
        if not slappee:
            slappee = slapper
            slapper = 'Zola'

        await client.send_message(message.channel, template.format(
            slapper=slapper,
            slappee=slappee,
            item=item,
            reaction=reaction,
        ))
        return True
    return False
