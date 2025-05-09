import pytest
from unittest.mock import patch
import json
from io import StringIO
from AOIS.lab_6.model.linear_hash_table import *


@pytest.fixture
def hash_table():
    return LinearHashTable()


def test_insert_new_item(hash_table):
    hash_table.insert_new_item("inertia", "the ability to maintain velocity")
    assert hash_table.table[21].ID == "inertia"
    assert hash_table.table[21].Pi == "the ability to maintain velocity"
    assert hash_table.num_of_occupied_cells == 1


def test_insert_duplicate_item(hash_table):
    hash_table.insert_new_item("inertia", "the ability to maintain velocity")
    initial_count = hash_table.num_of_occupied_cells
    hash_table.insert_new_item("inertia", "updated data")
    assert hash_table.num_of_occupied_cells == initial_count
    assert hash_table.table[21].Pi == "the ability to maintain velocity"


def test_find_by_key(hash_table):
    hash_table.insert_new_item("inertia", "the ability to maintain velocity")
    found_data = hash_table.find_by_key("inertia")
    assert found_data == "the ability to maintain velocity"

def test_update_item(hash_table):
    hash_table.insert_new_item("inertia", "the ability to maintain velocity")
    hash_table.insert_new_item("inennnn", "the ability to maintain velocity")
    updated = hash_table.update_item("inennnn", "updated data")
    hash_table.update_item("NOKEY", "updated data")
    assert updated is True
    assert hash_table.table[22].Pi == "updated data"


def test_delete_item(hash_table):
    hash_table.insert_new_item("inertia", "the ability to maintain velocity")
    hash_table.insert_new_item("inennnn", "the ability to maintain velocity")
    deleted = hash_table.delete_item_by_key("inennnn")
    assert deleted is True
    assert hash_table.table[21].U == 1
    assert hash_table.table[22].U == 0
    assert hash_table.num_of_occupied_cells == 1


def test_find_nonexistent_key(hash_table):
    result = hash_table.find_by_key("nonexistent")
    assert result is None


def test_get_fullness(hash_table):
    hash_table.insert_new_item("inertia", "the ability to maintain velocity")
    assert hash_table.get_fullness() == 1 / 25


def test_collision_handling(hash_table):
    hash_table.insert_new_item("inertia", "the ability to maintain velocity")
    hash_table.insert_new_item("resistance", "opposition to current")

    assert hash_table.table[21].ID == "inertia"
    assert hash_table.table[21].Po == 22
    assert hash_table.table[22].ID == "resistance"
    assert hash_table.table[22].Po == -1


def test_load_data(monkeypatch):
    test_data = {
        "inertia": "the ability to maintain velocity",
        "resistance": "opposition to current"
    }

    def mock_open(file, mode, encoding=None):
        class MockFile:
            def __init__(self, data):
                self.data = data

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                pass

            def read(self):
                return json.dumps(self.data)

        return MockFile(test_data)

    monkeypatch.setattr('builtins.open', mock_open)
    key_data = LinearHashTable.load_data('test_data.json')

    assert len(key_data) == 2
    assert key_data[0] == ("inertia", "the ability to maintain velocity")
    assert key_data[1] == ("resistance", "opposition to current")


def test_update_item1(monkeypatch):
    hash_table = LinearHashTable()
    hash_table.insert_new_item("inertia", "the ability to maintain velocity")

    result = hash_table.update_item("inertia", "updated value")
    assert result == True
    assert hash_table.table[0].Pi == ""

    result=hash_table.update_item("noo", "updated value")
    assert result == None

    result = hash_table.update_item("nonexistent", "some value")
    assert result == None

    hash_table.table[0].Po = -1
    result = hash_table.update_item("inertia", "updated again")
    assert result == True
    assert hash_table.table[0].Pi == ""

    for i in range(1, hash_table.size):
        hash_table.insert_new_item(f"key{i}", f"value{i}")

    result = hash_table.update_item("inertia", "should not update")
    assert result == True


def test_load_data_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = LinearHashTable.load_data("non_existing_file.json")
        assert result == []


def test_str_with_elements():
    hash_table = LinearHashTable()
    hash_table.insert_new_item("inertia", "the ability to maintain velocity")
    hash_table.insert_new_item("resistance", "opposition to current")

    str_rep = str(hash_table)

    assert "inertia" in str_rep
    assert "resistance" in str_rep
    assert "Fullness of table: 0.08" in str_rep


def test_load_data_json_decode_error():
    invalid_json_data = "{invalid_json: true"

    mock_file = StringIO(invalid_json_data)

    with patch("builtins.open", return_value=mock_file):
        with patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "doc", 0)):
            result = LinearHashTable.load_data("invalid_file.json")
            assert result == []
