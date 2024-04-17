from ..abstract.expression import Expression
from ..entorno.types import Type
from ..entorno.symbol import Symbol

class ToString(Expression):
    def __init__(self, line, column, exp: Expression):
        self.line = line
        self.column = column
        self.exp = exp

    def ejecutar(self, out, env):
        
        #DA ERROR AL SUMAR DOS TOSTRING
        valor_sym: Symbol = self.exp.ejecutar(out, env)

        valor_string = str(valor_sym.value)
        return Symbol(self.line, self.column, valor_string, Type.STRING)
        

    def generateASM(self, out, env, generator):
        pass