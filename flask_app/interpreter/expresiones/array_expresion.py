from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.types import Type

class Array_expresion(Expression):
    def __init__(self, line, column, list_expresion):
        self.line = line
        self.column = column
        self.list_expresion = list_expresion

    def ejecutar(self, out, env):
        
        if self.list_expresion == None:
            return None

        arr = []

        for exp in self.list_expresion:
            sym: Symbol = exp.ejecutar(out, env)
            arr.append(sym)

        return Symbol(self.line, self.column, arr, Type.ARRAY)


    def generateASM(self, out, env, generator):
        pass