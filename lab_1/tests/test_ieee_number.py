import pytest
from AOIS.lab_1.models.ieee_number import IEEENumber

def test_convert_float_to_ieee():
    assert IEEENumber(12.56).ieee_format_number == "0 10000010 10010001111010111000010"

def test_ieee_to_float():
    ieee = IEEENumber(12.56)
    assert pytest.approx(IEEENumber.ieee_754_2008_to_float(ieee.ieee_format_number), rel=1e-5) == 12.56

def test_ieee_addition():
    a = IEEENumber(12.56)
    b = IEEENumber(0.064)
    result = IEEENumber.ieee_754_2008_to_float(a + b)
    assert pytest.approx(result, rel=1e-5) == 12.624

def test_ieee_out_of_range():
    with pytest.raises(ValueError):
        IEEENumber(1e40)

def test_ieee_zero():
    assert IEEENumber(0.0).ieee_format_number == "0 01111111 00000000000000000000000"

def test_b_a():
    a = IEEENumber(0.064)
    b = IEEENumber(12.56)
    result = IEEENumber.ieee_754_2008_to_float(a + b)
    assert pytest.approx(result, rel=1e-5) == 12.624

def test_print():
    a=IEEENumber(12.56)
    assert str(a) == "0 10000010 10010001111010111000010"



