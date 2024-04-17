from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.types import Type
from ..entorno.out import Out
from ..entorno.symbol import Symbol

class AccederMatriz(Expression):
    def __init__(self, line, column, acceder_exp: Expression, list_index):
        self.line = line
        self.column = column
        self.acceder_exp = acceder_exp
        self.list_index = list_index

    def ejecutar(self, out, env):
        
        new_list_index = []
        for value in self.list_index:
            new_list_index.append(value.ejecutar(out,env).value)


        valor_matriz = self.acceder_exp.ejecutar(out,env).value
        for valor in new_list_index:
            
            try: 
                valor_matriz = valor_matriz[valor]
            except IndexError:
                print("Error: el indice del array esta fuera de rango")
                out.addErrores("Error: el indice del array esta fuera de rango", env.name, self.line, self.column, "Semantico")
                return Symbol(self.line, self.column, None, Type.NULL)
            except TypeError:
                print("Error: ha ocurrido un error")
                out.addErrores("Error: Ha ocurrido un error", env.name, self.line, self.column, "Semantico")
                return Symbol(self.line, self.column, None, Type.NULL)

        return valor_matriz

    def generateASM(self, out, env, generator):
        pass

