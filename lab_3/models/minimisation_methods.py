from itertools import product
from AOIS.lab_2.models.logic_table import *

class MinimisationMethods:
    @staticmethod
    def __get_formulas(big_formula):
        formulas = []
        if LogicTable.check_brackets_format(big_formula):
            formula = ''
            open_brackets = 0
            for char in big_formula:
                if char == '(':
                    if open_brackets > 0:
                        formula += char
                    open_brackets += 1
                elif char == ')':
                    open_brackets -= 1
                    if open_brackets == 0:
                        formulas.append(formula)
                        formula = ''
                    else:
                        formula += char
                else:
                    if open_brackets > 0:
                        formula += char
        else:
            print("Некорректный формат СКНФ/СДНФ")
        return formulas


    @staticmethod
    def __gluing_stage(norm_formula, formula_inter_sign):
        constituents = MinimisationMethods.__get_formulas(norm_formula)
        implicants = []
        used_constituents_idxs = set()

        for i in range(len(constituents)):
            for j in range(len(constituents)):
                if i == j:
                    continue

                implicant1 = [item.strip() for item in constituents[i].split(formula_inter_sign)]
                implicant2 = [item.strip() for item in constituents[j].split(formula_inter_sign)]

                common_elements = set(implicant1) & set(implicant2)
                differing_elements = set(implicant1) ^ set(implicant2)

                if len(common_elements) == len(implicant1) - 1 and len(differing_elements) == 2:
                    elem1, elem2 = differing_elements
                    if elem1.lstrip('!') == elem2.lstrip('!') and (elem1.startswith('!') ^ elem2.startswith('!')):
                        used_constituents_idxs.add(i)
                        used_constituents_idxs.add(j)
                        combined = formula_inter_sign.join(sorted(common_elements))
                        if combined not in implicants:
                            implicants.append(combined)
                            print(f"  Склеено: ({constituents[i]})  и ({constituents[j]})  ->  ({combined})")

        for idx, const in enumerate(constituents):
            if idx not in used_constituents_idxs:
                const = formula_inter_sign.join(sorted([item.strip() for item in const.split(formula_inter_sign)]))
                if const not in implicants:
                    implicants.append(const)

        print(f"\nИмпликанты после этапа склейки\n{implicants}\n")
        return implicants


    @staticmethod
    def __calculate_expression(expression, values):
        expression = re.sub(r'!([A-E])', lambda match: f'not {values.get(match.group(1), 0)}', expression)
        expression = re.sub(r'\b[A-E]\b', lambda match: str(values.get(match.group(0), 0)), expression)
        expression = expression.replace('&', ' and ')
        expression = expression.replace('|', ' or ')
        try:
            return int(eval(expression))
        except Exception as e:
            raise ValueError(f"Ошибка в выражении: {expression}") from e


    @staticmethod
    def __select_implicant_values(implicant, inter_sign):
        values = {}
        eq = 0 if inter_sign == '|' else 1
        literals = implicant.split(inter_sign)
        for lit in literals:
            lit = lit.strip()
            if lit.startswith('!'):
                values[lit[1:]] = not eq
            else:
                values[lit] = eq
        return values


    @staticmethod
    def __calc_method(norm_formula, inter_sign):
        constituents = MinimisationMethods.__get_formulas(norm_formula)
        if not constituents:
            print("Ошибка: конституенты не найдены")
            return
        print("Конституенты: ", constituents)

        current_implicants = constituents.copy()
        print("\nНачальные импликанты: ", current_implicants)

        while True:
            next_implicants = MinimisationMethods.__gluing_stage(inter_sign.join(f"({imp})" for imp in current_implicants),
                                                               inter_sign)
            next_implicants = sorted(set(next_implicants))
            print("Следующие импликанты после склейки: ", next_implicants)

            if set(next_implicants) == set(current_implicants):
                break
            current_implicants = next_implicants
            # print("Текущие импликанты: ", current_implicants)

        print("\nВсе импликанты после завершения склейки: ", current_implicants)

        final_implicants = []
        for implicant in current_implicants:
            values = MinimisationMethods.__select_implicant_values(implicant, inter_sign)
            updated_values = values
            result = MinimisationMethods.__calculate_expression(norm_formula, updated_values)

            if (inter_sign == '&' and result == 1) or (inter_sign == '|' and result == 0):
                final_implicants.append(implicant)

        return final_implicants


    @staticmethod
    def calc_method_sknf(norm_formula):
        final_implicants = MinimisationMethods.__calc_method(norm_formula, '|')
        sign_digits = ' & '
        final_expression = sign_digits.join(f"({imp})" for imp in final_implicants)
        print("\nТупиковая форма расчетного метода для СКНФ: ", final_expression)


    @staticmethod
    def calc_method_sdnf(norm_formula):
        final_implicants = MinimisationMethods.__calc_method(norm_formula, '&')
        sign_digits = ' | '
        final_expression = sign_digits.join(f"({imp})" for imp in final_implicants)
        print("\nТупиковая форма расчетного метода для СДНФ: ", final_expression)


    @staticmethod
    def __calc_table_method(norm_formula, inter_sign):
        constituents = MinimisationMethods.__get_formulas(norm_formula)
        if not constituents:
            print("Ошибка: конституенты не найдены")
            return

        print("Конституенты: ", constituents)

        current_implicants = constituents.copy()
        while True:
            next_implicants = MinimisationMethods.__gluing_stage(inter_sign.join(f"({c})" for c in current_implicants), inter_sign)
            next_implicants = sorted(set(next_implicants))

            if set(next_implicants) == set(current_implicants):
                break
            current_implicants = next_implicants

        print("\nВсе импликанты после склейки: ", current_implicants)

        parts_of_implicants = {}
        for imp in current_implicants:
            parts_of_implicants[imp] = set(i.strip() for i in imp.split(inter_sign))

        parts_of_constituents = {}
        for const in constituents:
            parts_of_constituents[const] = set(i.strip() for i in const.split(inter_sign))

        final_implicants = MinimisationMethods.__raschet_table(current_implicants, parts_of_implicants, parts_of_constituents)
        return final_implicants


    @staticmethod
    def __raschet_table(current_implicants, parts_of_implicants, parts_of_constituents):
        coverage_table = {imp: [] for imp in current_implicants}
        for imp, imp_literals in parts_of_implicants.items():
            for const, const_literals in parts_of_constituents.items():
                if imp_literals.issubset(const_literals):
                    coverage_table[imp].append(const)

        print("\nТаблица покрытия:")
        header = [" " * 15] + list(parts_of_constituents.keys())
        print("".join(col.center(18) for col in header))
        for imp in current_implicants:
            row = [imp.ljust(15)]
            for const in parts_of_constituents:
                row.append("+" if const in coverage_table[imp] else " ")
            print("".join(cell.center(18) for cell in row))

        final_implicants = []
        for imp, covered in coverage_table.items():
            other_coverage = set()
            for other_imp, other_covered in coverage_table.items():
                if other_imp != imp:
                    other_coverage.update(other_covered)
            if not set(covered).issubset(other_coverage):
                final_implicants.append(imp)

        return final_implicants


    @staticmethod
    def calc_table_method_sknf(norm_formula):
        final_implicants = MinimisationMethods.__calc_table_method(norm_formula, '|')
        sign_digits = ' & '
        final_expression = sign_digits.join(f"({imp})" for imp in final_implicants)
        print("\nТупиковая форма расчетно-табличного метода для СКНФ: ", final_expression)


    @staticmethod
    def calc_table_method_sdnf(norm_formula):
        final_implicants = MinimisationMethods.__calc_table_method(norm_formula, '&')
        sign_digits = ' | '
        final_expression = sign_digits.join(f"({imp})" for imp in final_implicants)
        print("\nТупиковая форма расчетно-табличного метода для СДНФ: ", final_expression)


    @staticmethod
    def __get_implicant_combinations(imp, all_vars, inter_sign):
        eq = 0 if inter_sign == '|' else 1
        values = imp.split(inter_sign)
        fixed = {}
        for val in values:
            val = val.strip()
            if val.startswith('!'):
                var = val[1:]
                fixed[var] = 1 - eq
            else:
                var = val
                fixed[var] = eq
        free_vars = [v for v in all_vars if v not in fixed]
        combinations = []
        for values in product([0, 1], repeat=len(free_vars)):
            point = {var: val for var, val in zip(free_vars, values)}
            point.update(fixed)
            combinations.append(tuple(point[v] for v in all_vars))
        return combinations


    @staticmethod
    def __generate_gray_code(num):
        if num == 0:
            return []
        result = []
        for i in range(2 ** num):
            gray = i ^ (i >> 1)
            result.append(gray)
        return result


    @staticmethod
    def __get_group(x, y, h, w, table):
        rows=len(table)
        cols=len(table[0])
        coords = []
        for dy in range(h):
            for dx in range(w):
                ny = (y + dy) % rows
                nx = (x + dx) % cols
                if not table[ny][nx]:
                    return None
                coords.append((ny, nx))
        return coords


    @staticmethod
    def __find_fixed_vars(group, row_values, col_values):
        cells = [(*row_values[row], *col_values[col]) for row, col in group]
        merged = cells[0]
        for cell in cells[1:]:
            merged = tuple(a if a == b else None for a, b in zip(merged, cell))
        return merged


    @staticmethod
    def __minimise_carno(points,num_of_rows,num_of_cols):
        row_values = [BinaryNumber.to_binary(i, num_of_rows) for i in MinimisationMethods.__generate_gray_code(num_of_rows)]
        col_values = [BinaryNumber.to_binary(i, num_of_cols) for i in MinimisationMethods.__generate_gray_code(num_of_cols)]

        table = [[(*row, *col) in points for col in col_values] for row in row_values]
        visited = [[False] * len(col_values) for _ in row_values]

        values_combinations = []
        for h in [32, 16, 8, 4, 2, 1]:
            for w in [32, 16, 8, 4, 2, 1]:
                for y in range(len(table)):
                    for x in range(len(table[0])):
                        group = MinimisationMethods.__get_group(x, y, h, w, table)
                        if group and not all(visited[row][col] for row, col in group):
                            for row, col in group:
                                visited[row][col] = True
                            vals_comb = MinimisationMethods.__find_fixed_vars(group, row_values, col_values)
                            values_combinations.append(vals_comb)
        return values_combinations


    @staticmethod
    def __generate_implicant(value_combination, vars, inter_sign):
        parts = []
        for val, name in zip(value_combination, vars):
            if val is None:
                continue
            if (val == 1 and inter_sign == '&') or (val == 0 and inter_sign == '|'):
                parts.append(name)
            else:
                parts.append(f"!{name}")
        sign_digits = ' ' + inter_sign + ' '
        return f"({sign_digits.join(parts)})"


    @staticmethod
    def __carno_method(norm_formula, inter_sign):
        print("Начальная формула: ", norm_formula)
        eq = 0 if inter_sign == '|' else 1
        implicants = MinimisationMethods.__get_formulas(norm_formula)
        variables = sorted(set(var.strip('!') for imp in implicants for var in imp.replace(inter_sign, ' ').split()))
        num_of_vars = len(variables)
        if num_of_vars > 5:
            print("Таблица Карно работает до 5 переменных")
            return

        points = set()
        for imp in implicants:
            points.update(MinimisationMethods.__get_implicant_combinations(imp, variables, inter_sign))
        working_points = points

        row_vars = variables[:num_of_vars // 2]
        col_vars = variables[num_of_vars // 2:]
        num_of_rows = len(row_vars)
        num_of_cols = len(col_vars)
        row_values = [BinaryNumber.to_binary(i, num_of_rows) for i in MinimisationMethods.__generate_gray_code(num_of_rows)]
        col_values = [BinaryNumber.to_binary(i, num_of_cols) for i in MinimisationMethods.__generate_gray_code(num_of_cols)]
        table = [[(*row, *col) for col in col_values] for row in row_values]

        print("\nТаблица Карно:")
        print("    | " + " | ".join("".join(map(str, col)) for col in col_values))
        print("-" * (len(col_values) * 6 + 6))

        for i, row in enumerate(table):
            row_label = "".join(map(str, row_values[i]))
            row_vals = []
            for cell in row:
                if (eq == 1 and cell in working_points) or (eq == 0 and cell not in working_points):
                    row_vals.append("1")
                else:
                    row_vals.append("0")
            print(f"{row_label} | " + " | ".join(row_vals))

        combinations = MinimisationMethods.__minimise_carno(working_points,num_of_rows,num_of_cols)
        prefinal_implicants = []
        for comb in combinations:
            if any(i is not None for i in comb):
                implicant = MinimisationMethods.__generate_implicant(comb, variables, inter_sign)
                prefinal_implicants.append(implicant)
        prefinal_form = " | ".join(prefinal_implicants) if inter_sign == '&' else " & ".join(prefinal_implicants)
        final_form = LogicTable.check_same(prefinal_form, inter_sign)
        final_form = " | ".join(f"({imp})" for imp in final_form) if inter_sign == '&' else " & ".join(
            f"({imp})" for imp in final_form)
        return final_form


    @staticmethod
    def carno_sknf(norm_formula):
        print("\nТупиковая форма по Карно для СКНФ: ",MinimisationMethods.__carno_method(norm_formula, '|'))


    @staticmethod
    def carno_sdnf(norm_formula):
        print("\nТупиковая форма по Карно для СДНФ: ",MinimisationMethods.__carno_method(norm_formula, '&'))

