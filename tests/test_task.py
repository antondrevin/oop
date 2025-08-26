from typing import Any
import pytest

from src.task import Category, Product, Smartphone, LawnGrass


def test_add_product_in_category() -> None:
    Category.category_count = 0
    Category.product_count = 0

    p = Product("TV", "Smart TV", 50000.0, 4)
    c = Category("Electronics", "TVs and more", [])

    assert Category.category_count == 1
    assert Category.product_count == 0

    c.add_product(p)

    assert Category.product_count == 1
    assert "TV, 50000.0 руб. Остаток: 4 шт." in c.products


def test_getter_setter_price(monkeypatch: Any) -> None:
    p = Product("Item", "Test item", 1000.0, 1)

    p.price = 1500.0
    assert p.price == 1500.0

    p.price = 0
    assert p.price == 1500.0

    p.price = -10
    assert p.price == 1500.0

    monkeypatch.setattr("builtins.input", lambda _: "нет")
    p.price = 900.0
    assert p.price == 1500.0

    monkeypatch.setattr("builtins.input", lambda _: "да")
    p.price = 900.0
    assert p.price == 900.0


def test_new_product_merging(monkeypatch: Any) -> None:
    p1 = Product("Phone", "Desc", 15000.0, 2)
    existing = [p1]

    monkeypatch.setattr("builtins.input", lambda _: "да")

    data = {"name": "Phone", "description": "Updated", "price": 20000.0, "quantity": 3}

    updated = Product.new_product(data, existing)

    assert updated.name == "Phone"
    assert updated.quantity == 5  # 2 + 3
    assert updated.price == 20000.0
    assert updated.description == "Desc"

    data2 = {"name": "Tablet", "description": "New", "price": 12000.0, "quantity": 1}

    new_p = Product.new_product(data2, existing)
    assert new_p.name == "Tablet"
    assert new_p.quantity == 1
    assert new_p.price == 12000.0


def test_category_iteration() -> None:
    p1 = Product("Телефон", "desc", 10000.0, 3)
    p2 = Product("Планшет", "desc", 20000.0, 2)
    category = Category("Гаджеты", "desc", [p1, p2])

    names = [product.name for product in category]
    assert names == ["Телефон", "Планшет"]


def test_add_wrong_type_product() -> None:
    """
    Проверяет, что в категорию нельзя добавить объект, не являющийся Product.
    """
    category = Category("Игрушки", "Категория с игрушками", [])

    # Передаём строку вместо объекта Product специально
    with pytest.raises(TypeError):
        category.add_product("не продукт")  # type: ignore


def test_add_product_accepts_valid_types() -> None:
    cat = Category("Test", "Тестовая категория", [])

    smartphone = Smartphone("iPhone", "desc", 1000.0, 2, 95.5, "14", 128, "black")
    grass = LawnGrass("Grass", "desc", 500.0, 5, "Россия", "7 дней", "зелёный")
    generic = Product("Мыло", "desc", 100.0, 10)

    cat.add_product(smartphone)
    cat.add_product(grass)
    cat.add_product(generic)

    assert Category.product_count >= 3


def test_add_product_rejects_wrong_types() -> None:
    cat = Category("Test", "Тестовая категория", [])

    # Передаём строку вместо объекта Product должна возникнуть ошибка TypeError
    with pytest.raises(TypeError):
        cat.add_product("Не продукт")  # type: ignore

    # Передаём целое число не является продуктом, ожидаем TypeError
    with pytest.raises(TypeError):
        cat.add_product(123)  # type: ignore

    # Передаём список тоже недопустимый тип, проверяем защиту
    with pytest.raises(TypeError):
        cat.add_product(["список"])  # type: ignore

    # Передаём None невалидный тип, должен быть вызван TypeError
    with pytest.raises(TypeError):
        cat.add_product(None)  # type: ignore
