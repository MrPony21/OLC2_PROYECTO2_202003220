from ..abstract.instruccion import Instruccion
from ..entorno.types import Type
from ..entorno.symbol import Symbol
from ..abstract.expression import Expression
from ..entorno.asmbol import Asmbol
from ..entorno.generator import Generator

class Transferencia(Instruccion):
    def __init__(self, line, column, tipo_transferencia, valor: Expression):
        self.line = line
        self.column = column 
        self.tipo_transferencia = tipo_transferencia
        self.valor = valor

    def ejecutar(self, out, env):

        if self.tipo_transferencia == 'break':
            return Symbol(self.line, self.column, None, Type.BREAK)
        elif self.tipo_transferencia == 'continue':
            return Symbol(self.line, self.column, None, Type.CONTINUE)
        elif self.tipo_transferencia == 'return':

            if self.valor != None:
                exp_sym = self.valor.ejecutar(out, env)
                #print(exp_sym,"esto es")
                return Symbol(self.line, self.column, exp_sym, Type.RETURN)
            else:
                #print("aqui no")
                return Symbol(self.line, self.column, None, Type.RETURN)

    def generateASM(self, out, env, generator: Generator):
        
        if self.tipo_transferencia == 'break':
            generator.add__break_pos()
            #print("pues si entre en el breaky genere", generator.break_pos)
        elif self.tipo_transferencia == 'continue':
            generator.add_continue_pos()
        