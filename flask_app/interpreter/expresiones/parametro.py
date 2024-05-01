from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.types import Type

class Parametro(Expression):
    def __init__(self, line, column, identificador, tipo):
        self.line = line
        self.column = column
        self.identificador = identificador
        self.tipo = tipo

    # solo en esta ocacion se usara el value del symbol como el identificador no como valor
    def ejecutar(self, out, env):

          if self.tipo == "number":
               return Symbol(self.line, self.column, self.identificador, Type.INTEGER)
          elif self.tipo == "float":
               return Symbol(self.line, self.column, self.identificador, Type.FLOAT)
          elif self.tipo == "char":
               return Symbol(self.line, self.column, self.identificador, Type.CHAR)
          elif self.tipo == "string":
               return Symbol(self.line, self.column, self.identificador, Type.STRING)
          elif self.tipo == "boolean":
               return Symbol(self.line, self.column, self.identificador, Type.BOOLEAN)
          elif self.tipo == "array":
               return Symbol(self.line, self.column, self.identificador, Type.ARRAY)

    def generateASM(self, out, env, generator):
          
          pass
