from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..instrucciones.declaration import Declaration
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol
from ..entorno.types import Type
from ..instrucciones.sentencias import Sentencias
from ..instrucciones.unario import Unario

class Inst_For_Array(Instruccion):
    def __init__(self, line, column, identificador, array_exp: Expression,  bloque_sentencias: Sentencias):
        self.line = line
        self.column = column
        self.identificador = identificador
        self.array_exp = array_exp
        self.bloque_sentecias = bloque_sentencias

    def ejecutar(self, out, env: Enviroment):
        
        newEntorno = Enviroment(env, env.name+" FOR")
        array_sym: Symbol = self.array_exp.ejecutar(out, env)

        if array_sym.type != Type.ARRAY:
            x = ("Error: la expresion recibida en el for debe ser de tipo array")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return

        valores = array_sym.value
        valor1_array = valores[0].value
        tipo_array = valores[0].type

        newEntorno.saveVariable(out, self.identificador, tipo_array, valor1_array, self.line, self.column)

        for iteracion in range(len(valores)):

            newEntorno.changeVariable(out, self.identificador, tipo_array, valores[iteracion].value ,self.line, self.column)
            transferencia = self.bloque_sentecias.ejecutar(out, newEntorno)

            if transferencia != None:
                if transferencia.type == Type.BREAK:
                    break
                elif transferencia.type == Type.CONTINUE:
                    continue
                elif transferencia.type == Type.RETURN:
                    return transferencia
                
            newEntorno.cleanVariables()

    def generateASM(self, out, env, generator):
        pass