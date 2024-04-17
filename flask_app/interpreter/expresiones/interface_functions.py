from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.out import Out
from ..entorno.symbol import Symbol
from ..entorno.types import Type

class Interface_Function(Expression):
    def __init__(self, line, colum, expresion: Expression, tipo_funcion):
        self.line = line
        self.column = colum
        self.expresion = expresion
        self.tipo_funcion = tipo_funcion

    def ejecutar(self, out: Out, env: Enviroment):
        
        exp_sym: Symbol = self.expresion.ejecutar(out, env)
        if exp_sym.type != Type.INTERFACE:
            x = "Error: la funcion "+self.tipo_funcion+" unicamente se puede aplicar a interfaces"
            print(x)
            out.addErrores(x, env.name, self.line, self.column, "Semantico")

        
        #en esta parte debemos de crear un array de symbols para evitar errores
        if self.tipo_funcion == "keys":
            diccionario_symbol = exp_sym.value
            list_keys = list(diccionario_symbol.keys())
            list_symbol = []
            for key in list_keys:
                list_symbol.append(Symbol(self.line, self.column, key, Type.STRING))
            return Symbol(self.line, self.column, list_symbol, Type.ARRAY)
        elif self.tipo_funcion == "values":
            diccionario_symbol = exp_sym.value
            list_values = list(diccionario_symbol.values())
            list_symbol = []
            for value in list_values:
                list_symbol.append(Symbol(self.line, self.column, str(value.value), Type.STRING))
            return Symbol(self.line, self.column, list_symbol, Type.ARRAY)
        
        print("hno entre")


    def generateASM(self, out, env, generator):
        pass

