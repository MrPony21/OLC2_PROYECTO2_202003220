from ..abstract.instruccion import Instruccion
from ..entorno.types import Type
from ..abstract.expression import Expression
from ..entorno.out import Out
from ..entorno.symbol import Symbol
from ..entorno.enviroment import Enviroment

class Asignacion_Interface(Instruccion):
    def __init__(self, line, column, identificador, list_claves, exp1: Expression):
        self.line = line
        self.column = column
        self.identificador = identificador
        self.list_claves = list_claves
        self.exp1 = exp1

    def ejecutar(self, out: Out, env: Enviroment):
        
        var_interface = env.getVariable(out, self.identificador)
        exp_sym: Symbol = self.exp1.ejecutar(out, env)

        if var_interface.type != Type.INTERFACE:
            x = "Error: no se puede acceder al atributo una variable que no es tipo interface"
            print(x)
            out.addErrores(x, env.name, self.line, self.column, "Semantico")

        #aqui dependiendo de las claves que nos vengas sigue y como recibe siempre un diccionario sigue
        valor = var_interface
        for clave in self.list_claves:
            
            try: 
                valor = valor.value[clave]
            except KeyError:
                x = "Error: el atributo al que se quiere asignar no existe: "+ clave
                print(x)
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                return
            except TypeError:
                x = "Error: se quiere asignar a un valor de tipo null: "+clave
                print(x)
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                return Symbol(self.line, self.column, None, Type.NULL)
            
        valor.value = exp_sym.value
        valor.type = exp_sym.type
        
    def generateASM(self, out, env, generator):
        pass