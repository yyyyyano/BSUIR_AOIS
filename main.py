from AOIS.lab_2.models.logic_table import *


formula = "((A | B) & !C)"
logic=LogicTable(formula)
operations = logic.load_operations_from_csv("operations")
subformulas = logic.extract_subformulas()
header, table = logic.compute_truth_table(subformulas, operations)
logic.print_truth_table(header, table)

sdnf = logic.generate_sdnf(header, table)
print("PDNF: ", sdnf)

sknf = logic.generate_sknf(header, table)
print("PCNF: ", sknf)

print(f"Index form: {logic.get_idx_form(table)[0]} - [{logic.get_idx_form(table)[1]}]")
print(f"Number form: {logic.get_num_form(table)[0]}\n             {logic.get_num_form(table)[1]}")

#formula = "((!(!A&B)->C)|(C~D))"