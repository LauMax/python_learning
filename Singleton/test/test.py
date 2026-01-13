import unittest
import os

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.population_data = {}
        # 使用绝对路径，避免工作目录问题
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "capitals.txt")
        f = open(file_path, "r")
        lines = f.readlines()
        for i in range(0,len(lines),2):
            city = lines[i].strip()
            population = int(lines[i+1].strip())
            self.population_data[city] = population
        f.close()

class SingletonRecordFinder:
    def total_population(self, cities):
        result = 0
        db = Database()
        for city in cities:
            result += db.population_data.get(city, 0)
        return result
    
class SingletonTests(unittest.TestCase):

    def test_is_singleton(self):
        db1 = Database()
        db2 = Database()
        self.assertIs(db1, db2)
    
    def test_singleton_total_population(self):
        rf = SingletonRecordFinder()
        cities = ["Seoul", "Mexico City"]
        tp = rf.total_population(cities)
        self.assertEqual(17500000 + 17400000, tp)
        
    
if __name__ == "__main__":
    unittest.main()