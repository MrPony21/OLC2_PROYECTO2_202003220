from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol
from ..entorno.types import Type

class Push_Array(Instruccion):
    def __init__(self, line, column, identificador,expresion: Expression):
        self.line = line
        self.column = column 
        self.identificador = identificador
        self.expresion = expresion

    def ejecutar(self, out, env: Enviroment):
        
        exp_sym: Symbol = self.expresion.ejecutar(out, env)

        #validacion si son de mismo tipo        
        array: Symbol = env.getVariable(out, self.identificador)
        
        if array.type != Type.ARRAY:
            x = ("Error: unicamente se puede hacer un push a un array")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return

        #aqui verificamos si el array es del mismo tipo
        valor1 = array.value[0]
        tipo_array = valor1.type

        if tipo_array != exp_sym.type:
            x = ("Error: push tipo de valor incompatible con el array")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return
        
        array_valor = array.value
        if valor1.value == None:
            array_valor[0] = exp_sym
        else:
            array_valor.append(exp_sym)

        env.changeVariable(out, self.identificador, array.type, array_valor, self.line, self.column)

    def generateASM(self, out, env, generator):
        pass