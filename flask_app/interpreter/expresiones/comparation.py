from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.types import Type
from ..entorno.asmbol import Asmbol
from ..entorno.generator import Generator

class Comparation(Expression):
    def __init__(self, line, column, exp1: Expression, exp2: Expression, tipo_comparacion):
        self.line = line
        self.column = column
        self.exp1 = exp1
        self.exp2 = exp2
        self.tipo_comparacion = tipo_comparacion

    def ejecutar(self, out, env):
        
        op1: Symbol = self.exp1.ejecutar(out, env) 
        op2: Symbol = self.exp2.ejecutar(out, env)

        if op1.type == op2.type or (op1.type == Type.INTEGER and op2.type == Type.FLOAT) or (op2.type == Type.INTEGER and op1.type == Type.FLOAT):
            
            if self.tipo_comparacion == "igualdad":
                valor_bool = (op1.value == op2.value)
                return Symbol(self.line, self.column, valor_bool, Type.BOOLEAN)
            if self.tipo_comparacion == "noigual":
                valor_bool = (op1.value != op2.value)
                return Symbol(self.line, self.column, valor_bool, Type.BOOLEAN)

        else:
            print("Error: Comparacion no valida no se pueden comparar distintos tipos")
            out.addErrores("Error: Comparacion no valida no se pueden comparar distintos tipos", env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)

    def generateASM(self, out, env, generator: Generator):
        
        op1: Asmbol = self.exp1.generateASM(out, env, generator)
        op2: Asmbol = self.exp2.generateASM(out, env, generator)

        generator.add_br()
        generator.add_li('t3', str(op1.valuePos))
        generator.add_lw('t1', '0(t3)')
        generator.add_li('t3', str(op2.valuePos))
        generator.add_lw('t2', '0(t3)')
        temp = generator.new_temp()
        #primero vamos a generar la comparacion y obtener un nuevo label
        new_label = generator.new_label()
        new_label2 = generator.new_label()
        new_label_final = generator.new_label()

        #beq
        if self.tipo_comparacion == "igualdad":
            valor_bool = (op1.value == op2.value)

            generator.add_operation('beq', 't1', 't2', str(new_label))
            generator.add_jump(str(new_label2))


        #bne
        if self.tipo_comparacion == "noigual":
            valor_bool = (op1.value != op2.value)

            generator.add_operation('bne', 't1', 't2', str(new_label))
            generator.add_jump(str(new_label2))


        #por si se cumple
        generator.write_label(str(new_label))
        generator.add_li('t0', str(1))
        generator.add_li('t3', str(temp))
        generator.add_sw('t0', '0(t3)')
        generator.add_jump(str(new_label_final))

        #aqui generamos por si no se cumple
        generator.write_label(str(new_label2))
        generator.add_li('t0', str(0))
        generator.add_li('t3', str(temp))
        generator.add_sw('t0', '0(t3)')

        generator.write_label(str(new_label_final))
        
        if valor_bool:
            valor = 1
        else:
            valor = 0

        return Asmbol(str(temp), valor, Type.BOOLEAN, False)
