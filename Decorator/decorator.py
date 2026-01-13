import time

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time of {func.__name__}: {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@time_it
def some_op():
    print("Some operation executed.")
    time.sleep(1)
    print("Operation completed.")
    return 123

if __name__ == "__main__":
    # time_it(some_op)()
    some_op()