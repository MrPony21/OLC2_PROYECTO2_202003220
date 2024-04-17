from ..abstract.instruccion import Instruccion
from ..instrucciones.sentencias import Sentencias
from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.types import Type
from ..entorno.enviroment import Enviroment

class IfElse(Instruccion):
    def __init__(self, line, column, condicion: Expression, bloque_sentencias: Sentencias, else_sentencias: Sentencias):
        self.line = line
        self.column = column
        self.condicion = condicion
        self.bloque_sentencias = bloque_sentencias
        self.else_sentencias = else_sentencias

    def ejecutar(self, out, env: Enviroment):
        
        exp_condicion: Symbol = self.condicion.ejecutar(out, env)

        if exp_condicion.type != Type.BOOLEAN:
            x = ("Error: la condicion del if debe recibir un boolean")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return
        
        if exp_condicion.value:
            newEntorno = Enviroment(env, env.name+" If")

            transferencia = self.bloque_sentencias.ejecutar(out, newEntorno)
            if transferencia != None:
                if transferencia.type == Type.BREAK:
                    return Symbol(self.line, self.column, None, Type.BREAK)
                elif transferencia.type == Type.CONTINUE:
                    return Symbol(self.line, self.column, None, Type.CONTINUE)
                elif transferencia.type == Type.RETURN:
                    return transferencia


        else:

            if self.else_sentencias != None:
                newEntorno = Enviroment(env, env.name+" Else")

                if isinstance(self.else_sentencias, Sentencias):
                   transferencia = self.else_sentencias.ejecutar(out, newEntorno)
                elif isinstance(self.else_sentencias, IfElse):
                   transferencia = self.else_sentencias.ejecutar(out, env)
                
                if transferencia != None:
                    if transferencia.type == Type.BREAK:
                        return Symbol(self.line, self.column, None, Type.BREAK)
                    elif transferencia.type == Type.CONTINUE:
                        return Symbol(self.line, self.column, None, Type.CONTINUE)
                    elif transferencia.type == Type.RETURN:
                        return transferencia

    def generateASM(self, out, env, generator):
        pass


