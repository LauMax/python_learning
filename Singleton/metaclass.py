class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
class Database(metaclass=Singleton):
        def __init__(self, connection_string=None):
            self.connection_string = connection_string
            self.connection = self.connect_to_database(connection_string)

        def connect_to_database(self, connection_string):
            # Simulate a database connection (replace with actual connection logic)
            return f"Connected to database with {connection_string}"

        def query(self, sql):
            # Simulate a database query (replace with actual query logic)
            return f"Executing query: {sql}"
        
# Example usage of the Singleton metaclass
if __name__ == "__main__":
    ''' Example usage of the Singleton metaclass '''
    db1 = Database("db_connection_string_1")
    print(db1.connection)  # Output: Connected to database with db_connection_string_1
    db2 = Database("db_connection_string_2")
    print(db2.connection)  # Output: Connected to database with db_connection_string_1
    print(db1 is db2)  # Output: True, both are the same instance
    print(db1.query("SELECT * FROM users"))  # Output: Executing query: