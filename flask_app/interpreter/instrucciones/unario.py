from ..abstract.instruccion import Instruccion
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol

class Unario(Instruccion):
    def __init__(self, line, column, identificador, tipo_unario):
        self.line = line
        self.column = column
        self.identificador = identificador
        self.tipo_unario = tipo_unario

    def ejecutar(self, out, env: Enviroment):
        
        valor_variable: Symbol = env.getVariable(out, self.identificador)

        if self.tipo_unario == "++":
            new_value = valor_variable.value + 1
            env.changeVariable(out, self.identificador, valor_variable.type, new_value, self.line, self.column)
        elif self.tipo_unario == "--":
            new_value = valor_variable.value - 1
            env.changeVariable(out, self.identificador, valor_variable.type, new_value, self.line, self.column)

    def generateASM(self, out, env, generator):
        pass