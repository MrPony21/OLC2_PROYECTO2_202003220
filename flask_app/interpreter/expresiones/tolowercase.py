from ..abstract.expression import Expression
from ..entorno.types import Type
from ..entorno.symbol import Symbol 

class ToLowerCase(Expression):
    def __init__(self, line, column, exp: Expression):
        self.line = line
        self.column = column
        self.exp: Expression = exp

    def ejecutar(self, out, env):
        
        exp_sym: Symbol = self.exp.ejecutar(out, env)

        if exp_sym.type == Type.STRING:
            valor1 = exp_sym.value
            minusculas = valor1.lower()
            return Symbol(self.line, self.column, minusculas, Type.STRING)
        else:
            x = ("Error: en la funcion ToLowerCase el valor debe ser una cadena")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)


    def generateASM(self, out, env, generator):
        pass
