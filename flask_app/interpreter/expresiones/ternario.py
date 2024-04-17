from ..abstract.expression import Expression
from ..entorno.types import Type
from ..entorno.symbol import Symbol

class Ternario(Expression):
    def __init__(self, line, column, condicion: Expression, exp_true: Expression, exp_false: Expression):
        self.line = line
        self.column = column
        self.condicion = condicion
        self.exp_true = exp_true
        self.exp_false = exp_false

    def ejecutar(self, out, env):

        exp_condicion: Symbol = self.condicion.ejecutar(out, env)
        exp_true: Symbol = self.exp_true.ejecutar(out, env)
        exp_false: Symbol = self.exp_false.ejecutar(out, env)

        if exp_condicion.type != Type.BOOLEAN:
            x = ("Error: La condicion del ternario deberia devolver una expresion de tipo boolean")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)

        if exp_condicion.value:
            return exp_true
        else:
            return exp_false
    

    def generateASM(self, out, env, generator):
        pass