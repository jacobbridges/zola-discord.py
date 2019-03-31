import os
import logging
from datetime import datetime

import pydash
from discord.ext.commands import Bot, command, Context, group

from pytube import YouTube as PyTube

from core.cogs.toolbox import StatefulCog
from core.constants import ZEN_SERVER, ZOLA_UTILS_ROLE
from core.decorators import with_role
from core.models import Stopwatch
from core.shortcuts import get_raw_arg


logger = logging.getLogger(__name__)


def download(video_url, path):
    video_stream = PyTube(video_url).streams \
        .filter(progressive=True, file_extension='mp4') \
        .order_by('resolution') \
        .desc() \
        .first()
    filename = video_stream.default_filename\
        .replace(' ', '_')\
        .replace('.mp4', '')
    video_stream.download(filename=filename, output_path=path)
    return filename + '.mp4'


class YoutubeDl(StatefulCog):

    def __init__(self, bot: Bot):
        super(YoutubeDl, self).__init__()
        self.bot = bot

    @command(name='youtube-dl', aliases=['ytdl'], pass_context=True,
             ignore_extra=True, no_pm=True)
    async def leave_command(self, ctx, url):
        """
        Download a youtube video.
        """
        author = ctx.message.author
        arg = get_raw_arg(ctx)

        # Download the video
        output_path = os.path.join(
            self.bot.config['youtube_dl']['output_path'],
            author.name.replace(' ', '_')
        )
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        await self.bot.say('Download started..')
        video_filename = await self.thread_it(download, arg, output_path)

        # Construct link to file
        video_link = '/'.join([self.bot.config['data_host'], author.name.replace(' ', '_'), video_filename])
        await self.bot.say(f'{author.mention}, your video is ready! {video_link}')


def setup(bot):
    bot.add_cog(YoutubeDl(bot))
    logger.info("Cog loaded: YoutubeDl")
