customer = {
    "name": "John Smith",
    "age": 30,
    "is_verified": True
}

print(customer["name"]) #case sensetive

customer["name"]  = "Jack Smith"

print(customer.get("name"))
print(customer.get("birthday"))

