from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment

class Sentencias(Instruccion):
    def __init__(self, line, column ,code: Instruccion):
        self.line = line
        self.column = column
        self.code = code

    def ejecutar(self, out, env_actual):
        

        for inst in self.code:
            transfer = inst.ejecutar(out, env_actual)
            
            if transfer != None:
                return transfer
            

    def generateASM(self, out, env, generator):
        pass


    