import psycopg2
import os

dbname = os.environ['DB_NAME']
print(dbname)

conn = psycopg2.connect("dbname=suppliers user=postgres password=postgres")

def get_db(db_file):
    """ create a database connection to a SQLite database """
    ...

def create_tables(db):
    ...

