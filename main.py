from src.task import Category, Product


if __name__ == "__main__":
    # Создание первых 3 товаров
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Выводим свойства одного товара
    print(product1.name)  # Название
    print(product1.description)  # Описание
    print(product1.price)  # Цена (через геттер)
    print(product1.quantity)  # Кол-во

    # Создание категории с этими товарами
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    # Проверяем, что всё создалось правильно
    print(category1.name == "Смартфоны")  # Должно быть True
    print(category1.description)  # Описание категории

    # category1.products теперь возвращает отформатированную строку, а не список!
    print(category1.products)  # Выводим красиво все товары в категории

    # Если нужно узнать, сколько товаров в категории и считаем строки
    print(category1.products.count("\n") + 1)

    # Общие счётчики категорий и товаров
    print(Category.category_count)  # Всего категорий
    print(Category.product_count)  # Всего товаров

    # Добавление нового товара
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4],
    )

    # Проверка второй категории
    print(category2.name)
    print(category2.description)
    print(category2.products)  # Отформатированная строка

    # Обновлённые счётчики
    print(Category.category_count)  # Должно быть 2
    print(Category.product_count)  # Должно быть 4
