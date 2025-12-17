def print_params(func):
    def wrapper(*args, **kwargs):
        print(f"Arguments: {args}, Keyword arguments: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@print_params
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# Example usage
result = greet("Alice", greeting="Hi")
print(result)