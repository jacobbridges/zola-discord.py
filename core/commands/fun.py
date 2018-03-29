import discord
import pydash

from ..constants import PARTY_HARDER_GIFS, SLAPPABLE_ITEMS, \
    SLAPPABLE_REACTIONS, SLAPPABLE_STRINGS
from ..logger import logger


async def command_party(message, client, *args, **kwargs):
    """
    Return a random party harder gif.
    """
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


async def command_slap(message, client, *args, **kwargs):
    """
    Return a random slap text.
    """
    if message.content.startswith('!slap'):
        logger.info('Running !slap command')
        logger.debug('{}, {}'.format(message.content, message.author.display_name))

        template = pydash.sample(SLAPPABLE_STRINGS)
        reaction = pydash.sample(SLAPPABLE_REACTIONS)
        if reaction.startswith(':'):
            reaction = pydash.trim(reaction, ':')
            reaction = client.zen['emoji_map'].get(reaction, 'Umm..')
        item = pydash.sample(SLAPPABLE_ITEMS)
        slapper = getattr(message.author, 'display_name', None) or \
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


async def command_color(message, client, *args, **kwargs):
    return True
