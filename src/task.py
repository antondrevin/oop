from __future__ import annotations

from typing import Any, Iterator
from abc import ABC, abstractmethod


class BaseProduct(ABC):
    @abstractmethod
    def __str__(self) -> str:
        ...

    @property
    @abstractmethod
    def price(self) -> float:
        ...

    @price.setter
    @abstractmethod
    def price(self, value: float) -> None:
        ...


class LoggerMixin:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        print(f"Создан объект класса {self.__class__.__name__} с аргументами: {args}, {kwargs}")


class Product(LoggerMixin, BaseProduct):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        super().__init__(name, description, price, quantity)
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __add__(self, other: "Product") -> float:  # переделано
        """
        Складывает два объекта одного и того же класса (Product или его наследники)
        """
        if type(self) != type(other):
            raise TypeError("Можно складывать только объекты одного типа")

        return self.price * self.quantity + other.price * other.quantity

    def __str__(self) -> str:
        """
        Для строкового отображения объекта Product
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}, {self.description!r}, {self.price}, {self.quantity})"

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

    def __str__(self) -> str:
        base_info = super().__str__()
        return f"{base_info} | Модель: {self.model}, Память: {self.memory}, Цвет: {self.color}"


class LawnGrass(Product):  # Подкласс от Product
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        base_info = super().__str__()
        return f"{base_info} | Период роста: {self.germination_period}, Страна: {self.country}"


class AbstractCategory(ABC):
    @abstractmethod
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class Order(AbstractCategory):
    def __init__(self, product: Product, quantity: int):
        super().__init__(product.name, product.description)
        self.product = product
        self.quantity = quantity
        self.total_price = self.product.price * quantity

    def __str__(self) -> str:
        return f"Заказ: {self.product.name} x {self.quantity}, итого: {self.total_price} руб."

    @property
    def total(self) -> float:
        return self.product.price * self.quantity


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
