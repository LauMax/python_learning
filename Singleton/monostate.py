class CEO:
    __shared_state = {
        "name": "Alice Johnson",
        "age": 50,
        "company": "Tech Innovations Inc."
    }

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __str__(self):
        return f"CEO Name: {self.name}, Age: {self.age}, Company: {self.company}"
    
if __name__ == "__main__":
    ceo1 = CEO()
    print(ceo1)  # Output: CEO Name: Alice Johnson, Age: 50, Company: Tech Innovations Inc.

    ceo2 = CEO()
    ceo2.age = 51  # Modify age through the second instance

    print(ceo1)  # Output: CEO Name: Alice Johnson, Age: 51, Company: Tech Innovations Inc.
    print(ceo1 is ceo2)  # Output: False, different instances but shared state