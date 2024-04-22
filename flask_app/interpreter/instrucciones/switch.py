from ..abstract.instruccion import Instruccion
from ..instrucciones.case import Case
from ..entorno.symbol import Symbol
from ..abstract.expression import Expression
from ..entorno.types import Type
from ..entorno.asmbol import Asmbol
from ..entorno.generator import Generator

class Switch(Instruccion):
    def __init__(self, line, column, exp: Expression, cases, default):
        self.line = line
        self.column = column
        self.exp = exp
        self.cases = cases
        self.default = default


    def ejecutar(self, out, env):

        exp_principal: Symbol = self.exp.ejecutar(out, env) 

        #Error en caso de que venga mas de un default
        cont_default = 0
        for case in self.cases:
            
            if case.exp == "default":
                cont_default +=1

        if cont_default > 1:
            x = ("Error: no puede venir mas de dos default en el switch")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return

        #Ejecucion de comparacion de la expresion del switch con la expresion del case y asi ejecutar sus sentencias o en caso de no encontrar ejecucion del default
        for case in self.cases:
            
            if case.exp != "default":

                exp_case: Symbol = case.exp.ejecutar(out, env)

                if exp_principal.value == exp_case.value and exp_principal.type == exp_case.type:

                    transferencia = case.ejecutar(out, env)

                    if transferencia != None:
                        if transferencia.type == Type.BREAK:
                            #x = ("Todo salio a la perfeccion")
                            return
                        elif transferencia.type == Type.CONTINUE:
                            x = ("Error: No puede venir la sentencia de transferencia continue dentro de un case")
                            out.addErrores(x, env.name, self.line, self.column, "Semantico")
                            return
                        elif transferencia.type == Type.RETURN:
                            return transferencia
                    
                    else:
                        x = ("Error: Hace falta un break en la sentencia switch")
                        out.addErrores(x, env.name, self.line, self.column, "Semantico")

            else:
                
                #Error en caso de que el default venga de primero
                last_default = self.cases[-1].exp == 'default'
                if (not last_default):
                    x = ("Error: El default debe ser la ultima clausula")
                    out.addErrores(x, env.name, self.line, self.column, "Semantico")
                    return

                transferencia = case.ejecutar(out, env)

                if transferencia != None:
                        if transferencia.type == Type.BREAK:
                            x = ("Error: No puede venir la sentencia de transferencia continue en el default")
                            out.addErrores(x, env.name, self.line, self.column, "Semantico")
                            return
                        elif transferencia.type == Type.CONTINUE:
                            x = ("Error: No puede venir la sentencia de transferencia continue dentro el default")
                            out.addErrores(x, env.name, self.line, self.column, "Semantico")
                            return
                        elif transferencia.type == Type.RETURN:
                            return transferencia
 
    def generateASM(self, out, env, generator: Generator):
        
        exp_principal: Asmbol = self.exp.generateASM(out, env, generator)

        default = None
        #primero vamos a verificar si viene el default
        if self.cases[-1].exp == "default":
            default = self.cases.pop(-1)

        generator.add_coment("SWITCH INICIO")
        #aqui estamos cargando el valor dentro del switch
        generator.add_br()
        generator.add_li('t3', str(exp_principal.valuePos))
        generator.add_lw('t1', '0(t3)')

        #aqui vamos a generar el label default cabe mencionar que el default es opcional

        list_labels = []
        #primero vamos a generar todos los label 
        for case in self.cases:

            exp_case: Asmbol = case.exp.generateASM(out ,env, generator)
            
            #aqui vamos a cargar las expresiones de cada case
            generator.add_br()
            generator.add_li('t3', str(exp_case.valuePos))
            generator.add_lw('t2', '0(t3)')

            label_case = generator.new_label()
            list_labels.append(label_case)

            generator.add_operation('beq', 't1', 't2', str(label_case))

        label_default = generator.new_label()
        generator.add_jump(label_default)
        end_switch = generator.new_label()

        #segundo vamos a escribir los label junto con sus instrucciones
        iteracion = 0
        for case in self.cases:

            generator.add_br()
            generator.write_label(list_labels[iteracion])

            transferencia = case.generateASM(out, env, generator, end_switch)

            
            iteracion += 1

        
        #aqui vamos a generar el codigo del default si venia
        if default != None:
            generator.write_label(label_default)
            default.generateASM(out, env, generator, end_switch)

        generator.write_label(end_switch)

  









