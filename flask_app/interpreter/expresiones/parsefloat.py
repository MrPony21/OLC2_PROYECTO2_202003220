from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.types import Type
import math

class ParseFloat(Expression):
    def __init__(self, line, column, exp: Expression):
        self.line = line
        self.column = column
        self.exp = exp

    def ejecutar(self, out, env):
        
        valor_sym: Symbol = self.exp.ejecutar(out, env)

        if valor_sym.type == Type.STRING:

            try: 
                valor_parseado_float = float(valor_sym.value)
                return Symbol(self.line, self.column, valor_parseado_float, Type.FLOAT)

            except ValueError:
                x = ("Error: Cadena incompatible para convertirse a float")
                print(x)
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                return Symbol(self.line, self.column, None, Type.NULL)
        else:
            x = ("Error: no se puede parsear un ",valor_sym.type, " a float")
            print(x)
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)
        

    def generateASM(self, out, env, generator):
        pass