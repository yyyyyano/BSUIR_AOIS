class BinaryNumber:
    BINARY_ZERO="0 0000000"
    MIN_NUMBER_ADDITIONAL_CODE = "1 0000001"
    MIN_NUMBER = -127
    MAX_NUMBER_ADDITIONAL_CODE = "0 1111111"
    MAX_NUMBER = 127

    @staticmethod
    def is_valid_decimal(dec_int):
        return isinstance(dec_int,int) and BinaryNumber.MIN_NUMBER <= dec_int <= BinaryNumber.MAX_NUMBER

    def __init__(self,dec_int:int):
      self.dec_int = dec_int
      self.direct_binary=self.convert_to_direct_code(dec_int)


    @staticmethod
    def _to_binary(number:int,INT_NUM_LENGTH=8)->str:
        if number == 0:
            return "0" * INT_NUM_LENGTH

        binary_num_reversed = ""
        while number / 2 != 0:
            modulo = number % 2
            binary_num_reversed += str(modulo)
            number = number // 2

        space = INT_NUM_LENGTH - len(binary_num_reversed)
        binary_num = "0" * space + binary_num_reversed[::-1]
        return binary_num


    @staticmethod
    def convert_to_direct_code(number:int)->str:
        if number >= 0:
            sign_digit = "0 "
        else:
            sign_digit = "1 "
            number = number * -1

        binary_num = BinaryNumber._to_binary(number, INT_NUM_LENGTH=7)
        return sign_digit + binary_num


    @staticmethod
    def convert_to_reversed_code(binary_number:str) -> str:  #from direct to reversed
        if binary_number[0] == "1":
            reversed_code = binary_number[0:2]
            for i in range(2, 9):
                if binary_number[i] == "1":
                    reversed_code += "0"
                else:
                    reversed_code += "1"
        else:
            reversed_code = binary_number
        return reversed_code


    @staticmethod
    def convert_to_additional_code(binary_number) -> str:  #from direct to additional
        if binary_number[0] == "0":
            additional_code = binary_number
        else:
            reversed_code = BinaryNumber.convert_to_reversed_code(binary_number)
            num = reversed_code[2:9]
            for i in range(len(num) - 1, -1, -1):
                if num[i] == "1":
                    num = num[:i] + "0" + num[i + 1:]
                else:
                    num = num[:i] + "1" + num[i + 1:]
                    break
            additional_code = reversed_code[:2] + num
        return additional_code


    @staticmethod
    def binary_int_to_decimal(binary_number:str)->int:  #direct int to dec
        sign = binary_number[0]
        direct_num_rev = binary_number[2:]
        dec_num = BinaryNumber._to_decimal(direct_num_rev)
        if sign == "1":
            dec_num *= -1
        return dec_num


    @staticmethod
    def _to_decimal(direct_num_rev):
        direct_num = direct_num_rev[::-1]
        length = len(direct_num_rev)
        dec_num = 0
        for i in range(0, length):
            dec_num += int(direct_num[i]) * 2 ** i
        return dec_num


    @staticmethod
    def additional_to_decimal(additional_code) -> int:
        if additional_code[0] == "0":
            return BinaryNumber.binary_int_to_decimal(additional_code)

        additional_code_list=list(additional_code[2:])
        for i in range(len(additional_code_list) - 1, -1, -1):
            if additional_code_list[i] == "1":
                additional_code_list[i] = "0"
                break
            else:
                additional_code_list[i] = "1"

        reversed_code = "".join(additional_code_list)
        reversed_code = "1 " + reversed_code
        direct_code = BinaryNumber.convert_to_reversed_code(reversed_code)
        decimal_num = BinaryNumber.binary_int_to_decimal(direct_code)
        return decimal_num


    @staticmethod
    def _sum_inside(first_num, second_num):
        carry = 0
        result = ""
        for i in range(len(first_num) - 1, -1, -1):
            current_sum = int(first_num[i]) + int(second_num[i]) + carry
            result = str(current_sum % 2) + result
            carry = current_sum // 2
        return result


    def __add__(self, other:"BinaryNumber"):
        first_additional_code = BinaryNumber.convert_to_additional_code(self.direct_binary)
        second_additional_code = BinaryNumber.convert_to_additional_code(other.direct_binary)

        first_num = list(first_additional_code[2:])
        second_num = list(second_additional_code[2:])
        result = BinaryNumber._sum_inside(first_num, second_num)

        sign_digit = self.direct_binary[0:2] if abs(self.dec_int) >= abs(other.dec_int) else other.direct_binary[0:2]
        additional_sum = sign_digit + result

        decimal_sum = BinaryNumber.additional_to_decimal(additional_sum)

        if decimal_sum > BinaryNumber.MAX_NUMBER:
            print(f"Out of range: {BinaryNumber.MAX_NUMBER}")

        if decimal_sum < BinaryNumber.MIN_NUMBER:
            print(f"Out of range: {BinaryNumber.MIN_NUMBER}")

        return (additional_sum,decimal_sum)


    def __sub__(self, other:"BinaryNumber"):
        other.dec_int *= -1
        other.direct_binary = BinaryNumber.convert_to_direct_code(other.dec_int)
        return self + other


    def __mul__(self, other:"BinaryNumber"):
        if self.direct_binary == BinaryNumber.BINARY_ZERO or other.direct_binary == BinaryNumber.BINARY_ZERO:
            return BinaryNumber.BINARY_ZERO

        if not BinaryNumber.is_valid_decimal(other.dec_int*self.dec_int):
            return "Multiply is out of range (-127, 127)"

        sign_digit = "0 " if (self.dec_int >= 0 and other.dec_int >= 0) or (self.dec_int < 0 and other.dec_int < 0) else "1 "

        first_num = self.direct_binary[2:]
        second_num = other.direct_binary[2:]

        result_length = len(first_num) + len(second_num)
        result = [0] * result_length

        for i in range(len(second_num) - 1, -1, -1):
            if second_num[i] == "1":
                shifted_number_array = list(map(str, first_num)) + ["0"] * (len(second_num) - 1 - i)
                shifted_number = list("".join(shifted_number_array).zfill(result_length))

            else:
                shifted_number = ["0"] * result_length

            carry = 0
            for j in range(result_length - 1, -1, -1):
                curr_sum = int(result[j]) + int(shifted_number[j] if j < len(shifted_number) else 0) + carry
                result[j] = curr_sum % 2
                carry = curr_sum // 2

        result_str = "".join(map(str, result))
        signed_result = sign_digit + result_str[7:]

        return (signed_result, BinaryNumber.binary_int_to_decimal(signed_result))


    def __truediv__(self,other:"BinaryNumber", precision: int = 10):
        if other.direct_binary == BinaryNumber.BINARY_ZERO:
            return "Error: division by zero"

        quotient = ""
        remainder = "0"

        sign_bit = "0 " if (self.direct_binary[0] == "1" and other.direct_binary[0] == "1") or (
                    self.direct_binary[0] == "0" and other.direct_binary[0] == "0") else "1 "

        dividend = self.direct_binary[2:]
        divisor = other.direct_binary[2:]

        for bit in dividend:
            remainder = remainder + bit
            remainder = remainder.lstrip("0") or "0"

            if BinaryNumber._to_decimal(remainder) >= BinaryNumber._to_decimal(divisor):
                quotient += "1"
                remainder = BinaryNumber._help_minus(remainder, divisor)
            else:
                quotient += "0"

        if remainder != "0":
            quotient += "."
            for _ in range(precision):
                remainder += "0"
                remainder = remainder.lstrip("0") or "0"

                if BinaryNumber._to_decimal(remainder) >= BinaryNumber._to_decimal(divisor):
                    quotient += "1"
                    remainder = BinaryNumber._help_minus(remainder, divisor)
                else:
                    quotient += "0"

        return (sign_bit + quotient,BinaryNumber.binary_float_to_float(sign_bit + quotient))


    @staticmethod
    def _help_minus(minuend: str, subtrahend: str) -> str:
        max_len = max(len(minuend), len(subtrahend))
        minuend = minuend.zfill(max_len)
        subtrahend = subtrahend.zfill(max_len)
        result = ["0"] * max_len
        borrow = 0

        for i in range(max_len - 1, -1, -1):
            bit1 = int(minuend[i])
            bit2 = int(subtrahend[i]) + borrow

            if bit1 < bit2:
                result[i] = str(bit1 + 2 - bit2)
                borrow = 1
            else:
                result[i] = str(bit1 - bit2)
                borrow = 0

        return "".join(result).lstrip("0") or "0"


    @staticmethod
    def _binary_fraction_to_decimal(binary_fraction: str) -> float:

        decimal_value = 0.0

        for i in range(len(binary_fraction)):
            bit = int(binary_fraction[i])
            decimal_value += bit * (1 / (2 ** (i + 1)))
        return decimal_value


    @staticmethod
    def binary_float_to_float(binary_float: str) -> float:
        is_negative = binary_float[0] == "1"
        binary_float = binary_float[1:]
        binary_float = binary_float.replace(" ", "")

        if '.' in binary_float:
            int_part, frac_part = binary_float.split('.')
        else:
            int_part, frac_part = binary_float, ""

        decimal_int_part = BinaryNumber._to_decimal(int_part) if int_part else 0

        decimal_frac_part = BinaryNumber._binary_fraction_to_decimal(frac_part) if frac_part else 0.0
        result = decimal_int_part + decimal_frac_part
        return -result if is_negative else result


    def __str__(self):
        return (f"\nDirect code: {self.direct_binary}"
                f"\nReversed code: {self.convert_to_reversed_code(self.direct_binary)}"
                f"\nAdditional code: {self.convert_to_additional_code(self.direct_binary)}")
