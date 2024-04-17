from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.types import Type
from ..entorno.symbol import Symbol
from ..entorno.out import Out

class Declaration_Matriz(Instruccion):
    def __init__(self, line, column, tipo, identificador, dimension, list_valores, tipo_var):
        self.line = line
        self.column = column
        self.tipo = tipo
        self.identificador = identificador
        self.dimension = dimension
        self.list_valores = list_valores
        self.tipo_var = tipo_var

    def ejecutar(self, out: Out, env: Enviroment):
        
        if self.tipo == 'number':
            self.tipo = Type.INTEGER
        elif self.tipo == 'string':
            self.tipo = Type.STRING
        elif self.tipo == 'float':
            self.tipo = Type.FLOAT
        elif self.tipo == 'char':
            self.tipo = Type.CHAR
        elif self.tipo == 'boolean':
            self.tipo = Type.BOOLEAN

        new_matriz = []
        new_matriz = self.obtenerValores(self.list_valores, self.dimension, out, env)

        if not isinstance(new_matriz, list):
            if new_matriz.type == Type.NULL:
                return Symbol(self.line, self.column, None, Type.NULL)  

        if self.tipo_var == "var":
            env.saveVariable(out, self.identificador, Type.MATRIZ, new_matriz, self.line, self.column)
        elif self.tipo_var == "const":
            env.saveConstante(out, self.identificador, Type.MATRIZ, new_matriz, self.line, self.column)


    #esto varia dependiendo de la dimension
    def obtenerValores(self, matriz, restante, out: Out, env):
        
        valores_matriz = []
        for valor in matriz:

            if restante != 1:
                #print("valor cuando faltan restantes", valor)
                val = self.obtenerValores(valor, restante-1, out, env)

                if not isinstance(val, list):
                    if val.type == Type.NULL:
                        return Symbol(self.line, self.column, None, Type.NULL)

                valores_matriz.append(val)
            else: 
                #print(valor.ejecutar(out, env))
                value_sym = valor.ejecutar(out, env)
                #error por si viene un tipo incomaptible
                if value_sym.type != self.tipo:
                    x = "Error: tipos incompatibles en la declaracion de la matriz"
                    print(x)
                    out.addErrores(x, env.name, self.line, self.column, "Semantico")
                    return Symbol(self.line, self.column, None, Type.NULL)
                
                valores_matriz.append(valor.ejecutar(out, env))

                
        return valores_matriz

    def generateASM(self, out, env, generator):
        pass