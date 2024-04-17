from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.types import Type

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

    def generateASM(self, out, env, generator):
        pass
