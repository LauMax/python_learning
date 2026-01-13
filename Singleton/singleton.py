def singleton(class_):
    """A decorator to make a class a singleton."""
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance

@singleton
class Database:
    def __init__(self, connection_string=None):
        self.connection_string = connection_string
        self.connection = self.connect_to_database(connection_string)

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