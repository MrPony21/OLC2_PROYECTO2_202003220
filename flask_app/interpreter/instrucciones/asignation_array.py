from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol
from ..entorno.types import Type

class Asignation_Array(Instruccion):
    def __init__(self, line, column, identificador, index: Expression, valor: list):
        self.line = line
        self.column = column
        self.identificador = identificador
        self.index = index
        self.valor = valor

    def ejecutar(self, out, env: Enviroment):
        
        exp_sym: Symbol = self.valor.ejecutar(out, env)
        
        array: Symbol = env.getVariable(out, self.identificador)

        #ya que utilizamos la misma regla para acceder a matriz nos vendra una lista se obtendra el primer y unico valor
        index_valor = self.index[0]
        index_sym: Symbol = index_valor.ejecutar(out, env)
        
        #error si el index no es de tipo integer
        if index_sym.type != Type.INTEGER:
            x = ("Error: el indice debe ser un valor de tipo number")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return

        #error si el valor no es un array
        if array.type != Type.ARRAY:
            x = ("Error: el valor que se quiere cambiar no es de un array ")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return
        
        valor1 = array.value[0]
        tipo_array = valor1.type

        #error si no son del mismo tipo
        if tipo_array != exp_sym.type:
            x = ("Error: el valor asignado no es del mismo tipo al valor del array")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return
        
        array_valor = array.value

        array_valor[index_sym.value] = exp_sym

        env.changeVariable(out, self.identificador, array.type, array_valor, self.line, self.column)

    def generateASM(self, out, env, generator):
        pass