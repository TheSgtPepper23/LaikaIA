import peewee as pw

laika_db = pw.MySQLDatabase(
    "laika", host="localhost", port=3306, user="laika", passwd="StarWars")

class MySQLModel(pw.Model):
    """Database model"""
    class Meta:
        database = laika_db

class User(MySQLModel):
    id_user = pw.PrimaryKeyField()
    username = pw.CharField()
    password = pw.CharField()
    is_admin = pw.BooleanField()
    is_active = pw.BooleanField()

class Score(MySQLModel):
    id_score = pw.PrimaryKeyField()
    score = pw.IntegerField()
    date = pw.DateField()
    id_user = pw.ForeignKeyField(rel_model=User, db_column="id_user")
