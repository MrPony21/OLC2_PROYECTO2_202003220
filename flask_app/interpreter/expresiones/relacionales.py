from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.types import Type

class Relacionales(Expression):
    def __init__(self, line, column, exp1: Expression, exp2: Expression, tipo_relacional):
        self.line = line
        self.column = column
        self.exp1 = exp1
        self.exp2 = exp2
        self.tipo_relacional = tipo_relacional

    def ejecutar(self, out, env):

        valor1: Symbol = self.exp1.ejecutar(out,env)
        valor2: Symbol = self.exp2.ejecutar(out,env)

        #x = ("relacionales")
        #x = ("val1: ", valor1.value, valor1.type)
        #x = ("val2: ", valor2.value, valor2.type)


        #> >= < <=
        if valor1.type == valor2.type or (valor1.type == Type.INTEGER and valor2.type == Type.FLOAT) or (valor2.type == Type.INTEGER and valor1.type == Type.FLOAT):
        
            if self.tipo_relacional == '>':
                relacional = valor1.value > valor2.value
                return Symbol(self.line, self.column, relacional, Type.BOOLEAN)
            elif self.tipo_relacional == '>=':
                relacional = valor1.value >= valor2.value
                return Symbol(self.line, self.column, relacional, Type.BOOLEAN)
            elif self.tipo_relacional == '<':
                relacional = valor1.value < valor2.value
                return Symbol(self.line, self.column, relacional, Type.BOOLEAN)
            elif self.tipo_relacional == '<=':
                relacional = valor1.value <= valor2.value
                return Symbol(self.line, self.column, relacional, Type.BOOLEAN) 

        else:
            x = ("Error: Operacion relacional no valida no se pueden comparar distintos tipos")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)

    def generateASM(self, out, env, generator):
        pass
