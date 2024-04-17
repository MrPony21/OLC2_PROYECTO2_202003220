from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.types import Type
from ..entorno.symbol import Symbol
from ..entorno.out import Out

class AccederArray(Expression):
    def __init__(self, line, column, acceder_exp: Expression, index: list):
        self.line = line
        self.column = column
        self.acceder_exp = acceder_exp
        self.index = index

    def ejecutar(self, out:Out, env: Enviroment):
        
        #ya que utilizamos la misma regla para acceder a matriz nos vendra una lista se obtendra el primer y unico valor
        index_valor = self.index[0]
        index_sym: Symbol = index_valor.ejecutar(out, env)

        if index_sym.type != Type.INTEGER:
            print("Error: el indice debe ser un valor de tipo number")
            out.addErrores("Error: el indice debe ser un valor de tipo number", env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)

        array_sym: Symbol = self.acceder_exp.ejecutar(out, env)

        if array_sym.type == Type.ARRAY:

            try:
                return array_sym.value[index_sym.value]
            except IndexError:
                print("Error: el indice del array esta fuera de rango")
                out.addErrores("Error: el indice del array esta fuera de rango", env.name, self.line, self.column, "Semantico")
                return Symbol(self.line, self.column, None, Type.NULL)
            except TypeError:
                print("Error: ha ocurrido un error")
                out.addErrores("Error: Ha ocurrido un error", env.name, self.line, self.column, "Semantico")
                return Symbol(self.line, self.column, None, Type.NULL)
        else:
            print("Error: ha ocurrido un error al intentar acceder al valor del array")
            out.addErrores("Error: ha ocurrido un error al intentar acceder al valor del array", env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)
        
    def generateASM(self, out, env, generator):
        pass