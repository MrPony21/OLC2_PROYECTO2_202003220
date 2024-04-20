from ..abstract.instruccion import Instruccion
from ..instrucciones.sentencias import Sentencias
from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.types import Type
from ..entorno.enviroment import Enviroment
from ..entorno.asmbol import Asmbol
from ..entorno.generator import Generator

class IfElse(Instruccion):
    def __init__(self, line, column, condicion: Expression, bloque_sentencias: Sentencias, else_sentencias: Sentencias):
        self.line = line
        self.column = column
        self.condicion = condicion
        self.bloque_sentencias = bloque_sentencias
        self.else_sentencias = else_sentencias

    def ejecutar(self, out, env: Enviroment):
        
        exp_condicion: Symbol = self.condicion.ejecutar(out, env)

        if exp_condicion.type != Type.BOOLEAN:
            x = ("Error: la condicion del if debe recibir un boolean")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return
        
        if exp_condicion.value:
            newEntorno = Enviroment(env, env.name+" If")

            transferencia = self.bloque_sentencias.ejecutar(out, newEntorno)
            if transferencia != None:
                if transferencia.type == Type.BREAK:
                    return Symbol(self.line, self.column, None, Type.BREAK)
                elif transferencia.type == Type.CONTINUE:
                    return Symbol(self.line, self.column, None, Type.CONTINUE)
                elif transferencia.type == Type.RETURN:
                    return transferencia


        else:

            if self.else_sentencias != None:
                newEntorno = Enviroment(env, env.name+" Else")

                if isinstance(self.else_sentencias, Sentencias):
                   transferencia = self.else_sentencias.ejecutar(out, newEntorno)
                elif isinstance(self.else_sentencias, IfElse):
                   transferencia = self.else_sentencias.ejecutar(out, env)
                
                if transferencia != None:
                    if transferencia.type == Type.BREAK:
                        return Symbol(self.line, self.column, None, Type.BREAK)
                    elif transferencia.type == Type.CONTINUE:
                        return Symbol(self.line, self.column, None, Type.CONTINUE)
                    elif transferencia.type == Type.RETURN:
                        return transferencia

    def generateASM(self, out, env, generator: Generator):
        
        exp_condicion: Asmbol = self.condicion.generateASM(out,env, generator)

        new_entorno = Enviroment(env, env.name+" if")

        generator.add_br()
        generator.add_li('t3', str(exp_condicion.valuePos))
        generator.add_lw('t1', '0(t3)')
        temp = generator.new_temp()

        #primero vamos a guardar en un registro el valor de 1 para compararlo con beq y ver si es verdadero
        generator.add_li('t2', "1")

        #generamos el label
        label_if = generator.new_label()
        label_else = generator.new_label()
        label_final = generator.new_label()

        generator.add_operation('beq', 't1', 't2', str(label_if))
        generator.add_jump(label_else)

        generator.write_label(label_if)
        transferencia = self.bloque_sentencias.generateASM(out, new_entorno, generator)
        generator.add_jump(label_final)

        generator.write_label(label_else)

        #aqui solo verificamos que el else no venga vacio para evitar error de generacion
        if self.else_sentencias != None:

            transferencia = self.else_sentencias.generateASM(out, new_entorno, generator)

        generator.write_label(label_final)






