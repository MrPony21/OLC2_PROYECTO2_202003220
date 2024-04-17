from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..instrucciones.declaration import Declaration
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol
from ..entorno.types import Type
from ..instrucciones.sentencias import Sentencias
from ..instrucciones.unario import Unario

class Inst_For(Instruccion):
    def __init__(self, line, column, declaracion: Declaration, condicional: Expression, unario: Unario, bloque_sentencias: Sentencias):
        self.line = line
        self.column = column
        self.declaracion = declaracion
        self.condicional = condicional
        self.unario = unario
        self.bloque_sentecias = bloque_sentencias

    def ejecutar(self, out, env: Enviroment):

        newEntorno = Enviroment(env, env.name+" FOR")

        self.declaracion.ejecutar(out, newEntorno)
        exp_condicion: Symbol = self.condicional.ejecutar(out, newEntorno)

        #esto es para verificar que la declaracion haya sido number
        var = newEntorno.getVariable(out, self.declaracion.identificador)
        if var.type != Type.INTEGER:
            x = ("Error: la declaracion del for debe ser number")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return 
        #esto es para verificar que la condicion devuelva un boolean
        if exp_condicion.type != Type.BOOLEAN:
            x = ("Error: la condicion del for debe recibir un boolean")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return

        iteracion = 0
        while True:
            
            exp_condicion: Symbol = self.condicional.ejecutar(out, newEntorno)
            if not exp_condicion.value:
                break
            
            #crear metodo clean enviroment
            transferencia = self.bloque_sentecias.ejecutar(out, newEntorno)

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

            
            self.unario.ejecutar(out, newEntorno)
            newEntorno.cleanVariables()
                
    def generateASM(self, out, env, generator):
        pass

