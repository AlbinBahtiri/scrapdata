from io import StringIO
import psycopg2
import pandas as pd
import gc



class HandlingDataDb:

    def __init__(self, ip_address, port, user, password,database='databaseprod_987y'):

        self.ip_address = ip_address
        self.port = str(port)
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect_db(self):
        """
        Create the connection to the database.
        """
        self.C = psycopg2.connect(
            dbname=self.database,
            host=self.ip_address,
            user=self.user,
            password=self.password
        )
        self.C.set_client_encoding('UTF8')
        self.cursor = self.C.cursor()

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def push_df_to_db(self, df, table_name, additional_columns=None):
        """
        Push a DataFrame to a PostgreSQL table, adding default values for extra columns if needed.
        Args:
            df (pd.DataFrame): The DataFrame to push.
            table_name (str): The name of the table in the database.
            additional_columns (dict): A dictionary of column names and their default values.
                                       These columns will be added with the specified defaults.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame.")

        # Convert column names to lowercase and remove problematic characters
        df.columns = [col.lower().replace(' ', '_').replace('/', '_') for col in df.columns]

        # Add additional columns with default values if specified
        if additional_columns:
            for column, default_value in additional_columns.items():
                if column not in df.columns:
                    df[column] = default_value

        # Create a CSV buffer
        buffer = StringIO()
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)

        # Get column names excluding 'id'
        column_names = ', '.join(df.columns)

        # Use COPY command to push data (exclude the 'id' column)
        try:
            self.cursor.copy_expert(f"COPY {table_name} ({column_names}) FROM STDIN WITH CSV", buffer)
            self.C.commit()
            print(f"Data successfully pushed to table: {table_name}")
        except Exception as e:
            self.C.rollback()
            print(f"Error pushing data to table {table_name}: {e}")


