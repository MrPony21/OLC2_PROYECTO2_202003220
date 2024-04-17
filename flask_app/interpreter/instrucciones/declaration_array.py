from ..abstract.instruccion import Instruccion
from ..entorno.types import Type
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol
from ..entorno.enviroment import Enviroment
from ..expresiones.array_expresion import Array_expresion

class Declaration_array(Instruccion):
    def __init__(self, line, column, tipo, identificador, expresion_array, tipo_var):
        self.line = line
        self.column = column
        self.tipo = tipo
        self.identificador = identificador
        self.expresion_array = expresion_array
        self.tipo_var = tipo_var

    #AL GUARDAR EL ARRAY EL TIPO QUE SE MANDA AL ENTORNO ES EL DEL DECLARADO NO EL TYPE.ARRAY
    def ejecutar(self, out, env: Enviroment):
        
        if not isinstance(self.expresion_array, Array_expresion):
            x = "Error no se puede declarar un array de mas de una dimension"
            print(x)
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)

        sym_array: Symbol = self.expresion_array.ejecutar(out, env)

        if self.tipo == 'number':
                tipo = Type.INTEGER
        elif self.tipo == 'string':
                tipo = Type.STRING
        elif self.tipo == 'float':
            tipo = Type.FLOAT
        elif self.tipo == 'char':
                tipo = Type.CHAR
        elif self.tipo == 'boolean':
                tipo = Type.BOOLEAN

        #Este if declara un array vacio pero se crea un symbol por default para saber el tipo del array
        if sym_array == None:
            array_default = []
            default_sym = Symbol(self.line, self.column, None, tipo)
            array_default.append(default_sym)
            if self.tipo_var == "var":
                env.saveVariable(out, self.identificador, Type.ARRAY, array_default, self.line, self.column)
            elif self.tipo_var == "const":
                env.saveConstante(out, self.identificador, Type.ARRAY, array_default, self.line, self.column)
            return


        if sym_array.type == Type.ARRAY:

            try:
                for valor in sym_array.value:
                    if valor.type != tipo:
                        x = ("Error: tipo asignado incompatible con el tipo de array declarado")
                        out.addErrores(x, env.name, self.line, self.column, "Semantico")
                        return Symbol(self.line, self.column, None, Type.NULL)
                
                if self.tipo_var == "var":
                    env.saveVariable(out, self.identificador, Type.ARRAY, sym_array.value, self.line, self.column)
                elif self.tipo_var == "const":
                    env.saveConstante(out, self.identificador, Type.ARRAY, sym_array.value, self.line, self.column)
            except TypeError:
                 x = ("Error: Algo salio mal en la declaracion del array")
                 out.addErrores(x, env.name, self.line, self.column, "Semantico")
                      
        else:
            x = ("Error: no se puede declarar el array valor incompatible")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")


    def generateASM(self, out, env, generator):
        pass
        

        


    