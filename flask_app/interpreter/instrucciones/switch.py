from ..abstract.instruccion import Instruccion
from ..instrucciones.case import Case
from ..entorno.symbol import Symbol
from ..abstract.expression import Expression
from ..entorno.types import Type

class Switch(Instruccion):
    def __init__(self, line, column, exp: Expression, cases, default):
        self.line = line
        self.column = column
        self.exp = exp
        self.cases = cases
        self.default = default


    def ejecutar(self, out, env):

        exp_principal: Symbol = self.exp.ejecutar(out, env) 

        #Error en caso de que venga mas de un default
        cont_default = 0
        for case in self.cases:
            
            if case.exp == "default":
                cont_default +=1

        if cont_default > 1:
            x = ("Error: no puede venir mas de dos default en el switch")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return

        #Ejecucion de comparacion de la expresion del switch con la expresion del case y asi ejecutar sus sentencias o en caso de no encontrar ejecucion del default
        for case in self.cases:
            
            if case.exp != "default":

                exp_case: Symbol = case.exp.ejecutar(out, env)

                if exp_principal.value == exp_case.value and exp_principal.type == exp_case.type:

                    transferencia = case.ejecutar(out, env)

                    if transferencia != None:
                        if transferencia.type == Type.BREAK:
                            #x = ("Todo salio a la perfeccion")
                            return
                        elif transferencia.type == Type.CONTINUE:
                            x = ("Error: No puede venir la sentencia de transferencia continue dentro de un case")
                            out.addErrores(x, env.name, self.line, self.column, "Semantico")
                            return
                        elif transferencia.type == Type.RETURN:
                            return transferencia
                    
                    else:
                        x = ("Error: Hace falta un break en la sentencia switch")
                        out.addErrores(x, env.name, self.line, self.column, "Semantico")

            else:
                
                #Error en caso de que el default venga de primero
                last_default = self.cases[-1].exp == 'default'
                if (not last_default):
                    x = ("Error: El default debe ser la ultima clausula")
                    out.addErrores(x, env.name, self.line, self.column, "Semantico")
                    return

                transferencia = case.ejecutar(out, env)

                if transferencia != None:
                        if transferencia.type == Type.BREAK:
                            x = ("Error: No puede venir la sentencia de transferencia continue en el default")
                            out.addErrores(x, env.name, self.line, self.column, "Semantico")
                            return
                        elif transferencia.type == Type.CONTINUE:
                            x = ("Error: No puede venir la sentencia de transferencia continue dentro el default")
                            out.addErrores(x, env.name, self.line, self.column, "Semantico")
                            return
                        elif transferencia.type == Type.RETURN:
                            return transferencia
 
    def generateASM(self, out, env, generator):
        pass