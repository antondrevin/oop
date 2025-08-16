from src.load_file import load_data_from_json
import json


def test_load_data_from_json(product: list) -> None:
    with open("data/test_products.json", "w", encoding="utf-8") as f:
        json.dump(product, f, ensure_ascii=False, indent=2)

    loaded_categories = load_data_from_json("data/test_products.json")


    for category in loaded_categories:
        assert category.name == "Смартфоны"
        assert category.description == "Смартфоны, как средство"
