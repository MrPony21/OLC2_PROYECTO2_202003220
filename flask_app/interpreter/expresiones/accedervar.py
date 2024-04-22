from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.asmvar import Asmvar
from ..entorno.asmbol import Asmbol

class Accedervar(Expression):
    def __init__(self,line ,column, identificador):
        self.line = line
        self.column = column
        self.identificador = identificador

    def ejecutar(self, out, env: Enviroment):
        
        variable_sym = env.getVariable(out, self.identificador)

        return variable_sym

    def generateASM(self, out, env: Enviroment, generator):
        
        variable_asym: Asmvar = env.getVariableASM(self.identificador)

        print(variable_asym)
        new_asymbol = Asmbol(variable_asym.valuepos, variable_asym.value, variable_asym.type, False)
    
        return new_asymbol



