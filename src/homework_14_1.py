class Product:
    name: str
    description: str
    price: float
    quantity: int
    product_count = 0

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        Product.product_count += 1

    def __str__(self) -> str:
        return f"{self.name} - {self.description} - {self.price} - {self.quantity}"


class Category:
    name: str
    description: str
    products: list
    product_count = 0
    category_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products

        Category.product_count += len(products)
        Category.category_count += 1

    def __str__(self) -> str:
        return f"{self.name} - {self.description} - {self.products}"
