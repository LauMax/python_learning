class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self, connection_string=None):
        if not hasattr(self, 'initialized'):  # Prevent re-initialization
            self.connection_string = connection_string
            self.connection = self.connect_to_database(connection_string)
            self.initialized = True

    def connect_to_database(self, connection_string):
        # Simulate a database connection (replace with actual connection logic)
        return f"Connected to database with {connection_string}"

    def query(self, sql):
        # Simulate a database query (replace with actual query logic)
        return f"Executing query: {sql}"
    
if __name__ == "__main__":
    db1 = Database("db_connection_string_1")
    print(db1.connection)  # Output: Connected to database with db_connection_string_1

    db2 = Database("db_connection_string_2")
    print(db2.connection)  # Output: Connected to database with db_connection_string_1

    print(db1 is db2)  # Output: True, both are the same instance

    print(db1.query("SELECT * FROM users"))  # Output: Executing query: SELECT * FROM users