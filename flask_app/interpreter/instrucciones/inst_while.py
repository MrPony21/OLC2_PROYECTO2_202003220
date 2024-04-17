from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol
from .sentencias import Sentencias
from ..entorno.types import Type
from ..entorno.enviroment import Enviroment

class Inst_While(Instruccion):
    def __init__(self, line, column, condicion: Expression, bloque_sentencias: Sentencias ):
        self.line = line
        self.column = column
        self.condicion = condicion
        self.bloque_sentencias = bloque_sentencias

    def ejecutar(self, out, env: Enviroment):
        
        exp_condicion: Symbol = self.condicion.ejecutar(out, env)
        newEntorno = Enviroment(env, env.name+" While")

        if exp_condicion.type != Type.BOOLEAN:
            x = ("Error: la condicion del while debe recibir un boolean")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return
        
        iteracion = 0
        while True:
            
            exp_condicion = self.condicion.ejecutar(out, env)
            if not exp_condicion.value:
                break
                
            transferencia = self.bloque_sentencias.ejecutar(out, newEntorno)

            # esto es por si es un bucle infinito
            if iteracion == 150:
                x = ("Error: Se ha entrado a un bucle infinito")
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                break
            iteracion += 1


            if transferencia != None:
                if transferencia.type == Type.BREAK:
                    break
                elif transferencia.type == Type.CONTINUE:
                    continue
                elif transferencia.type == Type.RETURN:
                    return transferencia

    def generateASM(self, out, env, generator):
        pass
    


            

            
