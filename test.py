import psycopg2
from items.debugging import app_logger as log
from spiders.rei import Rei

class SpiderModel:

    def __init__(self):
        self.connection = self.connect()

    @staticmethod
    def connect():
        try:
            connection = psycopg2.connect(
                user="postgresUser",
                password="postgresPW",
                host="127.0.0.1",
                port="5455",
                database="postgresDB"
            )
            return connection
        except (Exception, psycopg2.Error) as e:
            log.error(e)
            

    def create_tables(self):
        commands = (
            """ CREATE TABLE spider_product_info (
                SKU SERIAL PRIMARY KEY, 
                TITLE VARCHAR,
                DESCRIPTION VARCHAR,
                PRICE INT,
                CURRENCY VARCHAR,
                BRAND VARCHAR,
                SELLER VARCHAR,
                IMAGE VARCHAR,
                CATEGORY VARCHAR,
                REVIEW_COUNT FLOAT,
                REVIEW_RATING FLOAT,
                CREATED DATE,
                LAST_UPDATED DATE
                )
            """,
            """ CREATE TABLE spider_product_review (
                SKU SERIAL, 
                REVIEW_DATE DATE ,
                AUTHOR VARCHAR,
                LOCATION VARCHAR,
                HEADER VARCHAR ,
                BODY VARCHAR,
                RATING INT,
                THUMPS_UP INT,
                THUMPS_DOWN INT,
                CREATED DATE,
                LAST_UPDATED DATE
                )
            """
            )
        try:
            # connect to the PostgreSQL server
            connection = self.connect()
            cur = connection.cursor()
            # create table one by one
            for command in commands:
                cur.execute(command)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
    

    def insert(self, data:list):
        # connect to the PostgreSQL server
        connection = self.connect()
        cur = connection.cursor()
        if not data:
            log.info('there is no reviews to insert to database')
            return False

        print(type(data))

        for d in data:
            print(list(d.values()))
            cur.execute("INSERT INTO spider_product_review (SKU, REVIEW_DATE, AUTHOR, LOCATION, HEADER, BODY, RATING, THUMPS_UP, THUMPS_DOWN, CREATED, LAST_UPDATED) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",list(d.values()))
            
        connection.commit()
        connection.close()


        # info_insert_query = "INSERT INTO spider_product_info (SKU, TITLE, TITLE, DESCRIPTION, PRICE, CURRENCY, BRAND, SELLER, IMAGE, CATEGORY, REVIEW_COUNT, REVIEWW_RATING, CREATED, LAST_UPDATED) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # record_to_insert = (5, 'One Plus 6', 950)
        # cur.execute(info_insert_query, record_to_insert)



if __name__ == '__main__':
    url = 'https://www.rei.com/product/146801/patagonia-capilene-cool-daily-hoodie-mens'
    p = Rei(product_url=url)
    #print(p.get_product_info())
    data = p.get_product_review()

p = SpiderModel()
p.create_tables()
p.insert(data)



