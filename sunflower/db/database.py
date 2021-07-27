from peewee import SqliteDatabase


class Database:
    # TODO: create SINGLETON class
    def __init__(self, database_url=None):
        self._db = None
        self.database_url = database_url

    @property
    def db(self):
        if self._db is None:
            self._db = SqliteDatabase("database.db")
        return self._db

    def create_tables(self, models):
        with self.db:
            self.db.create_tables(models)
