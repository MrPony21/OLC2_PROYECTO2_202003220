from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol
from ..entorno.types import Type

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
        
    def generateASM(self, out, env, generator):
        pass