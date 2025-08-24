from __future__ import annotations

from typing import Any, Iterator


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        """
        Для строкового отображения объекта Product
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Product) -> float:
        """
        Для подсчета общей стоимости двух продуктов
        """
        if isinstance(other, Product):
            return self.price * self.quantity + other.price * other.quantity
        return NotImplemented

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
    def new_product(cls, data: dict, existing_products: list | None = None) -> Any:
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


class Smartphone(Product):  # Подкласс от Product
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):  # Подкласс от Product
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


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

    def __str__(self) -> str:
        """
        Для строкового отображения объекта Category
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> Iterator:
        """
        Возвращает итератор для перебора продуктов.
        """
        return CategoryIterator(self)

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

    def _get_products(self) -> list[Product]:
        """
        Внутренний метод для доступа к списку продуктов.
        Используется итератором.
        """
        return self.__products


class CategoryIterator:
    """
    Итератор для перебора продуктов в категории.
    """

    def __init__(self, category: Category):
        self._products = category._get_products()  # доступ к защищённому методу для итератора
        self._index = 0

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> Product:
        if self._index < len(self._products):
            product = self._products[self._index]
            self._index += 1
            return product
        raise StopIteration
