from src.homework_14_1 import Product, Category


def test_product_init() -> None:
    prod = Product("Test", "Desc", 10.5, 10)
    assert prod.name == "Test"
    assert prod.description == "Desc"
    assert prod.price == 10.5
    assert prod.quantity == 10


def test_category_init() -> None:
    prod_1 = Product("One", "Desc", 50.0, 1)
    prod_2 = Product("Two", "Desc", 70.0, 3)

    category = Category("TestCat", "DescCat", [prod_1, prod_2])

    assert category.name == "TestCat"
    assert category.description == "DescCat"
    assert len(category.products) == 2
    assert Category.category_count == 1
    assert Category.product_count == 2
