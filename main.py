from src.task import Category, Product

if __name__ == "__main__":
    # Продукты
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Проверка __str__ представления продуктов
    print(str(product1))
    print(str(product2))
    print(str(product3))

    # Категория
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    # Проверка __str__ представления категории
    print(str(category1))

    # Проверка геттера products (выводит все продукты в виде строки)
    print(category1.products)

    # Проверка __add__ сложения продуктов
    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)

    # Доб задание
    print("Товары в категории:")
    for product in category1:
        print(product)
