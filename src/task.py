from __future__ import annotations
from typing import Any


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """
        Геттер для получения цены товара.
        """
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        """
        Сеттер с проверкой, где цена не может быть ≤ 0
        и при снижении цены запрос подтверждения
        """
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif value < self.__price:
            answer = (
                input(f"Вы действительно хотите понизить цену с {self.__price} до {value}? (да/нет): ").strip().lower()
            )
            if answer not in ("да", "д"):
                print("Действие отменено")
                return
            self.__price = value
        else:
            self.__price = value

    @classmethod
    def new_product(cls, data: dict, existing_products: list|None = None) -> Any:
        """
        Создаёт новый продукт если товар с таким именем уже есть:
        увеличивает количество и оставляет более высокую цену
        """
        name = data["name"]
        description = data["description"]
        price = data["price"]
        quantity = data["quantity"]

        if existing_products:
            for product in existing_products:
                if product.name == name:
                    product.quantity += quantity  # Обновляем кол-во
                    if price > product.price:
                        product.price = price  # Оставляем более высокую цену
                    return product  # Возвращаем обновлённый объект

        return cls(name, description, price, quantity)


class Category:
    category_count = 0  # Общее кол-во категорий
    product_count = 0  # Общее кол-во всех товаров

    def __init__(self, name: str, description: str, products: list[Any]):
        self.name = name
        self.description = description
        self.__products: list[Any] = []

        for product in products:
            self.add_product(product)

        Category.category_count += 1  # Категории

    def add_product(self, product: Product) -> None:
        """
        Добавляет продукт и увеличивает счетчик
        """
        if not isinstance(product, Product):  # ДОБАВЛЕНО: проверка на тип
            raise TypeError("Можно добавить только объект класса Product или его наследника")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """
        Геттер, возвращает список товаров в читаемом формате.
        """
        result = []
        for product in self.__products:
            result.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")
        return "\n".join(result)
