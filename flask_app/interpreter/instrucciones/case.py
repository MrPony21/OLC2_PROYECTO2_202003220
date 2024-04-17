from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.enviroment import Enviroment
from ..instrucciones.sentencias import Sentencias
from ..entorno.types import Type

class Case(Instruccion):
    def __init__(self, line, column, exp: Expression, sentencias: Sentencias):
        self.line = line
        self.column = column
        self.exp = exp
        self.sentencias = sentencias


    def ejecutar(self, out, env: Enviroment):
        
        if self.exp != "default":
            exp1: Symbol = self.exp.ejecutar(out, env)
            newEntorno = Enviroment(env, env.name+"switch case:"+str(exp1.value))
        else:
            newEntorno = Enviroment(env, env.name+"switch default")
    

        for inst in self.sentencias:

            transferencia = inst.ejecutar(out, newEntorno)

            if transferencia != None:
                return transferencia

    def generateASM(self, out, env, generator):
        pass
   