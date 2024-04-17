from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.types import Type

class Function(Instruccion):
    def __init__(self, line, column, identificador, parametros, tipo, sentencias):
        self.line = line
        self.column = column
        self.identificador = identificador 
        self.parametros = parametros
        self.tipo = tipo
        self.sentencias = sentencias

    def ejecutar(self, out, env: Enviroment):

        if env.name != "global":
            x = ("Error: unicamente se pueden declarar funciones en el ambito global")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return

        if self.tipo == "number":
             self.tipo = Type.INTEGER
        elif self.tipo == "float":
             self.tipo = Type.FLOAT
        elif self.tipo == "char":
            self.tipo = Type.CHAR
        elif self.tipo == "string":
            self.tipo = Type.STRING
        elif self.tipo == "boolean":
            self.tipo = Type.BOOLEAN
        elif self.tipo == "array":
            self.tipo = Type.ARRAY
        
        
        env.saveFunction(out, self)


    def generateASM(self, out, env, generator):
        pass