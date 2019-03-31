from datetime import datetime

import peewee as p

db = p.SqliteDatabase('zola.db')


class WordCounter(p.Model):
    """
    Count how many times a user has said a word
    """

    created_on = p.DateTimeField()
    user_id = p.IntegerField()
    word = p.CharField()
    count = p.IntegerField()

    class Meta:
        database = db

    @classmethod
    def record(cls, user_id, word, num):
        word = word.lower()
        row = WordCounter.get_or_none(user_id=user_id, word=word)
        if row:
            row.count += num
            row.save()
        else:
            WordCounter.create(user_id=user_id, word=word, count=num, created_on=datetime.now())
