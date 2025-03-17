import pytest
from AOIS.lab_2.models.logic_table import *


@pytest.fixture
def logic_table():
    return LogicTable("((!A & B) -> C) | (C ~ D)")


@pytest.fixture
def operations():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    operations_dir = os.path.join(base_dir, "operations")
    return LogicTable.load_operations_from_csv(directory=operations_dir)


def test_check_brackets_format():
    assert LogicTable._LogicTable__check_brackets_format("(A&B)") == True
    assert LogicTable._LogicTable__check_brackets_format("((A|B)") == False
    assert LogicTable._LogicTable__check_brackets_format("A&B)") == False
    assert LogicTable._LogicTable__check_brackets_format("(A&(B|C))") == True


def test_extract_subformulas(logic_table):
    subformulas = logic_table.extract_subformulas()
    assert "(C~D)" in subformulas
    assert "!A" in subformulas
    assert "(A&B)" not in subformulas


def test_generate_truth_table():
    variables = ['A', 'B']
    table = LogicTable.generate_truth_table(variables)
    expected = [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1)
    ]
    assert table == expected


def test_print_truth_table(capsys):
    header = ["A", "B", "A & B"]
    table = [
        {"A": 0, "B": 0, "A & B": 0},
        {"A": 0, "B": 1, "A & B": 0},
        {"A": 1, "B": 0, "A & B": 0},
        {"A": 1, "B": 1, "A & B": 1},
    ]

    LogicTable.print_truth_table(header, table)

    captured = capsys.readouterr()
    output = captured.out.strip()

    expected_output =('A | B | A & B\n'
                      '-------------\n'
                      '0 | 0 |   0  \n'
                      '0 | 1 |   0  \n'
                      '1 | 0 |   0  \n'
                      '1 | 1 |   1')
    assert output == expected_output


def test_compute_truth_table(logic_table,operations):
    subformulas = logic_table.extract_subformulas()
    header, table = logic_table.compute_truth_table(subformulas, operations)
    assert len(table) == 16
    assert set(header) >= {"A", "B", "C", "D", "(C~D)"}


def test_generate_sdnf(logic_table, operations):
    subformulas = logic_table.extract_subformulas()
    header, table = logic_table.compute_truth_table(subformulas, operations)
    sdnf = logic_table.generate_sdnf(header, table)
    assert isinstance(sdnf, str)
    assert sdnf.count("&") > 0
    assert sdnf.count("|") > 0


def test_generate_sknf(logic_table, operations):
    subformulas = logic_table.extract_subformulas()
    header, table = logic_table.compute_truth_table(subformulas, operations)
    sknf = logic_table.generate_sknf(header, table)
    assert isinstance(sknf, str)
    assert sknf.count("|") > 0
    assert sknf.count("&") > 0


def test_get_idx_form(logic_table, operations):
    subformulas = logic_table.extract_subformulas()
    header, table = logic_table.compute_truth_table(subformulas, operations)
    decimal, binary = LogicTable.get_idx_form(table)
    assert isinstance(decimal, int)
    assert isinstance(binary, str)
    assert set(binary) <= {"0", "1"}


def test_get_num_form(logic_table, operations):
    subformulas = logic_table.extract_subformulas()
    header, table = logic_table.compute_truth_table(subformulas, operations)
    sknf, sdnf = LogicTable.get_num_form(table)
    assert sknf.endswith("&")
    assert sdnf.endswith("|")
