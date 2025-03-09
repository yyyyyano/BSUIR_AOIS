import pytest
from AOIS.lab_1.models.binary_number import BinaryNumber  # Убедись, что имя файла с классом BinaryNumber — binary_number.py


def test_convert_to_direct_code_positive():
    assert BinaryNumber.convert_to_direct_code(14) == "0 0001110"

def test_convert_to_direct_code_negative():
    assert BinaryNumber.convert_to_direct_code(-33) == "1 0100001"

def test_is_valid_decimal_true():
    assert BinaryNumber.is_valid_decimal(14) == True

def test_is_valid_decimal_false():
    assert BinaryNumber.is_valid_decimal(-133) == False

def test_convert_to_reversed_code_positive():
    assert BinaryNumber.convert_to_reversed_code("0 0001100") == "0 0001100"

def test_convert_to_reversed_code_negative():
    assert BinaryNumber.convert_to_reversed_code("1 0001100") == "1 1110011"

def test_convert_to_additional_code_positive():
    assert BinaryNumber.convert_to_additional_code("0 0001100") == "0 0001100"

def test_convert_to_additional_code_negative():
    assert BinaryNumber.convert_to_additional_code("1 0001100") == "1 1110100"

def test_binary_int_to_decimal_positive():
    assert BinaryNumber.binary_int_to_decimal("0 0001100") == 12

def test_binary_int_to_decimal_negative():
    assert BinaryNumber.binary_int_to_decimal("1 0001100") == -12

def test_additional_to_decimal_positive():
    assert BinaryNumber(5) + BinaryNumber(3) == ("0 0001000", 8)

def test_additional_to_decimal_negative():
    assert BinaryNumber(-5) + BinaryNumber(3) == ("1 1111110", -2)

def test_sum_out_of_range():
    BinaryNumber(110) + BinaryNumber(27)  # Выполняем сложение, которое выходит за диапазон

def test_sum_out_min():
    BinaryNumber(-114)+BinaryNumber(-27)

def test_minus_posit():
    assert BinaryNumber(5) - BinaryNumber(3) == ("0 0000010", 2)

def test_minus_neg():
    assert BinaryNumber(-5) - BinaryNumber(3) == ("1 1111000", -8)

def test_mult_out_of_range():
    assert BinaryNumber(12) * BinaryNumber(12) == "Multiply is out of range (-127, 127)"

def test_mult_zero():
    assert BinaryNumber(10) * BinaryNumber(0) == BinaryNumber.BINARY_ZERO

def test_mult_posit():
    assert BinaryNumber(12) * BinaryNumber(4) == ("0 0110000", 48)

def test_mult_neg():
    assert BinaryNumber(-12) * BinaryNumber(4) == ("1 0110000", -48)

def test_div_zero():
    assert BinaryNumber(10) / BinaryNumber(0) == "Error: division by zero"

def test_div_posit():
    assert BinaryNumber(12) / BinaryNumber(4) == ("0 0000011", 3.0)

def test_div_neg():
    assert BinaryNumber(-6) / BinaryNumber(5) == ('1 0000001.0011001100', -1.19921875)

def test_print_posit():
    a=BinaryNumber(11)
    expect_str= ("\nDirect code: 0 0001011"
                "\nReversed code: 0 0001011"
                "\nAdditional code: 0 0001011")
    assert str(a)==expect_str

def test_print_neg():
    a=BinaryNumber(-11)
    expect_str= ("\nDirect code: 1 0001011"
                "\nReversed code: 1 1110100"
                "\nAdditional code: 1 1110101")
    assert str(a)==expect_str

def test_float_to_float():
    assert BinaryNumber.binary_float_to_float("0.101")==0.625
