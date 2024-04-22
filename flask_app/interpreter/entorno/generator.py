class Generator:
    def __init__(self):
        self.temporal = 0x10000000
        self.label = 0
        self.msg = 0
        self.code = []
        self.finalcode = []
        self.data = []
        self.break_pos = []
        self.continue_pos = []
        self.return_pos = []
        self.natives = []
        self.funcode = []
        self.tempList = []
        self.PrintStringFlag = True
        self.ConcatStringFlag = True
        self.BreakLabel = ""
        self.ContinueLabel = ""
        self.MainCode = False

    def get_code(self):
        return self.code
    
    def get_final_code(self):
        self.add_data_boolean()
        self.add_headers()
        self.add_footers()
        self.add_data()
        outstring = "".join(self.code)
        return outstring

    def get_temps(self):
        return self.tempList
    
    def add_code(self, code):
        self.code.append(code)

    def new_temp(self):
        self.temporal += 4
        return self.temporal
    
    def new_label(self):
        temp = self.label
        self.label += 1
        return "L"+str(temp)
    
    def write_label(self, label):
        self.code.append(f'{label}:\n')
    
    def add_br(self):
        self.code.append('\n')

    def add_li(self, left, right):
        self.code.append(f"\tli {left}, {right}\n")

    def add_la(self, left, right):
        self.code.append(f'\tla {left}, {right}\n')

    def add_lw(self, left, right):
        self.code.append(f"\tlw {left}, {right}\n")

    def add_sw(self, left, right):
        self.code.append(f"\tsw {left}, {right}\n")

    def add_operation(self, operation, reg, left, right):
        self.code.append(f"\t{operation} {reg}, {left}, {right}\n")

    def add_xor(self, reg1, reg2, reg3):
        self.code.append(f'\txor {reg1}, {reg2}, {reg3}\n')

    def add_jump(self, label):
        self.code.append(f'\tj {label}\n')

    #añadir el jump de las sentencias de transferencias
    def add__break_pos(self):
        self.break_pos.append(len(self.code))

    def load_break(self, label):
        incremento = 0
        for pos in self.break_pos:
            self.code.insert(pos+incremento, f'\tj {label}\n')
            incremento += 1
        self.break_pos = []

    def add_continue_pos(self):
        self.continue_pos.append(len(self.code))

    def load_continue(self, label):
        incremento = 0
        for pos in self.continue_pos:
            self.code.insert(pos, f'\tj {label}\n')
            incremento += 1
        self.continue_pos = []

    def add_ecall(self):
        self.code.append(f"\tecall\n")

    def add_headers(self):
        self.code.insert(0,'.globl _start\n_start:\n\n')

    def add_footers(self):
        self.code.append('\n\tli a0, 0\n')
        self.code.append('\tli a7, 10\n')
        self.code.append('\tecall\n') 

    def add_data(self):
        self.code.append('\n.data\n')
        
        for dat in self.data:
            self.code.append(str(dat)+"\n")

    def add_data_boolean(self):
        self.data.append('true: .string " True"')
        self.data.append('false: .string " False"')

    def add_section_data(self, name, type, value):
        self.data.append(f'{name}: .{type} {value}')

    def new_msg(self):
        self.msg += 1
        return "msg"+str(self.msg)
    
    def add_coment(self, comentario):
        self.code.append(f'#{comentario}\n')
        
