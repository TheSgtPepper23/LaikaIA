from datetime import date
import peewee as pw

laika_db = pw.SqliteDatabase('laika.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64
})

#laika_db = pw.MySQLDatabase("laika", host="localhost", port=3306, user="laika", passwd="StarWars")


class SqlLite(pw.Model):
    """Database model"""
    class Meta:
        database = laika_db


class User(SqlLite):
    id_user = pw.PrimaryKeyField()
    username = pw.CharField()
    password = pw.CharField()
    is_admin = pw.BooleanField()
    is_active = pw.BooleanField()


class Score(SqlLite):
    id_score = pw.PrimaryKeyField()
    score = pw.IntegerField()
    date = pw.DateField()
    id_user = pw.ForeignKeyField(User, db_column="id_user")


if __name__ == "__main__":
    from logic import Hash
    from datetime import date

    # laika_db.connect()
    # laika_db.create_tables([User, Score])
    # laika_db.close()

    admin = User(
        username="TheSgtPepper23", password=Hash.encrypt("An6248322"), is_admin=1, is_active=1)
    admin.save()

    player = User(
        username="fei", password=Hash.encrypt("An6248322"), is_admin=0, is_active=1)
    player.save()

    score = Score(score=0, date=date.today(), id_user=player.id_user)
    score.save()
