import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote

class MySql:
    """
    A class for interacting with a MySQL database.
    Parameters:
    - host (str): The hostname or IP address of the MySQL server.
    - user (str): The MySQL user to authenticate as.
    - password (str): The password to use for authentication.
    - database (str): The name of the MySQL database to use.
    """
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host 
        self.user = user 
        self.password = password
        self.database = database

    def start_connection(self):
        """
        Establishes a connection to the MySQL database.
        """
        self.connection = mysql.connector.connect(
        host= self.host,
        user= self.user,
        password= self.password,
        database = self.database
        )
        self.cursor = self.connection.cursor()

    def close_connection(self):
        """
        Closes the connection to the MySQL database.
        """
        self.cursor.close()
        self.connection.close()

    def select(self, sql_query: str) ->pd.DataFrame:
        """
        Executes a SELECT query and returns the result as a Pandas DataFrame.
        Parameters:
        - sql_query (str): The SELECT query to execute.
        Returns:
        - pd.DataFrame: Result of the SELECT query in tabular form.
        """
        try:
            self.start_connection()
            self.cursor.execute(sql_query)
            result = self.cursor.fetchall()
            data_frame = pd.DataFrame(result, columns=[desc[0] for desc in self.cursor.description])
            return data_frame
        except mysql.connector.Error as err:
            print(f"Error to connect to MySQL: {err}")
        finally:
            self.close_connection()

    def show_tables(self) -> list:
        """
        Retrieves a list of tables in the connected MySQL database.
        Returns:
        - list: A list of table names.
        """
        try:
            self.start_connection()
            self.cursor.execute(f"SHOW TABLES")
            tables = self.cursor.fetchall()
            ls_tables = []
            for table in tables:
                ls_tables.append(table)
            return ls_tables
        except mysql.connector.Error as err:
            print(f"Error to connect to MySQL: {err}")
        finally:
            self.close_connection()

    def ddl_operation(self, sql_query: str):
        """
        Executes a Data Definition Language (DDL) SQL query.
        Parameters:
        - sql_query (str): The DDL SQL query to execute.
        """
        try:
            self.start_connection()
            self.cursor.execute(sql_query)
            print('DDL Operation Executed with Sucess')
        except mysql.connector.Error as err:
            print(f"Error to connect to MySQL: {err}")
        finally:
            self.close_connection()

    def dml_operation(self, sql_query: str):
        """
        Executes a Data Manipulation Language (DML) SQL query.
        Parameters:
        - sql_query (str): The DML SQL query to execute.
        """
        try:
            self.start_connection()
            self.cursor.execute(sql_query)
            self.connection.commit()
            print('DML Operation Executed with Sucess')
        except mysql.connector.Error as err:
            print(f"Error to connect to MySQL: {err}")
        finally:
            self.close_connection()

    def insert_df(self, data_frame: pd.DataFrame, table_name: str):
        """
        Inserts a Pandas DataFrame into a specified MySQL table.
        Parameters:
        - data_frame (pd.DataFrame): The DataFrame to be inserted.
        - table_name (str): The name of the target MySQL table.
        """
        try:
            string_connection= f"mysql+mysqlconnector://{self.user}:{quote(self.password)}@{self.host}:3306/{self.database}"
            engine = create_engine(string_connection,  connect_args={'connect_timeout': 120})
            data_frame.to_sql(name=table_name, con= engine, if_exists='append', index=False, chunksize= 200000)
            print("Data insert with sucess!")
        except Exception as e:
            print(f"Error to insert data: {e}")
        finally:
            engine.dispose()