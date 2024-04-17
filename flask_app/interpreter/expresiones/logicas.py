from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.types import Type

class Logicas(Expression):
    def __init__(self, line, column, exp1: Expression, exp2:Expression, tipo_logico):
        self.line = line
        self.column = column
        self.exp1 = exp1
        self.exp2 = exp2 
        self.tipo_logico = tipo_logico

    def ejecutar(self, out, env):

        valor1: Symbol = self.exp1.ejecutar(out, env)
        valor2: Symbol = self.exp2.ejecutar(out, env)

        #x = ("logicas")
        #x = ("valor1: ", valor1.value, valor1.type)
        #x = ("valor2: ", valor2.value, valor2.type)
        #x = (self.tipo_logico)

        if valor1.type == Type.BOOLEAN and valor2.type == Type.BOOLEAN:
            
            if self.tipo_logico == 'and':
                valor_logico = valor1.value and valor2.value
                return Symbol(self.line, self.column, valor_logico, Type.BOOLEAN)
            elif self.tipo_logico == 'or':
                valor_logico = valor1.value or valor2.value
                return Symbol(self.line, self.column, valor_logico, Type.BOOLEAN)
            elif self.tipo_logico == 'not':
                valor_logico = not valor1.value 
                return Symbol(self.line, self.column, valor_logico, Type.BOOLEAN)

        else:
            x = ("Error: Tipo de operacion logica incompatible")
            print(x)
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)
    
    def generateASM(self, out, env, generator):
        pass