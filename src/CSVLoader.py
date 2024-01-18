import pandas as pd
import numpy as np
from PostgresDatabase import PostgresDatabase
from config import CSV_PATH, SCHEMA, TABLE_NAME

# define constants
DATA = pd.read_csv(CSV_PATH)

# class that processes and inserts csv data into postgres table
class DataLoader:
    def __init__(self, table_name, schema = SCHEMA):
        self.table_name = table_name
        self.schema = schema
        self.df = DATA
        self.db = PostgresDatabase()

        # process data
        self.handle_missing_values()

        # create table in postgres database
        self.create_table()

        # load data into postgres table
        self.insert_data()
    
    def handle_missing_values(self):
        self.df['has_pool'] = self.df['has_pool'].apply(lambda x: bool(x) if pd.notnull(x) else None)
        self.df['has_terrace'] = self.df['has_terrace'].apply(lambda x: bool(x) if pd.notnull(x) else None)
        self.df = self.df.replace(np.nan, None)

    def create_table(self):
        self.db.create_table(self.table_name, self.schema)

    def insert_data(self):
        self.db.insert_df(self.table_name, self.df)

if __name__ == "__main__":
    DataLoader(TABLE_NAME)