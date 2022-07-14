import os
import psycopg2
from psycopg2.extensions import AsIs
from psycopg2 import errors
from dotenv import load_dotenv
from datetime import datetime
from items.debugging import app_logger as log

load_dotenv()
UniqueViolation = errors.lookup('23505')
InFailedSqlTransaction = errors.lookup('25P02')  # if raised required "ROLLBACK"


class NineWestModel:

    def __init__(self):
        self.connection = self.connect()


    def insert(self, data: dict, table: str):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            columns, values = self._get_column_value(data)
            insert_statement = f'insert into {table} (%s) values %s'
            cursor.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
            connection.commit()
            log.info(f'{data["sku"]} inserted successfully')
        except UniqueViolation as e:
            # This error is raised if the record already exist in Database
            # if so update records except `created` attribute.
            cursor.execute("ROLLBACK")
            data.pop('created', None)
            columns, values = self._get_column_value(data)
            update_statement = f'UPDATE {table} SET (%s) = %s WHERE sku=%s'
            cursor.execute(update_statement, (AsIs(','.join(columns)), tuple(values), data['sku']))
            connection.commit()
            log.info(f'{data["sku"]} updated')
        except InFailedSqlTransaction as e:
            cursor.execute("ROLLBACK")
            log.error("cursor ROLLBACK")
        except (Exception, psycopg2.Error) as e:
            log.error(f'failed to insert into table: {e}')
        finally:
            self.close(connection)


    @staticmethod
    def connect():
        try:
            connection = psycopg2.connect(
                database=os.getenv('aws_postgres_db'),
                user=os.getenv('aws_postgres_username'),
                password=os.getenv('aws_postgres_password'),
                host=os.getenv('aws_postgres_endpoint'),
                port='5455'
            )
            return connection
        except (Exception, psycopg2.Error) as e:
            log.error(e)
        return False


    @staticmethod
    def close(connection: psycopg2.extensions.connection):
        if connection:
            try:
                connection.cursor().close()
                connection.close()
                log.info(f'connection to server closed')
            except (Exception, psycopg2.Error) as e:
                log.error(e)


    @staticmethod
    def _get_column_value(data):
        columns = data.keys()
        values = [data[column] for column in columns]
        return columns, values


    def review_bulk_insert(self, data: list, table: str):
        connection = self.connect()
        cursor = connection.cursor()
        if not data:
            log.info('there is no reviews to insert to database')
            return False
        # Check if new reviews scraped. Later on need to handle review update from source.
        sku = data[0]['sku']
        columns, _ = self._get_column_value(data[0])
        s = str('%s,' * len(columns))[:-1]
        select_statement = f'select * from {table} where sku={sku}'

        cursor.execute(select_statement)
        records = cursor.fetchall()
        if len(records) == len(data):
            log.info(f'no change, all reviews for {sku} are up to date')
        else:
            # Delete all current reviews from db
            delete_statement = f'Delete from {table} where sku={sku}'
            cursor.execute(delete_statement)
            connection.commit()
            # Insert new reviews to db
            sql_data = self.remove_non_utf8(data, update=True)
            insert_statement = f'insert into {table} ({AsIs(",".join(columns))}) values ({s})'
            cursor.executemany(insert_statement, sql_data)
            connection.commit()
            log.info(f'reviews for {sku} updated')


    @staticmethod
    def remove_non_utf8(data: list, update=False):
        for item in data:
            for k, v in item.items():
                if isinstance(v, str):
                    item[k] = v.encode('utf-8', 'ignore').decode("utf-8")
            if update:
                item['last_updated'] = str(datetime.now())
        sql_data = [tuple(ele.values()) for ele in data]
        return sql_data
