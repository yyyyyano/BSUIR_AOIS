from AOIS.lab_1.models.binary_number import *

class IEEENumber(BinaryNumber):
    EXP_CONSTANT=127
    EXP_START_IDX=2
    EXP_END_IDX=10
    EXP_LENGTH=8
    MANTISSA_START_IDX=11
    MANTISSA_LENGTH=23

    def __init__(self,float_number:float):
        self.float_number = float_number
        self.ieee_format_number = self.convert_to_ieee_754_2008(float_number)


    @staticmethod
    def __convert_float_to_binary(number: float):
        int_part = int(number)
        fractional_part = number - int_part

        binary_int_part = IEEENumber._to_binary(int_part)

        binary_fractional_part = ""
        counter = 0
        max_iterations = 20

        while counter < max_iterations and fractional_part != 0:
            fractional_part *= 2
            if fractional_part >= 1:
                binary_fractional_part += "1"
                fractional_part -= 1
            else:
                binary_fractional_part += "0"
            counter += 1

        binary_float = binary_int_part + "." + binary_fractional_part
        return binary_float


    @staticmethod
    def convert_to_ieee_754_2008(number: float):
        binary_float = IEEENumber.__convert_float_to_binary(number)

        if '.' in binary_float:
            binary_float = binary_float.lstrip('0')
            if binary_float[0] == '.':
                binary_float = '0' + binary_float

        shift_count = 0
        if '1' in binary_float:
            if number >= 1.0:
                while not (binary_float[0] == '1' and binary_float[1] == '.'):
                    point_index = binary_float.index('.')
                    binary_float = (
                            binary_float[:point_index - 1] +
                            binary_float[point_index] +
                            binary_float[point_index - 1] +
                            binary_float[point_index + 1:]
                    )
                    shift_count += 1
            else:
                binary_float = binary_float[1:]
                while binary_float[0] != '1':
                    binary_float = binary_float[1:]
                    shift_count -= 1
                binary_float = binary_float[0] + "." + binary_float[1:]

        exponenta = IEEENumber.EXP_CONSTANT + shift_count
        if exponenta <= 0 or exponenta >= 255:
            raise ValueError(f"Exponent value {exponenta} out of range IEEE 754 (32-bit).")

        binary_exponenta = bin(exponenta)[IEEENumber.EXP_START_IDX:].zfill(IEEENumber.EXP_LENGTH)
        mantissa = binary_float.split('.')[1]
        mantissa = mantissa.ljust(IEEENumber.MANTISSA_LENGTH, '0')[:IEEENumber.MANTISSA_LENGTH]
        binary_number = "0 " + binary_exponenta + " " + mantissa
        return binary_number


    @staticmethod
    def ieee_754_2008_to_float(ieee_number):
        exponenta_binary = ieee_number[IEEENumber.EXP_START_IDX:IEEENumber.EXP_END_IDX]
        mantissa_binary = ieee_number[IEEENumber.MANTISSA_START_IDX:]

        exponenta = IEEENumber._to_decimal(exponenta_binary)
        exp = exponenta - IEEENumber.EXP_CONSTANT

        mantissa = IEEENumber._binary_fraction_to_decimal(mantissa_binary)
        number =  (1 + mantissa) * pow(2, exp)
        return number


    def __add__(self,other:"IEEENumber"):
        a_exponenta = self.ieee_format_number[IEEENumber.EXP_START_IDX:IEEENumber.EXP_END_IDX]
        b_exponenta = other.ieee_format_number[IEEENumber.EXP_START_IDX:IEEENumber.EXP_END_IDX]

        a_exp = IEEENumber._to_decimal(a_exponenta)
        b_exp = IEEENumber._to_decimal(b_exponenta)

        a_mantissa = self.ieee_format_number[IEEENumber.MANTISSA_START_IDX:]
        b_mantissa = other.ieee_format_number[IEEENumber.MANTISSA_START_IDX:]

        if a_exp > b_exp:
            shift = a_exp - b_exp - 1
            b_mantissa = "0" * shift + "1" + b_mantissa
            exp_bin = a_exponenta
        else:
            shift = b_exp - a_exp - 1
            a_mantissa = "0" * shift + "1" + a_mantissa
            exp_bin = b_exponenta

        max_length = max(len(a_mantissa), len(b_mantissa))
        a_mantissa = a_mantissa.ljust(max_length, "0")
        b_mantissa = b_mantissa.ljust(max_length, "0")

        summa_mantissa = IEEENumber._sum_inside(a_mantissa, b_mantissa)

        if len(summa_mantissa) > max_length:
            exp_bin = IEEENumber._sum_inside(exp_bin, "00000001")
            summa_mantissa = summa_mantissa[1:]

        result = "0 " + exp_bin + " " + summa_mantissa
        return result


    def __str__(self):
        return self.ieee_format_number
