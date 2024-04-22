from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.enviroment import Enviroment
from ..instrucciones.sentencias import Sentencias
from ..entorno.types import Type
from ..entorno.generator import Generator
from ..instrucciones.transferencia import Transferencia

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

    #aqui tambien recibimos el label end_switch esto para poder crear los jump del break correctamente 
    #No dara error porque case es exclusivo del switch
    def generateASM(self, out, env: Enviroment, generator: Generator, end_switch):

        newEntorno = Enviroment(env, env.name+" switch")

        for inst in self.sentencias:

            transferencia = inst.generateASM(out, newEntorno, generator)

       
        if generator.break_pos != 0:
                generator.load_break(end_switch)


            
            
