from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.types import Type
from ..entorno.out import Out
from ..entorno.symbol import Symbol

class AccederInterface(Expression):
    def __init__(self, line, column, acceder_exp: Expression, list_claves):
        self.line = line
        self.column = column
        self.acceder_exp = acceder_exp
        self.list_claves = list_claves

    def ejecutar(self, out: Out, env: Enviroment):

        var_interface = self.acceder_exp.ejecutar(out, env)

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
                x = "Error: el atributo al que se quiere acceder no existe: "+clave
                print(x)
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                return Symbol(self.line, self.column, None, Type.NULL)
            except TypeError:
                x = "Error: se quiere acceder a un valor de tipo null: "+clave
                print(x)
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                return Symbol(self.line, self.column, None, Type.NULL)
       

        return Symbol(self.line, self.column, valor.value, valor.type)
        
    def generateASM(self, out, env, generator):
        pass    


