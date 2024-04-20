from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol
from ..entorno.types import Type
from ..entorno.asmbol import Asmbol
from ..entorno.generator import Generator
from ..entorno.asmvar import Asmvar

class Asignation(Instruccion):
    def __init__(self, line, column,identificador, valor: Expression, tipo_asignacion):
        self.line = line
        self.column = column
        self.identificador = identificador
        self.valor = valor
        self.tipo_asignacion = tipo_asignacion

    def ejecutar(self, out, env: Enviroment):

        exp: Symbol = self.valor.ejecutar(out,env)
        if self.tipo_asignacion == "=":
            env.changeVariable(out, self.identificador, exp.type , exp.value, self.line, self.column)
        elif self.tipo_asignacion == "+=":
            if exp.type == Type.BOOLEAN:
                x = ("Error: boolean incompatible con operador asignacion suma")
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                return
            elif exp.type == Type.CHAR:
                x = ("Error: char incompatible con operador asignacion suma")
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                return
            valor_variable = env.getVariable(out, self.identificador)
            new_valor = valor_variable.value + exp.value
            env.changeVariable(out, self.identificador, exp.type, new_valor, self.line, self.column)
        elif self.tipo_asignacion == "-=":
            if exp.type == Type.BOOLEAN:
                x = ("Error: boolean incompatible con operador asignacion resta")
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                return
            elif exp.type == Type.CHAR:
                x = ("Error: char incompatible con operador asignacion resta")
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                return
            elif exp.type == Type.STRING:
                x = ("Error: string incompatible con operador asignacion resta")
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                return
            valor_variable = env.getVariable(out, self.identificador)
            new_valor = valor_variable.value - exp.value
            env.changeVariable(out, self.identificador, exp.type, new_valor, self.line, self.column)
        
    def generateASM(self, out, env: Enviroment, generator: Generator):
        
        exp: Asmbol = self.valor.generateASM(out, env, generator)
        print("entre en la asginacionsdkfjal")
        #obtendremos la variable del enviroment 
        var: Asmvar = env.getVariableASM(self.identificador)

        if self.tipo_asignacion == "=":
            
            generator.add_br()
            #primero obtendremos el nuevo valor
            generator.add_li('t3', str(exp.valuePos))
            generator.add_lw('t1', '0(t3)')
            
            #ahora lo cargaremos en la anterior posicion
            generator.add_li('t4', str(var.valuepos))
            generator.add_sw('t1', '0(t4)')


            env.changeVariableASM(self.identificador, var.type, var.valuepos, exp.value)

        #faltan las asignaciones de otros tipos
        elif self.tipo_asignacion == "+=":

            generator.add_br()
            #primero obtendremos el nuevo valor
            generator.add_li('t3', str(exp.valuePos))
            generator.add_lw('t1', '0(t3)')
            generator.add_li('t3', str(var.valuepos))
            generator.add_lw('t2', '0(t3)')
            generator.add_operation('add', 't0', 't1', 't2')

            #ahora lo cargaremos en la anterior posicion
            generator.add_li('t4', str(var.valuepos))
            generator.add_sw('t0', '0(t4)')

            env.changeVariableASM(self.identificador, var.type, var.valuepos, exp.value)

        elif self.tipo_asignacion == "-=":
            
            print("hola")
            generator.add_br()
            #primero obtendremos el nuevo valor
            generator.add_li('t3', str(var.valuepos))
            generator.add_lw('t1', '0(t3)')
            generator.add_li('t3', str(exp.valuePos))
            generator.add_lw('t2', '0(t3)')
            generator.add_operation('sub', 't0', 't1', 't2')

            #ahora lo cargaremos en la anterior posicion
            generator.add_li('t4', str(var.valuepos))
            generator.add_sw('t0', '0(t4)')

            env.changeVariableASM(self.identificador, var.type, var.valuepos, exp.value)


