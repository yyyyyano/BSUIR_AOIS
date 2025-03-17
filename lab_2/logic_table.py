from AOIS.lab_2.imports import *

class LogicTable:
    variables = ('A', 'B', 'C', 'D', 'E')
    binary_operations={'&': 'CONJUNCTION', '|': 'DISJUNCTION', '->': 'IMPLICATION', '~': 'EQUIVALENCE'}
    unary_operation={'!': 'NEGATION'}


    def __init__(self, function):
        self.function = function


    @staticmethod
    def __check_brackets_format(function)->bool:
        stack=[]
        for char in function:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return len(stack)==0


    def extract_subformulas(self):
        try:
            function=self.function.replace(' ','')

            if not self.__check_brackets_format(function):
                raise Exception('Invalid brackets format')

            subformulas=set()
            stack=[]
            subformula_pos={}

            for i,char in enumerate(function):
                if char=='(':
                    stack.append(i)
                elif char==')':
                    if stack:
                        start=stack.pop()
                        subformula_pos[start]=i

            sorted_positions=sorted(subformula_pos.items())

            for start,end in sorted_positions:
                subformula=function[start:end+1]
                subformulas.add(subformula)

                if start>0 and function[start-1]=='!':
                    subformulas.add('!'+subformula)

            for var in self.variables:
                if var in function:
                    subformulas.add(var)

            for match in re.finditer(r'!([A-E])',function):
                subformulas.add(match.group())

            return sorted(subformulas, key=len)
        except Exception as e:
            print(f"Error: {e}")


    @staticmethod
    def __remove_ext_brackets(subformula):
        while subformula.startswith('(') and subformula.endswith(')'):
            count=0
            for i,char in enumerate(subformula):
                if char =='(':
                    count+=1
                elif char==')':
                    count-=1
                if count==0 and i==len(subformula)-1:
                    return subformula[1:-1]
        return subformula


    @staticmethod
    def __find_main_operator(subformula):
        stack=[]
        operators=['->','|','&','~']
        i=0
        while i<len(subformula):
            char=subformula[i]
            if char=='(':
                stack.append('(')
            elif char == ')':
                stack.pop()

            if (subformula[i:i+2]=='->'or subformula[i] in operators) and not stack:
                if subformula[i:i+2]=='->':
                    return '->',i
                return subformula[i],i
            i+=1
        return None,None


    @staticmethod
    def __split_subformula(subformula):
        subformula=LogicTable.__remove_ext_brackets(subformula)
        operator,pos=LogicTable.__find_main_operator(subformula)

        if not operator:
            return subformula,None,''

        left=subformula[:pos]
        right=subformula[pos+len(operator):]
        return left,operator,right


    @staticmethod
    def load_operations_from_csv(directory='operations'):
        operations={}
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                op_name=filename[:-4]
                operations[op_name]=[]

                with open(os.path.join(directory,filename),'r') as file:
                    reader=csv.DictReader(file)
                    for row in reader:
                        operations[op_name].append({
                            "A": int(row["A"]),
                            "B": int(row.get("B", 0)),
                            "Result": int(row["Result"])
                        })
        return operations


    @staticmethod
    def generate_truth_table(variables):
        return list(itertools.product([0,1],repeat=len(variables)))


    def evaluate_subformula(self,subformula,operations,row):
        left,operator,right=LogicTable.__split_subformula(subformula)

        if subformula.startswith('!'):
            operand=subformula[1:]
            if operand not in row:
                return None

            result=[
                entry["Result"]
                for entry in operations["NEGATION"]
                if entry["A"]==row[operand]
            ]
            return result[0] if result else None

        for op, op_name in self.binary_operations.items():
            if op in subformula and op==operator:
                if left not in row or right not in row:
                    return None

                subformula_table = operations[op_name]
                result = [
                    entry["Result"]
                    for entry in subformula_table
                    if entry["A"] == row[left] and entry["B"] == row[right]
                ]
                return result[0] if result else None

        return row.get(subformula,None)


    def compute_truth_table(self, subformulas,operations):
        vars=sorted(set(filter(lambda x: x in self.variables,subformulas)))
        truth_table=self.generate_truth_table(vars)

        header=vars+[subf for subf in subformulas if subf not in vars]
        table=[]

        for combination in truth_table:
            row={var: val for var, val in zip(vars, combination)}
            computed=set()

            while len(computed)< len(subformulas):
                for subformula in subformulas:
                    if subformula in computed:
                        continue

                    dependencies=re.findall(r'[A-E]|\(!?[A-E]\)|\((.*?)\)', subformula)
                    dependencies=[d for d in dependencies if d in subformulas and d!=subformula]

                    if all(dep in computed for dep in dependencies):
                        row[subformula]=self.evaluate_subformula(subformula,operations,row)
                        computed.add(subformula)

            table.append(row)
        return header,table


    @staticmethod
    def print_truth_table(header,table):
        col_widths = [max(len(str(row[col])) if col in row else len(str(col))
                          for row in table + [dict((col, col) for col in header)])
                      for col in header]

        header_row = " | ".join(f"{col:^{col_width}}" for col, col_width in zip(header, col_widths))
        print(header_row)
        print("-" * len(header_row))

        for row in table:
            row_str = " | ".join(
                f"{str(row.get(col, '')):^{col_width}}" for col, col_width in zip(header, col_widths)
            )
            print(row_str)


    def generate_sdnf(self,header,table):
        sdnf_terms=[]
        for row in table:
            if row[header[-1]]==1:
                literals=[]
                for var in header[:-1]:
                    if var in self.variables:
                        if row[var]==1:
                            literals.append(var)
                        else:
                            literals.append(f"!{var}")
                sdnf_terms.append(f"({' & '.join(literals)})")

        if sdnf_terms:
            return ' | '.join(sdnf_terms)
        return '0'


    def generate_sknf(self,header,table):
        sknf_terms=[]
        for row in table:
            if row[header[-1]]==0:
                literals=[]
                for var in header[:-1]:
                    if var in self.variables:
                        if row[var]==0:
                            literals.append(var)
                        else:
                            literals.append(f"!{var}")
                sknf_terms.append(f"({' | '.join(literals)})")

        if sknf_terms:
            return " & ".join(sknf_terms)
        return '1'


    @staticmethod
    def get_idx_form(table):
        idx_form=""
        for row in table:
            idx_form+=str(row[list(row.keys())[-1]])
        decimal=BinaryNumber.to_decimal(idx_form)
        return (decimal,idx_form)


    @staticmethod
    def get_num_form(table):
        sknf_tuple=()
        sdnf_tuple=()
        for idx,row in enumerate(table):
            value=row[list(row.keys())[-1]]
            if value==0:
                sknf_tuple+=(idx,)
            elif value==1:
                sdnf_tuple+=(idx,)
        return str(sknf_tuple)+' &', str(sdnf_tuple)+'|'
