from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..instrucciones.function import Function
from ..entorno.symbol import Symbol
from ..entorno.types import Type
from ..instrucciones.sentencias import Sentencias
from ..entorno.asmbol import Asmbol
from ..entorno.generator import Generator

class CallFunction(Expression):
    def __init__(self, line, column, identificador, expresion_list):
        self.line = line
        self.column = column
        self.identificador = identificador
        self.expresion_list = expresion_list

    def ejecutar(self, out, env: Enviroment):
        
        funcion: Function = env.getFunction(out,self.identificador)
        newEntorno = Enviroment(env, funcion.identificador)

        if funcion == None:
            return Symbol(self.line, self.column, None, Type.NULL)

        #print("se ejecuta la funcion")

        bloque_sentencias: Sentencias = funcion.sentencias

        if self.expresion_list == None and funcion.parametros != None:
            print("Error: no se puede llamar la funcion sin sus parametros")
            out.addErrores("Error: no se puede llamar la funcion sin sus parametros", env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)
        elif self.expresion_list != None and funcion.parametros == None:
            print("Error: la funcion a la que se quiere llamar no tiene parametros")
            out.addErrores("Error: la funcion a la que se quiere llamar no tiene parametros", env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)


        #en esta parte vamos a hacer las verificaciones de los parametros
        if self.expresion_list != None and funcion.parametros != None:

            #error por si se envian diferente cantidad de parametros a los correspondientes
            if len(self.expresion_list) != len(funcion.parametros):
                print("Error: La cantidad de argumentos debe coincidir con la cantidad de parametros de la funcion")
                out.addErrores("Error: La cantidad de argumentos debe coincidir con la cantidad de parametros de la funcion", env.name, self.line, self.column, "Semantico")
                return Symbol(self.line, self.column, None, Type.NULL)

            #aqui vamos a verificar que todas los parametros enviados coincidan con el mismo tipo y asi declaralos en el nuevo entorno y sus errores
            for index in range(0, len(self.expresion_list)):
                parametro: Symbol = funcion.parametros[index].ejecutar(out, env)
                argumento_exp: Symbol = self.expresion_list[index].ejecutar(out, env)

                #print("Argumento:",argumento_exp.type)
                #print("parametro:",parametro.type)
                if argumento_exp.type != parametro.type:
                    print("Error: Los parametros no coinciden con el mismo tipo de variable")
                    out.addErrores("Error: Los parametros no coinciden con el mismo tipo de variable", env.name, self.line, self.column, "Semantico")
                    return Symbol(self.line, self.column, None, Type.NULL)
                
                newEntorno.saveVariable(out, parametro.value, parametro.type, argumento_exp.value, self.line, self.column)

        #en esta parte haremos la verificacion si debe retornar un valor o no 
        if funcion.tipo != None:
            #el value recibido aqui es un symbol
            transferencia = bloque_sentencias.ejecutar(out, newEntorno)

            if transferencia != None:
                if transferencia.type == Type.RETURN:
                    if transferencia.value != None:
                        if transferencia.value.type != funcion.tipo:
                            print("Error: la funcion debe retornar un",funcion.tipo)
                            out.addErrores("Error: Los parametros no coinciden con el mismo tipo de variable", env.name, self.line, self.column, "Semantico")
                            return Symbol(self.line, self.column, None, Type.NULL)
                        else: 
                            return Symbol(self.line, self.column, transferencia.value.value, transferencia.value.type)
                    
            print("Error: El return de la funcion: "+funcion.identificador+" debe retornar una expresion")
            out.addErrores("Error: El return de la funcion: "+funcion.identificador+" debe retornar una expresion", env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)

        else:
            #print("no ahora aqui")
            transferencia = bloque_sentencias.ejecutar(out, newEntorno)

            if transferencia != None:
                if transferencia.type == Type.RETURN:
                    if transferencia.value != None:
                        print("Error: la funcion "+ funcion.identificador+ " no debe de retornar un valor")
                        out.addErrores("Error: la funcion "+ funcion.identificador+ " no debe de retornar un valor", env.name, self.line, self.column, "Semantico")
                        return Symbol(self.line, self.column, None, Type.NULL)
                    return Symbol(self.line, self.column, None, Type.NULL)
                
            return Symbol(self.line, self.column, None, Type.NULL)
                
    def generateASM(self, out, env: Enviroment, generator: Generator):
        

        #primero vamos a guardar los valores de los parametros
        funcion: Function = env.getFunctionASM(self.identificador)
        newEntorno = Enviroment(env, funcion.identificador)

        generator.add_coment("Llamada de funcion")

        generator.add_br()
        
        generator.add_call(str(funcion.identificador))


        



                
