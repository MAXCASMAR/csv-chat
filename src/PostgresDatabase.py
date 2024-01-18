from typing import List
import psycopg2
import pandas as pd
import numpy as np
from psycopg2.errors import InterfaceError
import warnings
from keys import DB_KEYS



missing_keys_error_message = """No database keys found. Please create a file called db_keys.py with the following format:
    # Using the default postgres database
    >>> db_keys = {
        "host": "localhost",
        "password": "postgres",
        "user": "postgres",
        "port": 5432,
        "database": "postgres" < Optional >
    """


class PostgresDatabase:
    """
    Postgres Database Wrapper
    """

    def __init__(self, db_keys=None):
        if db_keys is None:
            try:
                db_keys = DB_KEYS
            except NameError:
                raise NameError(missing_keys_error_message)

        self.db_keys = db_keys
        self.conn = psycopg2.connect(**db_keys)
        self.cur = self.conn.cursor()

    ##################################################################
    # Helper functions
    ##################################################################
    def _execute(self, query, params=None, commit=True):
        try:
            self.cur.execute(query, params)
        except InterfaceError:
            self.conn = psycopg2.connect(**self.db_keys)
            self.cur = self.conn.cursor()
            self.cur.execute(query, params)

        if commit:
            self.conn.commit()
        try:
            return self.cur.fetchall()
        except psycopg2.ProgrammingError:
            return None

    def _execute_sql_file(self, path):
        """Reads a SQL file with multiple queries and executes them"""
        with open(path, "r") as f:
            self._execute(f.read())
        self.conn.commit()

    ##################################################################
    # Create
    ##################################################################

    def create_table(self, table_name: str, schema: dict):
        """Create table in database
        Args:
            table_name (str): Name of table
            schema (dict): Schema of table
        Example:
            >>> schema = {
                "id": "SERIAL",
                "name": "TEXT",
                "grade": "INTEGER NOT NULL"
                }
            >>> db.create_table("test", schema)
        """
        print("Creating table: ", table_name)
        query = f"CREATE TABLE {table_name} ("
        columns = ",\n".join([f"{k} {v}" for k, v in schema.items()])
        query += columns + ")"
        self._execute(query)


    def insert_df(self, table_name: str, df: pd.DataFrame):
        """Insert data from dataframe into table
        Args:
            table_name (str): Name of table
            df (pd.DataFrame): Dataframe to insert
        Example:
            >>> df = pd.DataFrame({
                "name": ["John", "Mary"],
                "grade": [5, 4]
                })
            >>> db.insert_df("test", df)
        """
        for _, row in df.iterrows():
            print(row.to_dict())
            self.insert(table_name, row.to_dict(), commit=False)
        self.conn.commit()

    ##################################################################
    # Read
    ##################################################################

    def select(self, query, return_type="pandas"):
        """Select data from table
        Args:
            query (str): SQL query
            return_type (str, optional): options ["pandas", "np", "list"]
                                        Defaults to "pandas".
        Returns:
            (pd.DataFrame, list, dict): result of select query
        """
        if return_type == "pandas":
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                return pd.read_sql(query, self.conn)
        if return_type in ["np", "list"]:
            result = self._execute(query)
            if return_type == "np":
                return np.array(result)
            elif return_type == "list":
                if len(result[0]) == 1:
                    return [r[0] for r in result]
                else:
                    return result

    ##################################################################
    # Close
    ##################################################################

    def close(self):
        """Close connection to database"""
        self.conn.close()