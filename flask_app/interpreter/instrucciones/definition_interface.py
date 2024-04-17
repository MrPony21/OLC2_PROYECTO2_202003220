from ..abstract.instruccion import Instruccion
from ..entorno.enviroment import Enviroment
from ..entorno.types import Type

class Definition_Interface(Instruccion):
    def __init__(self, line, column, identificador, atributos):
        self.line = line
        self.column = column
        self.identificador = identificador
        self.atributos = atributos

    def ejecutar(self, out, env: Enviroment):

        #aqui cambiaremos los valores a number, string, float, char y float
        for clave, valor in self.atributos.items():
              
            if valor == 'number':
                self.atributos[clave] = Type.INTEGER
            elif valor == 'string':
                self.atributos[clave] = Type.STRING
            elif valor == 'float':
                self.atributos[clave] = Type.FLOAT
            elif valor == 'char':
                self.atributos[clave] = Type.CHAR
            elif valor == 'boolean':
                self.atributos[clave] = Type.BOOLEAN
            else:
                interface = env.getInterface(out, valor)
                if interface != None:
                    self.atributos[clave] = Type.INTERFACE

        if env.name != "global":
            x = ("Error: unicamente se pueden definir interfaces en el ambito global")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return
        env.saveInterface(out, self.identificador, self.atributos, self.line, self.column)

    def generateASM(self, out, env, generator):
        pass