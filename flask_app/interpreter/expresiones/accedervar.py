from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment

class Accedervar(Expression):
    def __init__(self,line ,column, identificador):
        self.line = line
        self.column = column
        self.identificador = identificador

    def ejecutar(self, out, env: Enviroment):
        
        variable_sym = env.getVariable(out, self.identificador)

        return variable_sym

    def generateASM(self, out, env, generator):
        pass

