import pytest
from AOIS.lab_1.models.binary_number import BinaryNumber
from AOIS.lab_7.diagonal_matrix import DiagonalMatrix


@pytest.fixture
def matrix():
    m = DiagonalMatrix(rows=16, cols=16)
    for i in range(16):
        word = [int(b) for b in BinaryNumber.to_binary(i * 1000 % 32768, 16)]
        m.write_word(i, word)
    return m


def test_read_write_word(matrix):
    word = [1, 0] * 8  
    assert len(word) == 16
    matrix.write_word(0, word)
    read = matrix.read_word(0)
    assert read == word


def test_logic_disjunction(matrix):
    a = [0, 1] * 8
    b = [1, 0] * 8
    result = matrix.logic_disjunction(a, b)
    assert result == [1] * 16


def test_logic_disjunction_negation(matrix):
    a = [0, 0, 1, 1] * 4
    b = [1, 0, 1, 0] * 4
    result = matrix.logic_disjunction_negation(a, b)
    expected = [0, 1, 0, 0] * 4
    assert result == expected


def test_logic_implication(matrix):
    a = [1, 1, 0, 0] * 4
    b = [1, 0, 1, 0] * 4
    result = matrix.logic_implic_from1_to2(a, b)
    expected = [1, 0, 1, 1] * 4
    assert result == expected


def test_add_fields_by_key(matrix):
    key_v = '101'
    word = [1, 0, 1] + [0, 0, 1, 0] + [0, 0, 1, 1] + [0] * 5
    assert len(word) == 16
    matrix.write_word(0, word)
    matrix.add_fields_by_key(key_v)
    updated = matrix.read_word(0)
    sum_val = (2 + 3) % 32
    expected_s = [int(b) for b in BinaryNumber.to_binary(sum_val, 5)]
    assert updated[11:] == expected_s


def test_search_in_range(matrix, capsys):
    lower = [0] * 16
    upper = [1] * 16
    matrix.search_in_range(lower, upper)
    captured = capsys.readouterr()
    assert "Слова, попавшие в указанный интервал" in captured.out


def test_str_representation(matrix):
    output = str(matrix)
    lines = output.strip().split('\n')
    assert lines[0] == "Матрица:"
    assert len(lines[1:]) == 16
    for line in lines[1:]:
        bits = line.strip().split()
        assert len(bits) == 16
        assert all(bit in ['0', '1'] for bit in bits)

def test_logic_first_arg_ban(matrix):
    word1 = [1, 0] * 8
    word2 = [1, 1, 0, 0] * 4

    expected_result = [
        a & (~b & 1)
        for a, b in zip(word1, word2)
    ]

    result = matrix.logic_first_arg_ban(word1, word2)
    assert result == expected_result


def test_write_and_read_address_column(matrix):
    test_address = [i % 2 for i in range(16)]
    matrix.write_address_column(5, test_address)
    read_address = matrix.read_address_column(5)
    assert read_address == test_address


def test_write_address_column_invalid_length(matrix, capsys):
    short_address = [1] * 10
    matrix.write_address_column(0, short_address)
    captured = capsys.readouterr()
    assert "Некорректная длина адресного столбца" in captured.out


def test_add_fields_by_key_invalid_length(matrix):
    with pytest.raises(ValueError, match="Ключ V должен быть длиной 3 бита"):
        matrix.add_fields_by_key("10")

    with pytest.raises(ValueError, match="Ключ V должен быть длиной 3 бита"):
        matrix.add_fields_by_key("1001")

    with pytest.raises(ValueError, match="Ключ V должен быть длиной 3 бита"):
        matrix.add_fields_by_key([])


def test_binary_str_to_list():
    binary_str = "101010"
    result = DiagonalMatrix.binary_str_to_list(binary_str)
    assert result == [1, 0, 1, 0, 1, 0]


def test_list_to_binary_str():
    bits = [1, 1, 0, 0, 1]
    result = DiagonalMatrix.list_to_binary_str(bits)
    assert result == "11001"


def test_write_word_invalid_length(matrix, capsys):
    invalid_word = [1, 0, 1]
    matrix.write_word(0, invalid_word)
    captured = capsys.readouterr()
    assert "Некорректная длина слова" in captured.out
