from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..instrucciones.declaration import Declaration
from ..entorno.enviroment import Enviroment
from ..entorno.symbol import Symbol
from ..entorno.types import Type
from ..instrucciones.sentencias import Sentencias
from ..instrucciones.unario import Unario
from ..entorno.asmbol import Asmbol
from ..entorno.generator import Generator

class Inst_For(Instruccion):
    def __init__(self, line, column, declaracion: Declaration, condicional: Expression, unario: Unario, bloque_sentencias: Sentencias):
        self.line = line
        self.column = column
        self.declaracion = declaracion
        self.condicional = condicional
        self.unario = unario
        self.bloque_sentecias = bloque_sentencias

    def ejecutar(self, out, env: Enviroment):

        newEntorno = Enviroment(env, env.name+" FOR")

        self.declaracion.ejecutar(out, newEntorno)
        exp_condicion: Symbol = self.condicional.ejecutar(out, newEntorno)

        #esto es para verificar que la declaracion haya sido number
        var = newEntorno.getVariable(out, self.declaracion.identificador)
        if var.type != Type.INTEGER:
            x = ("Error: la declaracion del for debe ser number")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return 
        #esto es para verificar que la condicion devuelva un boolean
        if exp_condicion.type != Type.BOOLEAN:
            x = ("Error: la condicion del for debe recibir un boolean")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return

        iteracion = 0
        while True:
            
            exp_condicion: Symbol = self.condicional.ejecutar(out, newEntorno)
            if not exp_condicion.value:
                break
            
            #crear metodo clean enviroment
            transferencia = self.bloque_sentecias.ejecutar(out, newEntorno)

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

            
            self.unario.ejecutar(out, newEntorno)
            newEntorno.cleanVariables()
                
    def generateASM(self, out, env, generator: Generator):
        
        newEntorno = Enviroment(env, env.name+" FOR")

        #empezamos generando la declaracion de la variable y verificando la condicion
        generator.add_coment("FOR INICIO")
        self.declaracion.generateASM(out, newEntorno, generator)
        exp_condicion: Asmbol = self.condicional.generateASM(out, newEntorno, generator)
        generator.add_br()
        generator.add_li('t3', str(exp_condicion.valuePos))
        generator.add_lw('t1', '0(t3)')

        var = newEntorno.getVariableASM(self.declaracion.identificador)

        #primero vamos a guardar en un registro el valor de 1 para compararlo con beq y ver si es verdadero
        generator.add_li('t2', '1')

        #generamos los label correspondientes
        start_for = generator.new_label()
        end_for = generator.new_label()

        generator.add_operation('beq', 't1', 't2', str(start_for))
        generator.add_jump(end_for)

        generator.write_label(start_for)
        transferencia = self.bloque_sentecias.generateASM(out, newEntorno, generator)

        self.unario.generateASM(out, newEntorno, generator)

        #volvemos a generar el condicional
        exp_condicion: Asmbol = self.condicional.generateASM(out, newEntorno, generator)

        #evaluamos otra vez la condicion
        generator.add_br()
        generator.add_li('t3', str(exp_condicion.valuePos))
        generator.add_lw('t1', '0(t3)')
        generator.add_li('t2', "1")
        generator.add_operation('beq', 't1', 't2', str(start_for))

        generator.write_label(end_for)
        generator.add_coment("FOR FINAL")