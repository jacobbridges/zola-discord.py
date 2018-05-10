import asyncio
from concurrent.futures import ThreadPoolExecutor


class ThreadedCog(object):
    """
    Cog with helpers to await synchronous code via a thread pool.
    """
    max_workers = 5

    def __init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=5)

    async def thread_it(self, func, *args):
        """
        Wrap a synchronous function in an awaitable future.
        """

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.thread_pool, func, *args)
