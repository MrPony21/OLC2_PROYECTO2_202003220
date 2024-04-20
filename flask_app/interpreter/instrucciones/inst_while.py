from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol
from .sentencias import Sentencias
from ..entorno.types import Type
from ..entorno.enviroment import Enviroment
from ..entorno.asmbol import Asmbol
from ..entorno.generator import Generator

class Inst_While(Instruccion):
    def __init__(self, line, column, condicion: Expression, bloque_sentencias: Sentencias ):
        self.line = line
        self.column = column
        self.condicion = condicion
        self.bloque_sentencias = bloque_sentencias

    def ejecutar(self, out, env: Enviroment):
        
        exp_condicion: Symbol = self.condicion.ejecutar(out, env)
        newEntorno = Enviroment(env, env.name+" While")

        if exp_condicion.type != Type.BOOLEAN:
            x = ("Error: la condicion del while debe recibir un boolean")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return
        
        iteracion = 0
        while True:
            
            exp_condicion = self.condicion.ejecutar(out, env)
            if not exp_condicion.value:
                break
                
            transferencia = self.bloque_sentencias.ejecutar(out, newEntorno)

            # esto es por si es un bucle infinito
            if iteracion == 150:
                x = ("Error: Se ha entrado a un bucle infinito")
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                break
            iteracion += 1


            if transferencia != None:
                if transferencia.type == Type.BREAK:
                    break
                elif transferencia.type == Type.CONTINUE:
                    continue
                elif transferencia.type == Type.RETURN:
                    return transferencia

    def generateASM(self, out, env, generator: Generator):
        
        exp_condicion: Asmbol = self.condicion.generateASM(out,env, generator)

        new_entorno = Enviroment(env, env.name+" while")

        generator.add_br()
        generator.add_li('t3', str(exp_condicion.valuePos))
        generator.add_lw('t1', '0(t3)')
        temp = generator.new_temp()

        #primero vamos a guardar en un registro el valor de 1 para compararlo con beq y ver si es verdadero
        generator.add_li('t2', "1")

        #generamos los label correspondientes
        label_while = generator.new_label()
        end_while = generator.new_label()


        generator.add_operation('beq', 't1', 't2', str(label_while))
        generator.add_jump(end_while)

        generator.write_label(label_while)
        transferencia = self.bloque_sentencias.generateASM(out, new_entorno, generator)

        # en teoria aqui al haberse ejecutado todas las sentencias ya debio cambiar el valor de la variable y deberia dar true
        exp_condicion = self.condicion.generateASM(out, env, generator)

        generator.add_br()
        generator.add_li('t3', str(exp_condicion.valuePos))
        generator.add_lw('t1', '0(t3)')
        generator.add_li('t2', "1")
        generator.add_operation('beq', 't1', 't2', str(label_while))

        generator.write_label(end_while)


        

            

            
