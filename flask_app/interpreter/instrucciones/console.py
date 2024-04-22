from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.types import Type
from ..entorno.out import Out
from ..entorno.asmbol import Asmbol
from ..entorno.generator import Generator

class Console(Instruccion):
    def __init__(self, line, col, Exp: Expression):
        self.line = line
        self.col = col
        self.Exp = Exp

    
    def ejecutar(self, out: Out, env):
        consoleout = ''


        for exp in self.Exp:
            sym = exp.ejecutar(out, env)

            #print(exp)
            if sym.type == Type.ARRAY:
                salida = self.print_array(sym.value)
                consoleout += salida
            elif sym.type == Type.INTERFACE:
                salida = self.printInterface(sym.value)
                consoleout += salida
            elif sym.type == Type.MATRIZ:
                salida = self.printMatiz(sym.value)
                consoleout += salida
            else:
                consoleout += " " + str(sym.value)

        out.addConsole(consoleout)
        print(consoleout)


    def print_array(self, array):

        salida = "[ "
        #print(array)

        for symbol in array:
            salida += str(symbol.value) + ", "
        salida += "]"

        #eliminamos la ultima coma
        indice_ultima_coma = salida.rfind(',')
        salida = salida[:indice_ultima_coma] + salida[indice_ultima_coma + 1:]
        return salida


    def printInterface(self, diccionary):
        
        salida = '{'

        for key, value in diccionary.items():
            salida += str(key+" : "+value.value+ ", ")
        salida += '}'

        #eliminamos la ultima coma
        indice_ultima_coma = salida.rfind(',')
        salida = salida[:indice_ultima_coma] + salida[indice_ultima_coma + 1:]
        return salida
    
    def printMatiz(self, matriz):

        salida = "[ "

        for valor in matriz:

            if isinstance(valor, list):
                
                salida += self.printMatiz(valor) + ", "
            
            else:

                salida += str(valor.value) + ", "

        salida += " ]"
        indice_ultima_coma = salida.rfind(',')
        salida = salida[:indice_ultima_coma] + salida[indice_ultima_coma + 1:]

        return salida
    

    def generateASM(self, out, env, generator: Generator):
        
        for exp in self.Exp:

            asym: Asmbol = exp.generateASM(out, env, generator)
            #print(asym)

            generator.add_br()
            generator.add_li('t3', str(asym.valuePos))
            generator.add_lw('a0', '0(t3)')
            

            if asym.type == Type.INTEGER:
                generator.add_li('a7', '1')
            elif asym.type == Type.STRING:
                generator.add_li('a7', '4')
            elif asym.type == Type.BOOLEAN:
                generator.add_li('a7', '1')
                generator.add_ecall()
                if asym.value == 1:
                    generator.add_la('a0', 'true')
                elif asym.value == 0:
                    generator.add_la('a0', 'false')
                generator.add_li('a7', '4')



            generator.add_ecall()

            #salto de linea
            generator.add_br()
            generator.add_li('a0', '10')
            generator.add_li('a7', '11')
            generator.add_ecall()