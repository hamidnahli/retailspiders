from typing import List
import psycopg2
from items.debugging import app_logger as log
from dotenv import load_dotenv
import os
load_dotenv()

class SpiderModel:

    def __init__(self):
        self.connection = self.connect()

    @staticmethod
    def connect():
        try:
            connection = psycopg2.connect(
                user=os.getenv('docker_postgres_username'),
                password=os.getenv('docker_postgres_password'),
                host=os.getenv('docker_postgres_host'),
                port='5455',
                database=os.getenv('docker_postgres_db')
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
                PRICE FLOAT,
                CURRENCY VARCHAR,
                BRAND VARCHAR,
                SELLER VARCHAR,
                IMAGE VARCHAR,
                CATEGORY VARCHAR,
                REVIEW_COUNT FLOAT,
                REVIEW_RATING FLOAT,
                CREATED DATE,
                LAST_UPDATED DATE,
                PRODUCT_URL VARCHAR,
                SPIDER VARCHAR
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
    

    def insert(self, data_review:List,data_product):
        connection = self.connect()
        cur = connection.cursor()
        
        if not data_review:
            log.info('there is no reviews to insert to database')
            return False

        for dr in data_review:
            cur.execute("INSERT INTO spider_product_review (SKU, REVIEW_DATE, AUTHOR, LOCATION, HEADER, BODY, RATING, THUMPS_UP, THUMPS_DOWN, CREATED, LAST_UPDATED) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",list(dr.values()))
        
        cur.execute("INSERT INTO spider_product_info (SKU, TITLE, DESCRIPTION, PRICE, CURRENCY, BRAND, SELLER, IMAGE, CATEGORY, REVIEW_COUNT, REVIEW_RATING, CREATED, LAST_UPDATED, PRODUCT_URL, SPIDER) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",list(data_product.values()))
        connection.commit()
        connection.close()

