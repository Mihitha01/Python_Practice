#function that extends the functionality of another function without modifying it

def add_sprinkles(func):
    def wrapper(*args, **kwargs):
        print("Adding sprinkles to your ice cream")
        func(*args, **kwargs)
    return wrapper

def add_chocolate(func):
    def wrapper(*args, **kwargs):
        print("Adding chocolate syrup to your ice cream")
        func(*args, **kwargs)
    return wrapper

def add_nuts(func):
    def wrapper(*args, **kwargs):
        print("Adding nuts to your ice cream")
        func(*args, **kwargs)
    return wrapper

@add_sprinkles
@add_chocolate
@add_nuts
def get_ice_cream(flavor):
    print(f"Here is your {flavor} ice cream")

get_ice_cream("vanilla")