import logging
import random
from datetime import datetime

import pydash
from discord import Embed
from discord.ext.commands import Bot, command, Context, group, UserConverter
from google.cloud import firestore

from core.cogs.toolbox import StatefulCog
from core.constants import ZEN_SERVER, ZOLA_UTILS_ROLE
from core.decorators import with_role
from core.models import Stopwatch, WordCounter

logger = logging.getLogger(__name__)


class Utility(StatefulCog):

    def __init__(self, bot: Bot):
        super(Utility, self).__init__()
        self.bot = bot
        self.fire = firestore.Client()

    @command(name='test', hidden=True, pass_context=True)
    async def test_command(self, ctx: Context):
        """
        Count how many messages you have in this channel.
        """

        placeholder = await self.bot.say('Fetching messages..')
        messages = [m async for m in self.bot.logs_from(ctx.message.channel)]
        my_messages = pydash.filter_(
            messages,
            lambda m: m.author == ctx.message.author
        )

        return await self.bot.edit_message(
            placeholder,
            f'You have {len(my_messages)} messages.'
        )

    @command(name='syncdb', hidden=True, pass_context=True)
    @with_role(ZOLA_UTILS_ROLE)
    async def sync_database(self, ctx: Context):
        """
        Create tables for all models.
        """

        db = await self.get_db()
        await self.run_db_transactions(db, transactions=[
            lambda: db.drop_tables([Stopwatch, WordCounter]),
            lambda: db.create_tables([Stopwatch, WordCounter]),
        ])
        return await self.bot.say(f'Database synced successfully.')

    @command(name='clear', pass_context=True)
    @with_role(ZOLA_UTILS_ROLE)
    async def clear_command(self, ctx: Context, limit=1000):
        """
        Clear messages from a channel.
        """

        try:
            limit = int(limit)
        except ValueError:
            await ctx.invoke(self.bot.get_command('help'), 'clear')
            return

        if limit is 1:
            await self.bot.delete_message(ctx.message)
            return

        messages = [m async for m in
                    self.bot.logs_from(ctx.message.channel, limit=limit)]
        [await self.bot.delete_message(m) for m in messages]

    @group(name='id', pass_context=True)
    @with_role(ZOLA_UTILS_ROLE)
    async def id_command(self, ctx: Context):
        """
        Get the Discord ID by name.
        """

        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command('help'), 'id')

    @id_command.command(name='role', ignore_extra=True, pass_context=True)
    @with_role(ZOLA_UTILS_ROLE)
    async def id_role_command(self, ctx: Context, *role_name):
        """
        Get the Discord ID of a role.
        """

        role_name = ' '.join(role_name)
        for role in self.bot.get_server(ZEN_SERVER).roles:
            if role_name == role.name:
                return await self.bot.say(role.id)

        return await self.bot.say(f'No role found "{role_name}"')

    @command(name='stopwatch', aliases=['sw'], pass_context=True)
    async def stopwatch_command(self, ctx):
        """
        Starts/Stop a stopwatch.
        """

        author = ctx.message.author
        stopwatch = await self.thread_it(lambda: Stopwatch.get_or_none(Stopwatch.created_by == author.id))

        if not stopwatch:
            await self.thread_it(lambda: Stopwatch.create(created_on=datetime.now(), created_by=author.id))
            await self.bot.say(author.mention + ' - Stopwatch started!')
        else:
            stopwatch.stopped_on = datetime.now()
            await self.thread_it(lambda: stopwatch.save())
            await self.bot.say(author.mention + ' - Stopwatch stopped! Time: **' + stopwatch.result + '**')
            await self.thread_it(lambda: stopwatch.delete_instance())

    @command(name='lmgtfy')
    async def lmgtfy(self, *, search_terms: str):
        """
        Let me Google that for you.
        """
        search_terms = search_terms\
            .replace('@everyone', '@\u200beveryone')\
            .replace('@here', '@\u200bhere')\
            .replace(' ', '+')
        await self.bot.say('https://lmgtfy.com/?q={}'.format(search_terms))
        
    @command(name='wallpaper', aliases=['wallpapers', 'wp'])
    async def wallpaper(self, *, tag: str):
        """
        Explore wallpapers from the nivix hoard.
        """
        if tag:
            tag = tag.lower().strip()
        else:
            tag = 'random'

        if tag == 'nsfw':
            wp = await self.thread_it(lambda: list(
                self.fire.collection('hoard/photos/wallpapers')
                    .where('nsfw', '==', True)
                    .get()))
        elif tag == 'random':
            wp = await self.thread_it(lambda: list(
                self.fire.collection('hoard/photos/wallpapers').get()))
        else:
            wp = await self.thread_it(lambda: list(
                self.fire.collection('hoard/photos/wallpapers')
                    .where('tags', 'array_contains', tag)
                    .where('nsfw', '==', False)
                    .get()))

        if not wp:
            await self.bot.say('No wallpaper found with that tag.')
            return
        else:
            wp = random.choice(wp)

        image_url = 'https://storage.googleapis.com/space.jacobbridges.pw/' + wp.get('storage_path')
        embed = Embed()
        embed.set_image(url=image_url)
        embed.add_field(
            name='Tags',
            value=', '.join(wp.get('tags')),
        )
        embed.add_field(
            name='Image URL',
            value='https://storage.googleapis.com/space.jacobbridges.pw/' + wp.get('storage_path'),
        )
        await self.bot.say(embed=embed)
        
    @command('wp_remove_nsfw_tag', aliases=['rmnsfw'])
    @with_role(ZOLA_UTILS_ROLE)
    async def wp_remove_nsfw_tag(self, *, wpid):
        """
        Remove "nsfw" tag from wallpaper.
        """
        wp = self.fire.collection('hoard/photos/wallpapers').document(wpid)
        s = wp.get()
        tags = s.get('tags')
        if 'nsfw' not in tags: return
        tags.remove('nsfw')
        wp.update({'nsfw': False, 'tags': tags})
        await self.bot.say('NSFW tag removed.')

    @command('showme', aliases=['sm'], pass_context=True)
    async def showme(self, ctx: Context, user, word=None):
        """
        Show how many times a user has said a certain word.
        """
        print(user, word)
        user = UserConverter().convert(ctx, user)
        print(dir(user))

        if word is None:
            top_5_words = await self.thread_it(lambda: WordCounter.select()
                .where(WordCounter.user_id==user.id)
                .order_by(WordCounter.count.desc())
                .limit(5))
            response = '**Top 5 words for {}**'.format(user)
            for record in top_5_words:
                response += '\n{} - {}'.format(record.word, record.count)
            await self.bot.say(response)
        else:
            record = await self.thread_it(lambda: WordCounter.select()
                .where(WordCounter.user_id==user.id, word=word.lower())
                .order_by(WordCounter.count.desc())
                .get_or_none())
            if record:
                await self.bot.say('{} has said "{}" {} times.'.format(user.display_name, record.word, record.count))
            else:
                await self.bot.say('{} has never said the word "{}"'.format(user.display_name, word))



def setup(bot):
    bot.add_cog(Utility(bot))
    logger.info("Cog loaded: Utility")
