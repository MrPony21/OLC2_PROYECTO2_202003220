from ..abstract.expression import Expression
from ..entorno.types import Type
from ..entorno.symbol import Symbol

class TypeOf(Expression):
    def __init__(self, line, column, exp: Expression):
        self.line = line
        self.column = column
        self.exp = exp

    def ejecutar(self, out, env):
        
        exp_symbol: Symbol = self.exp.ejecutar(out, env)
        #primitivos
        if exp_symbol.type == Type.INTEGER:
            return Symbol(self.line, self.column, "number", Type.STRING)
        elif exp_symbol.type == Type.FLOAT:
            return Symbol(self.line, self.column, "float", Type.STRING)
        elif exp_symbol.type == Type.BOOLEAN:
            return Symbol(self.line, self.column, "boolean", Type.STRING)
        elif exp_symbol.type == Type.STRING:
            return Symbol(self.line, self.column, "string", Type.STRING)
        elif exp_symbol.type == Type.CHAR:
            return Symbol(self.line, self.column, "char", Type.STRING)
        elif exp_symbol.type == Type.NULL:
            return Symbol(self.line, self.column, "null", Type.STRING)
        elif exp_symbol.type == Type.INTERFACE:
            return Symbol(self.line, self.column, "Interface", Type.STRING)
        elif exp_symbol.type == Type.MATRIZ:
            return Symbol(self.line, self.column, "Matriz", Type.STRING)

        
        #falta agregar los compuestas

    def generateASM(self, out, env, generator):
        pass