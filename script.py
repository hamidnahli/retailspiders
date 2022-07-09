DB_HOST = "aws-postgresql.calehf707uca.us-east-1.rds.amazonaws.com"
DB_NAME = "spiders"
DB_USER = "salma"
DB_PASS = "salma123"

import psycopg2
import psycopg2.extras

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# cur.execute("CREATE TABLE student (id SERIAL PRIMARY KEY, name VARCHAR);")

cur.execute("INSERT INTO student (name) VALUES(%s)", ("imran",))


conn.commit()

cur.close()

conn.close()