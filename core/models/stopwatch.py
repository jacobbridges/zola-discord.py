import peewee as p

db = p.SqliteDatabase('zola.db')


class Stopwatch(p.Model):
    """
    Keep track of start and end timestamps.
    """

    created_on = p.DateTimeField()
    created_by = p.IntegerField()
    name = p.CharField(null=True)
    stopped_on = p.DateTimeField(null=True)

    class Meta:
        database = db

    @property
    def result(self):
        """
        How long did the stopwatch run?
        """

        if not self.created_on or not self.stopped_on:
            return None

        total_seconds = (self.stopped_on - self.created_on).total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return '%d:%02d:%02d' % (hours, minutes, seconds)
