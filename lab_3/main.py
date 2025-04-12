from AOIS.lab3.models.minimisation_methods import *
from AOIS.lab_2.models.logic_table import *

if __name__ == "__main__":
    #formula="(((A & B) | (C & D)) & E)"
    formula="((A -> !B) | (C & D))"
    logic = LogicTable(formula)
    operations = logic.load_operations_from_csv("operations")
    subformulas = logic.extract_subformulas()
    header, table = logic.compute_truth_table(subformulas, operations)
    logic.print_truth_table(header, table)

    sdnf = logic.generate_sdnf(header, table)
    print("СДНФ: ", sdnf)

    sknf = logic.generate_sknf(header, table)
    print("СКНФ: ", sknf)



    print('\n\nМИНИМИЗАЦИЯ СКНФ\n\n')
    MinimisationMethods.calc_method_sknf(sknf)

    print("\n\n\nРАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД\n")
    MinimisationMethods.calc_table_method_sknf(sknf)

    print("\n\n\nМЕТОД КАРНО\n")
    MinimisationMethods.carno_sknf(sknf)



    print('\n\nМИНИМИЗАЦИЯ СДНФ\n\n')
    MinimisationMethods.calc_method_sdnf(sdnf)

    print("\n\n\nРАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД\n")
    MinimisationMethods.calc_table_method_sdnf(sdnf)

    print("\n\n\nМЕТОД КАРНО\n")
    MinimisationMethods.carno_sdnf(sdnf)
