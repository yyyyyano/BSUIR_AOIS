from AOIS.lab_2.models.logic_table import *
from AOIS.lab_1.models.binary_number import to_decimal

class DiagonalMatrix:
    operations=LogicTable.load_operations_from_csv()

    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.matrix=[]
        for i in range(rows):
            row=[]
            for j in range(cols):
                row.append(0)
            self.matrix.append(row)

    def read_word(self,word_index):
        column=[]
        for i in range(self.rows):
            element=self.matrix[i][word_index]
            column.append(element)
        word=column[word_index:]+column[:word_index]
        return word

    def write_word(self,word_index,word):
        if len(word)!=self.rows:
            print("Некорректная длина слова")
            return
        write_word=word[-word_index:] + word[:-word_index]
        for i in range(self.rows):
            self.matrix[i][word_index]=write_word[i]

    def read_address_column(self,col_idx):
        result=[]
        for col in range(self.cols):
            row=(col_idx+col)%self.rows
            result.append(self.matrix[row][col])
        return result

    def write_address_column(self,col_idx,address):
        if len(address)!=self.rows or len(address)!=self.cols:
            print("Некорректная длина адресного столбца")
            return
        for col in range(self.cols):
            row=(col_idx+col)%self.rows
            self.matrix[row][col]=address[col]

    def logic_disjunction(self, word1:list, word2:list):  #f7
        result = []
        disjunction_table = self.operations.get("DISJUNCTION", [])
        if not disjunction_table:
            raise ValueError("Таблица DISJUNCTION не загружена или отсутствует.")

        for a, b in zip(word1, word2):
            match = next((entry for entry in disjunction_table if entry["A"] == a and entry["B"] == b), None)
            if match is None:
                raise ValueError(f"Нет подходящей строки в таблице для A={a}, B={b}")
            result.append(match["Result"])
        return result

    def logic_disjunction_negation(self, word1, word2): #f8
        disjunction = self.logic_disjunction(word1, word2)
        return self.__logic_negation_word(disjunction)

    def __logic_negation_word(self,word):
        negation_table = self.operations.get("NEGATION", [])
        if not negation_table:
            raise ValueError("Таблица NEGATION не загружена или отсутствует.")

        result = []
        for val in word:
            match = next((entry for entry in negation_table if entry["A"] == val), None)
            if match is None:
                raise ValueError(f"Нет подходящей строки в таблице NEGATION для A={val}")
            result.append(match["Result"])
        return result

    def logic_first_arg_ban(self,word1,word2):
        neg_word2=self.__logic_negation_word(word2)
        conjunction_table = self.operations.get("CONJUNCTION", [])
        if not conjunction_table:
            raise ValueError("Таблица CONJUNCTION не загружена или отсутствует.")
        result=[]
        for a, b in zip(word1, neg_word2):
            match = next((entry for entry in conjunction_table if entry["A"] == a and entry["B"] == b), None)
            if match is None:
                raise ValueError(f"Нет подходящей строки в таблице для A={a}, B={b}")
            result.append(match["Result"])
        return result

    def logic_implic_from1_to2(self,word1,word2):
        neg_word1=self.__logic_negation_word(word1)
        return self.logic_disjunction(neg_word1,word2)

    def search_in_range(self,lower_bound,upper_bound):
        word_flag_pairs=[]
        for i in range(self.rows):
            word=self.read_word(i)
            word_flag_pairs.append((word,1))

        lower_pairs=self.__find_lower(word_flag_pairs,lower_bound)
        final_pairs=self.__find_upper(lower_pairs,upper_bound)
        print("\nСлова, попавшие в указанный интервал:")
        for i,(word, flag) in enumerate(final_pairs):
            if flag == 1:
                print("Слово #",i,": ", word)

    def __find_lower(self, word_flag_pairs, lower_bound):
        low = ''.join(str(bit) for bit in lower_bound)
        lower_num = BinaryNumber.to_decimal(low)
        updated_pairs = []
        for i,(word, flag) in enumerate(word_flag_pairs):
            binary_str = ''.join(str(bit) for bit in word)
            dec_value = BinaryNumber.to_decimal(binary_str)
            if dec_value < lower_num:
                updated_pairs.append((word, 0))
            else:
                updated_pairs.append((word, flag))
        return updated_pairs

    def __find_upper(self, word_flag_pairs, upper_bound):
        up = ''.join(str(bit) for bit in upper_bound)
        upper_num = BinaryNumber.to_decimal(up)
        updated_pairs = []
        for i, (word, flag) in enumerate(word_flag_pairs):
            binary_str = ''.join(str(bit) for bit in word)
            dec_value = BinaryNumber.to_decimal(binary_str)
            if dec_value > upper_num:
                updated_pairs.append((word, 0))
            else:
                updated_pairs.append((word, flag))
        return updated_pairs

    @staticmethod
    def binary_str_to_list(s):
        return [int(ch) for ch in s]

    @staticmethod
    def list_to_binary_str(bits):
        return ''.join(str(b) for b in bits)

    def add_fields_by_key(self, key_v):
        if len(key_v) != 3:
            raise ValueError("Ключ V должен быть длиной 3 бита")

        for i in range(self.rows):
            word = self.read_word(i)
            word_str = ''.join(str(b) for b in word)

            v_bits = word_str[0:3]
            if v_bits != key_v:
                continue

            a_bits = word_str[3:7]
            b_bits = word_str[7:11]
            s_bits = word_str[11:16]

            a_val = BinaryNumber.to_decimal(a_bits)
            b_val = BinaryNumber.to_decimal(b_bits)

            sum_val = (a_val + b_val) % 32

            new_s_bits = [int(bit) for bit in BinaryNumber.to_binary(sum_val, 5)]

            v_bits_list = [int(bit) for bit in v_bits]
            a_bits_list = [int(bit) for bit in a_bits]
            b_bits_list = [int(bit) for bit in b_bits]

            new_word_list = v_bits_list + a_bits_list + b_bits_list + new_s_bits

            self.write_word(i, new_word_list)
            print(f"Обновлено слово #{i}: {word_str} → {''.join(str(b) for b in new_word_list)}")

    def __str__(self):
        result = "\nМатрица:\n"
        for row in self.matrix:
            result += " ".join(map(str, row)) + "\n"
        return result



