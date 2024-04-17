from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol
from ..entorno.types import Type

class Array_Function(Expression):
    def __init__(self, line, column, exp_array: Expression, tipo_funcion, expresion: Expression):
        self.line = line
        self.column = column
        self.exp_array = exp_array
        self.tipo_funcion = tipo_funcion
        self.expresion = expresion

    def ejecutar(self, out, env):
        
        if self.expresion != None:
            exp_sym: Symbol = self.expresion.ejecutar(out, env)
       
        array: Symbol = self.exp_array.ejecutar(out, env)
        array_valor = array.value

        #validacion si son de mismo tipo 
        if array.type != Type.ARRAY:
            print("Error: se espera un valor de tipo array")
            out.addErrores("Error: se espera un valor de tipo array", env.name, self.line, self.column, "Semantico")
            
            return

        if array.value[0].value == None:
            print("Error: no se puede modificar una array vacio")
            out.addErrores("Error: no se puede modificar una array vacio", env.name, self.line, self.column, "Semantico")
            return

        #aqui verificamos el tipo de funcion y la ejecutamos
        if self.tipo_funcion == "pop":

            pop_valor = array_valor.pop()
            return pop_valor
            
        elif self.tipo_funcion == "indexof":

            if exp_sym == None:
                print("Error: se espera una expresion en la funcion indexOf")
                out.addErrores("Error: se espera una expresion en la funcion indexOf", env.name, self.line, self.column, "Semantico")
                return Symbol(self.line, self.column, None, Type.NULL)
            else: 
                
                valor_encontrado = None
                for valor in array_valor:
                    if exp_sym.value == valor.value:
                        valor_encontrado = valor
                        break

                if valor_encontrado != None:
                    indice = array_valor.index(valor_encontrado)
                    return Symbol(self.line, self.column, indice, Type.INTEGER)
                else:
                    return Symbol(self.line, self.column, -1, Type.INTEGER)
                
        elif self.tipo_funcion == "join":

            cadena = ""
            for valor in array_valor:
                cadena += str(valor.value) +","

            indice_ultima_coma = cadena.rfind(',')
            cadena = cadena[:indice_ultima_coma] + cadena[indice_ultima_coma + 1:]

            return Symbol(self.line, self.column, cadena, Type.STRING)
        
        elif self.tipo_funcion == "length":
            longitud = len(array_valor)
            return Symbol(self.line, self.column, longitud, Type.INTEGER)


    def generateASM(self, out, env, generator):
        pass

            
            
            
