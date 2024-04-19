from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.asmbol import Asmbol
from ..entorno.types import Type
from ..entorno.generator import Generator

class Primitivo(Expression):
    def __init__(self, line, col, value, type):
        self.line = line
        self.col = col
        self.value = value
        self.type = type

    def ejecutar(self, out, env):
        return Symbol(line=self.line, col=self.col, value=self.value, type=self.type)
    
    def generateASM(self, out, env, generator: Generator):
        
        if self.type == Type.INTEGER:
            temp = generator.new_temp()
            generator.add_br()
            generator.add_li('t0', str(self.value))
            generator.add_li('t3', str(temp))
            generator.add_sw('t0','0(t3)')
            return Asmbol(str(temp), self.value, self.type, False)
        
        if self.type == Type.STRING:
            temp_msg = generator.new_msg()
            value_data = f'"{self.value}"'
            generator.add_section_data(temp_msg, "string", value_data)

            temp = generator.new_temp()
            generator.add_br()
            generator.add_la('t0', str(temp_msg))
            generator.add_li('t3', str(temp))
            generator.add_sw('t0', '0(t3)')
            return Asmbol(str(temp), self.value, self.type, False)
        
        if self.type == Type.BOOLEAN:

            if self.value:
                valor = 1
            else:
                valor = 0

            temp = generator.new_temp()
            generator.add_br()
            generator.add_li('t0', str(valor))
            generator.add_li('t3', str(temp))
            generator.add_sw('t0', '0(t3)')
            return Asmbol(str(temp), valor, self.type, False)