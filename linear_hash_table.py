from dataclasses import dataclass
import json

@dataclass
class HashTableCell:
    ID: str = ""
    C: int = 0
    U: int = 0
    T: int = 0
    L: int = 0
    D: int = 0
    Po: int = -1
    Pi: str = ""
    V: int = -1
    h: int = -1

class LinearHashTable:
    def __init__(self):
        self.size = 25
        self.table = []
        for i in range(self.size):
            cell = HashTableCell()
            self.table.append(cell)
        self.num_of_occupied_cells = 0
        self.insert_list = []


    @staticmethod
    def __get_unicode_num(char):
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        char = char.upper()
        if char in alphabet:
            return alphabet.index(char) + 65
        else:
            raise ValueError(f"Invalid character: {char}")


    def __calc_num_value_for_keyword(self, keyword):
        if len(keyword) < 2 or not keyword[0].isalpha() or not keyword[1].isalpha():
            raise ValueError("Invalid keyword: A valid keyword must be at least 2 alphabetical characters long")

        let1 = keyword[0]
        let2 = keyword[1]
        a_val = LinearHashTable.__get_unicode_num('A')
        let1_value = LinearHashTable.__get_unicode_num(let1) - a_val
        let2_value = LinearHashTable.__get_unicode_num(let2) - a_val
        return let1_value * 26 + let2_value


    def __calc_hash_value(self, keyword_value, att=0):
        hash_value = keyword_value % self.size
        return hash_value


    def __linear_collision_solve(self, hash_value, step):
        result = (hash_value + step) % self.size
        return result


    def __get_init_pos(self, key):
        keyword_value = self.__calc_num_value_for_keyword(key)
        hash_value = self.__calc_hash_value(keyword_value)
        return keyword_value, hash_value, hash_value


    def find_by_key(self, key):
        keyword_value, hash_value, curr_pos = self.__get_init_pos(key)
        step = 0
        while self.table[curr_pos].U == 1:
            if self.table[curr_pos].ID == key and self.table[curr_pos].D == 0:
                print(f"Found key at position {curr_pos}: {self.table[curr_pos].Pi}")
                return self.table[curr_pos].Pi

            if self.table[curr_pos].Po == -1:
                break

            curr_pos = self.table[curr_pos].Po
            step += 1

            if step >= self.size:
                print("End of hash table reached. No key found.")
                break

        print(f"Key {key} not found.")
        return None


    def insert_new_item(self, key, data):
        key_item = self.find_by_key(key)
        if key_item is not None:
            print(f"Item with key {key} already exists:\n{key_item}")
            return

        keyword_value, hash_value, curr_pos = self.__get_init_pos(key)
        step = 0

        while self.table[curr_pos].U == 1 and self.table[curr_pos].D == 0:
            curr_pos = self.__linear_collision_solve(hash_value, step)
            step += 1
            if step >= self.size:
                print("Table is full")
                return

        self.table[curr_pos].ID = key
        self.table[curr_pos].C = 1 if step > 0 else 0
        self.table[curr_pos].U = 1
        self.table[curr_pos].T = 1
        self.table[curr_pos].L = 0
        self.table[curr_pos].D = 0
        self.table[curr_pos].Po = -1
        self.table[curr_pos].Pi = data
        self.table[curr_pos].V = keyword_value
        self.table[curr_pos].h = hash_value

        self.num_of_occupied_cells += 1

        if step > 0:
            prev_hash = hash_value
            prev_step = 0
            while self.table[prev_hash].U == 1 and prev_step < step:
                if self.table[prev_hash].Po == -1:
                    self.table[prev_hash].T = 0
                    self.table[prev_hash].Po = curr_pos
                    break
                prev_hash = self.table[prev_hash].Po
                prev_step += 1
        self.insert_list.append((key, data, keyword_value, hash_value, curr_pos))


    def update_item(self, key, data):
        key_item = self.find_by_key(key)

        if key_item is None:
            print(f"There is no item with key {key} ")
            return

        keyword_value, hash_value, curr_pos = self.__get_init_pos(key)
        step = 0
        print("New data: ", data)

        while self.table[curr_pos].U == 1:
            if self.table[curr_pos].ID == key and self.table[curr_pos].D == 0:
                self.table[curr_pos].Pi = data
                return True

            if self.table[curr_pos].Po == -1:
                break

            curr_pos = self.table[curr_pos].Po
            step += 1
            if step >= self.size:
                print("Updating warning: Table is full")
                break

        return False


    def delete_item_by_key(self, key):
        key_item = self.find_by_key(key)

        if key_item is None:
            print(f"There is no item with key {key}")
            return

        keyword_value, hash_value, curr_pos = self.__get_init_pos(key)
        step = 0

        while self.table[curr_pos].U == 1:
            if self.table[curr_pos].ID == key and self.table[curr_pos].D == 0:
                self.table[curr_pos].ID = "X"
                self.table[curr_pos].C = -1
                self.table[curr_pos].U = 0
                self.table[curr_pos].T = -1
                self.table[curr_pos].L = -1
                self.table[curr_pos].D = 1
                self.table[curr_pos].Pi = "X"
                self.table[curr_pos].V = -1
                self.num_of_occupied_cells -= 1
                return True

            if self.table[curr_pos].Po == -1:
                break

            curr_pos = self.table[curr_pos].Po
            step += 1
            if step >= self.size:
                break

        return False

    def get_fullness(self):
        return self.num_of_occupied_cells/self.size

    def __str__(self):
        output = []
        output.append(
            f"{'№':<3} {'ID':<15} {'C':<3} {'U':<3} {'T':<3} {'L':<3} {'D':<3} {'Po':<5} {'Pi':<55} {'V':<5} {'h':<5}")
        output.append("-" * 110)
        for i, cell in enumerate(self.table):
            if cell.U == 1 or cell.D == 1:
                output.append(
                    f"{i:<3} {cell.ID:<15} {cell.C:<3} {cell.U:<3} {cell.T:<3} {cell.L:<3} {cell.D:<3} {cell.Po:<5} "
                    f"{cell.Pi:<55} {cell.V:<5} {cell.h:<5}")
        output.append(f"Fullness of table: {self.get_fullness():.2f}")
        return "\n".join(output)

    @staticmethod
    def load_data(file_path):
        key_data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for key, value in data.items():
                    key_data.append((key.strip(), value.strip()))
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
        except json.JSONDecodeError as e:
            print(f"Ошибка чтения JSON: {e}")
        return key_data
