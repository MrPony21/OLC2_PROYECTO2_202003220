from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.types import Type
from ..entorno.tabla_aritmetica import sumaT, restaT, multT, divT, modT
from ..entorno.out import Out
from ..entorno.generator import Generator
from ..entorno.asmbol import Asmbol

class Aritmetica(Expression):
    def __init__(self, line, column, ope1: Expression, ope2: Expression, signo):
        self.line = line
        self.column = column
        self.ope1 = ope1
        self.ope2 = ope2
        self.signo = signo


    def ejecutar(self, out: Out, env):

        op1 = self.ope1.ejecutar(out, env)
        op2  = self.ope2.ejecutar(out, env)

        #print("op1: ",op1.value ,op1.type,"op2: ",op2.value,op2.type)
        #error null
        if op1.type == Type.NULL or op2.type == Type.NULL:
            print("Error: Null cannot be operated, Linea: ",self.line, "Columna: ",self.column)
            out.addErrores("Error: Null cannot be operated", env.name, self.line, self.column, "Semantico")
            symbol = Symbol(line=self.line, col=self.column, value=None, type=Type.NULL)
            return symbol

        if self.signo == "+":
            dominante = sumaT[op1.type.value][op2.type.value]
            if dominante != Type.NULL:
                symbol = Symbol(line=self.line, col=self.column, value=op1.value+op2.value, type=dominante)
            else:
                print('Error: Operacion incompatible')
                out.addErrores('Error: Operacion incompatible', env.name, self.line, self.column, "Semantico")
                symbol = Symbol(line=self.line, col=self.column, value=None, type=Type.NULL)
            return symbol
        
        elif self.signo  == '-':
            dominante = restaT[op1.type.value][op2.type.value]
            if dominante != Type.NULL:
                symbol = Symbol(line=self.line, col=self.column, value=op1.value-op2.value, type=dominante)
            else:
                print('Error: Operacion incompatible')
                out.addErrores('Error: Operacion incompatible', env.name, self.line, self.column, "Semantico")
                symbol = Symbol(line=self.line, col=self.column, value=None, type=Type.NULL)
            return symbol

        elif self.signo == '*':
            dominante = multT[op1.type.value][op2.type.value]
            if dominante != Type.NULL:
                symbol = Symbol(line=self.line, col=self.column, value=op1.value*op2.value, type=dominante)
            else:
                print('Error: Operacion incompatible')
                out.addErrores('Error: Operacion incompatible', env.name, self.line, self.column, "Semantico")
                symbol = Symbol(line=self.line, col=self.column, value=None, type=Type.NULL)
            return symbol
        
        elif self.signo == '/':
            if op2.value != 0:
                dominante = divT[op1.type.value][op2.type.value]
                if dominante == Type.INTEGER:
                    symbol = Symbol(line=self.line, col=self.column, value=op1.value//op2.value, type=dominante)
                elif dominante == Type.FLOAT:
                    symbol = Symbol(line=self.line, col=self.column, value=op1.value/op2.value, type=dominante)
                else:
                    print('Error: Operacion incompatible')
                    out.addErrores('Error: Operacion incompatible', env.name, self.line, self.column, "Semantico")
                    symbol = Symbol(line=self.line, col=self.column, value=None, type=Type.NULL)
                return symbol
            else:
                print("Error: No se puede dividir dentro de 0")
                out.addErrores('Error: Operacion incompatible', env.name, self.line, self.column, "Semantico")
                return Symbol(line=self.line, col=self.column, value=None, type=Type.NULL)
            
        elif self.signo == '%':
            if op2.value != 0:
                dominante = modT[op1.type.value][op2.type.value]
                if dominante != Type.NULL:
                    symbol = Symbol(line=self.line, col=self.column, value=op1.value%op2.value, type=dominante)
                else:
                    print('Error: Operacion incompatible')
                    out.addErrores('Error: Operacion incompatible', env.name, self.line, self.column, "Semantico")
                    symbol = Symbol(line=self.line, col=self.column, value=None, type=Type.NULL)
                return symbol
            else:
                print("Error: No se puede dividir dentro de 0")
                out.addErrores("Error: No se puede dividir dentro de 0", env.name, self.line, self.column, "Semantico")
                return Symbol(line=self.line, col=self.column, value=None, type=Type.NULL)

        elif self.signo == 'umenos':
            
            if op2.type == Type.INTEGER:
                symbol = Symbol(line = self.line, col=self.column, value= (-op2.value), type=Type.INTEGER )
                
            elif op2.type == Type.FLOAT:
                symbol = Symbol(line = self.line, col=self.column, value= (-op2.value), type=Type.FLOAT )
            else:
                print("Error: Operacion unaria incompatible con el tipo")
                out.addErrores("Error: Operacion unaria incompatible con el tipo", env.name, self.line, self.column, "Semantico")
                symbol = Symbol(line=self.line, col=self.column, value=None, type=Type.NULL)
            return symbol


        return Symbol(line=self.line, col=self.column, value=None, type=Type.NULL)
    

    def generateASM(self, out, env, generator: Generator):
        
        op1: Asmbol = self.ope1.generateASM(out, env, generator)
        op2: Asmbol = self.ope2.generateASM(out, env, generator)

        generator.add_br()
        generator.add_li('t3', str(op1.valuePos))
        generator.add_lw('t1', '0(t3)')
        generator.add_li('t3', str(op2.valuePos))
        generator.add_lw('t2', '0(t3)')
        temp = generator.new_temp()

        if self.signo == "+":
            dominante = sumaT[op1.type.value][op2.type.value]

            if dominante == Type.INTEGER:

                generator.add_operation('add', 't0', 't1', 't2')
                valor = op1.value + op2.value
                generator.add_li('t3', str(temp))
                generator.add_sw('t0', '0(t3)')
                return Asmbol(str(temp), valor, dominante, False)


        elif self.signo == "-":

            dominante = restaT[op1.type.value][op2.type.value]

            if dominante == Type.INTEGER:

                generator.add_operation('sub', 't0', 't1', 't2')
                valor = op1.value - op2.value
                generator.add_li('t3', str(temp))
                generator.add_sw('t0', '0(t3)')
                return Asmbol(str(temp), valor, dominante, False)
            
        elif self.signo == "*":

            dominante = multT[op1.type.value][op2.type.value]

            if dominante == Type.INTEGER:

                generator.add_operation('mul', 't0', 't1', 't2')
                valor = op1.value * op2.value
                generator.add_li('t3', str(temp))
                generator.add_sw('t0', '0(t3)')
                return Asmbol(str(temp), valor, dominante, False)
            
        elif self.signo == "/":

            dominante = divT[op1.type.value][op2.type.value]

            if dominante == Type.INTEGER:

                generator.add_operation('div', 't0', 't1', 't2')
                valor = op1.value / op2.value
                generator.add_li('t3', str(temp))
                generator.add_sw('t0', '0(t3)')
                return Asmbol(str(temp), valor, dominante, False)
            
        elif self.signo == 'umenos':

            print('ejslkrtfjasklsjd')
            if op2.type == Type.INTEGER:
                temp = generator.new_temp()
                generator.add_br()
                new_value = -op2.value
                generator.add_li('t0', str(new_value))
                generator.add_li('t3', str(temp))
                generator.add_sw('t0','0(t3)')
                return Asmbol(str(temp), -op2.value, Type.INTEGER, False)
        
            elif op2.type == Type.FLOAT:
                pass

        #falta programar el module
