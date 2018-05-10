import peewee

from core.cogs.toolbox.threaded_cog import ThreadedCog


class StatefulCog(ThreadedCog):
    """
    Cog with database helpers.
    """

    async def get_db(self) -> peewee.SqliteDatabase:
        """
        Return the SQLite database reference.
        """

        return await self.thread_it(lambda: peewee.SqliteDatabase('zola.db'))

    async def run_db_transactions(self, db, transactions):
        """
        Run a list of database transactions wrapped in a connection.
        """

        await self.thread_it(lambda: db.connect())
        for transaction in transactions:
            await self.thread_it(transaction)
        await self.thread_it(lambda: db.close())
