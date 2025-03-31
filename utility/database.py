import sqlite3


class Database:

    def __init__(self):
        self.db_path = "db/test.sqlite3"
        # isolation_level=None enables auto commit
        self.conn = sqlite3.connect(database=self.db_path, isolation_level=None)
        self.cursor = self.conn.cursor()

    def load_data(self):
        """
        Helper method
        """
        INSERT_CUSTOMERS = """
            INSERT INTO customers (name, email) 
            VALUES
            ('Alice Smith', 'alice@example.com'),
            ('Bob Johnson', 'bob@example.com');
        """
        INSERT_ORDERS = """
            INSERT INTO orders (customer_id, order_date, amount, product)  
            VALUES  
            (4, '2025-03-10', 250.50, 'Laptop'),  
            (4, '2025-03-12', 99.99, 'Wireless Mouse'),  
            (4, '2025-03-15', 450.75, 'Smartphone'),  
            (5, '2025-03-18', 75.00, 'Headphones'),  
            (5, '2025-03-22', 1200.00, 'Gaming Console');
        """
        self.cursor.execute(INSERT_CUSTOMERS)
        self.cursor.execute(INSERT_ORDERS)
        self.close()
        print("[SQL] Loaded data successfully.")

    def get_db_schema(self):
        SELECT_TABLE_QUERY = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        PRAGMA_TABLE_QUERY = "PRAGMA table_info({name})"

        self.cursor.execute(SELECT_TABLE_QUERY)
        tables = self.cursor.fetchall()

        schema = {}
        for table in tables:
            name = table[0]
            self.cursor.execute(PRAGMA_TABLE_QUERY.format(name=name))
            columns = self.cursor.fetchall()
            schema[name] = [col[1] for col in columns]

        self.close()
        return schema
    
    def execute(self, sql_query: str):
        self.cursor.execute(sql_query)
        results = self.cursor.fetchall()
        self.close()
        return results

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    instance = Database()
    instance.get_db_schema()
    # instance.load_data()
