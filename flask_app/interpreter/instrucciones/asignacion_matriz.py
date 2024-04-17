from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol
from ..entorno.types import Type

class Asignacion_Matriz(Instruccion):
    def __init__(self, line, column, identificador, list_index, valor: Expression):
        self.line = line
        self.column = column
        self.identificador = identificador
        self.list_index = list_index
        self.valor = valor

    def ejecutar(self, out, env: Enviroment):
        
        new_list_index = []
        for value in self.list_index:
            new_list_index.append(value.ejecutar(out,env).value)

        matriz = env.getVariable(out, self.identificador).value

        exp_sym: Expression = self.valor.ejecutar(out,env)

        valor_matriz = matriz

        
        for i in range(len(new_list_index)-1):

            try: 
                valor_matriz = valor_matriz[new_list_index[i]]
            except IndexError:
                print("Error: el indice de la matriz esta fuera de rango")
                out.addErrores("Error: el indice de la matriz esta fuera de rango", env.name, self.line, self.column, "Semantico")
                return Symbol(self.line, self.column, None, Type.NULL)
            except TypeError:
                print("Error: ha ocurrido un error")
                out.addErrores("Error: Ha ocurrido un error", env.name, self.line, self.column, "Semantico")
                return Symbol(self.line, self.column, None, Type.NULL)

        try:
            valor_matriz[new_list_index[-1]] = exp_sym
        except TypeError:
            print("Error: ha ocurrido un error en la asignacion de matriz")
            out.addErrores("Error: Ha ocurrido un error en la asignacion de matriz", env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)

    def generateASM(self, out, env, generator):
        pass