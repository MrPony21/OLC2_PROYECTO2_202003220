from ..abstract.instruccion import Instruccion
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol
from ..entorno.asmbol import Asmbol
from ..entorno.generator import Generator
from ..entorno.asmvar import Asmvar

class Unario(Instruccion):
    def __init__(self, line, column, identificador, tipo_unario):
        self.line = line
        self.column = column
        self.identificador = identificador
        self.tipo_unario = tipo_unario

    def ejecutar(self, out, env: Enviroment):
        
        valor_variable: Symbol = env.getVariable(out, self.identificador)

        if self.tipo_unario == "++":
            new_value = valor_variable.value + 1
            env.changeVariable(out, self.identificador, valor_variable.type, new_value, self.line, self.column)
        elif self.tipo_unario == "--":
            new_value = valor_variable.value - 1
            env.changeVariable(out, self.identificador, valor_variable.type, new_value, self.line, self.column)

    def generateASM(self, out, env: Enviroment, generator: Generator):
        
        valor_var: Asmvar = env.getVariableASM(self.identificador)

        generator.add_coment("Unario del for")
        if self.tipo_unario == "++":
            new_value = valor_var.value + 1

            generator.add_br()
            generator.add_li('t3', str(valor_var.valuepos))
            generator.add_lw('t1', '0(t3)')
            #aqui cargaremos el valor 1 para sumarlo
            generator.add_li('t2', '1')

            generator.add_operation('add', 't0', 't1', 't2')

            #ahora se carga a la posicion anterior
            generator.add_li('t4', str(valor_var.valuepos))
            generator.add_sw('t0', '0(t4)')

            env.changeVariableASM(self.identificador, valor_var.type, valor_var.valuepos, new_value)
            

        elif self.tipo_unario == "--":
            new_value = valor_var.value - 1
           
            generator.add_br()
            generator.add_li('t3', str(valor_var.valuepos))
            generator.add_lw('t1', '0(t3)')
            #aqui cargaremos el valor 1 para sumarlo
            generator.add_li('t2', '1')

            generator.add_operation('sub', 't0', 't1', 't2')

            #ahora se carga a la posicion anterior
            generator.add_li('t4', str(valor_var.valuepos))
            generator.add_sw('t0', 't0(t4)')

            env.changeVariableASM(self.identificador, valor_var.type, valor_var.valuepos, new_value)

