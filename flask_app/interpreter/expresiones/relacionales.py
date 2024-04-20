from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.types import Type
from ..entorno.asmbol import Asmbol
from ..entorno.generator import Generator

class Relacionales(Expression):
    def __init__(self, line, column, exp1: Expression, exp2: Expression, tipo_relacional):
        self.line = line
        self.column = column
        self.exp1 = exp1
        self.exp2 = exp2
        self.tipo_relacional = tipo_relacional

    def ejecutar(self, out, env):

        valor1: Symbol = self.exp1.ejecutar(out,env)
        valor2: Symbol = self.exp2.ejecutar(out,env)

        #x = ("relacionales")
        #x = ("val1: ", valor1.value, valor1.type)
        #x = ("val2: ", valor2.value, valor2.type)


        #> >= < <=
        if valor1.type == valor2.type or (valor1.type == Type.INTEGER and valor2.type == Type.FLOAT) or (valor2.type == Type.INTEGER and valor1.type == Type.FLOAT):
        
            if self.tipo_relacional == '>':
                relacional = valor1.value > valor2.value
                return Symbol(self.line, self.column, relacional, Type.BOOLEAN)
            elif self.tipo_relacional == '>=':
                relacional = valor1.value >= valor2.value
                return Symbol(self.line, self.column, relacional, Type.BOOLEAN)
            elif self.tipo_relacional == '<':
                relacional = valor1.value < valor2.value
                return Symbol(self.line, self.column, relacional, Type.BOOLEAN)
            elif self.tipo_relacional == '<=':
                relacional = valor1.value <= valor2.value
                return Symbol(self.line, self.column, relacional, Type.BOOLEAN) 

        else:
            x = ("Error: Operacion relacional no valida no se pueden comparar distintos tipos")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return Symbol(self.line, self.column, None, Type.NULL)

    def generateASM(self, out, env, generator: Generator):
        
        op1: Asmbol = self.exp1.generateASM(out,env, generator)
        op2: Asmbol = self.exp2.generateASM(out, env, generator)

        generator.add_br()
        generator.add_li('t3', str(op1.valuePos))
        generator.add_lw('t1', '0(t3)')
        generator.add_li('t3', str(op2.valuePos))
        generator.add_lw('t2', '0(t3)')
        temp = generator.new_temp()
        #primero vamos a generar la comparacion y obtener un nuevo label
        new_label = generator.new_label()
        new_label2 = generator.new_label()
        new_label_final = generator.new_label()

        
        if self.tipo_relacional == '>':
            relacional = op1.value > op2.value
            
            generator.add_operation('bgt', 't1', 't2', str(new_label))
            generator.add_jump(str(new_label2))

        elif self.tipo_relacional == '>=':
            relacional = op1.value >= op2.value
            
            generator.add_operation('bge', 't1', 't2', str(new_label))
            generator.add_jump(str(new_label2))
            
        elif self.tipo_relacional == '<':
            relacional = op1.value < op2.value

            generator.add_operation('blt', 't1', 't2', str(new_label))
            generator.add_jump(str(new_label2))

        elif self.tipo_relacional == '<=':
            relacional = op1.value <= op2.value

            generator.add_operation('ble', 't1', 't2', str(new_label))
            generator.add_jump(str(new_label2))


        #por si se cumple
        generator.write_label(str(new_label))
        generator.add_li('t0', str(1))
        generator.add_li('t3', str(temp))
        generator.add_sw('t0', '0(t3)')
        generator.add_jump(str(new_label_final))

        #aqui generamos por si no se cumple
        generator.write_label(str(new_label2))
        generator.add_li('t0', str(0))
        generator.add_li('t3', str(temp))
        generator.add_sw('t0', '0(t3)')

        generator.write_label(str(new_label_final))
        
        if relacional:
            valor = 1
        else:
            valor = 0

        return Asmbol(str(temp), valor, Type.BOOLEAN, False)