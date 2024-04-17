from ..abstract.expression import Expression
from ..entorno.symbol import Symbol
from ..entorno.types import Type
from ..entorno.tabla_aritmetica import sumaT, restaT, multT, divT, modT
from ..entorno.out import Out

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
    

    def generateASM(self, out, env, generator):
        pass