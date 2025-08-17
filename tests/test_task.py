from src.task import Category, Product
from typing import Any

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

    # Повышаем цену
    p.price = 1500.0
    assert p.price == 1500.0

    # Нулевая цена не проходит
    p.price = 0
    assert p.price == 1500.0

    # Отрицательная цена не проходит
    p.price = -10
    assert p.price == 1500.0

    # Подтверждение понижения цены отказ
    monkeypatch.setattr("builtins.input", lambda _: "нет")
    p.price = 900.0
    assert p.price == 1500.0

    # Подтверждение понижения цены согласие
    monkeypatch.setattr("builtins.input", lambda _: "да")
    p.price = 900.0
    assert p.price == 900.0


def test_new_product_merging(monkeypatch: Any) -> None:
    p1 = Product("Phone", "Desc", 15000.0, 2)
    existing = [p1]

    monkeypatch.setattr("builtins.input", lambda _: "да")

    # Новый продукт с тем же именем, но другой ценой и кол-вом
    data = {"name": "Phone", "description": "Updated", "price": 20000.0, "quantity": 3}

    updated = Product.new_product(data, existing)

    assert updated.name == "Phone"
    assert updated.quantity == 5  # 2 + 3
    assert updated.price == 20000.0  # цена обновилась
    assert updated.description == "Desc"  # описание не меняется

    # Новый продукт
    data2 = {"name": "Tablet", "description": "New", "price": 12000.0, "quantity": 1}

    new_p = Product.new_product(data2, existing)
    assert new_p.name == "Tablet"
    assert new_p.quantity == 1
    assert new_p.price == 12000.0
