from ..abstract.instruccion import Instruccion
from ..entorno.enviroment import Enviroment
from ..abstract.expression import Expression
from ..entorno.types import Type
from ..entorno.symbol import Symbol
from ..expresiones.primitivo import Primitivo
from ..entorno.asmbol import Asmbol

class Declaration(Instruccion):
    def __init__(self, line, column, tipo_declaracion, identificador, tipo, value: Expression):
        self.line = line
        self.column = column
        self.tipo_declaracion = tipo_declaracion
        self.identificador = identificador
        self.tipo = tipo
        self.value = value

    def ejecutar(self, out, env: Enviroment):

        if self.value != None:
            exp = self.value.ejecutar(out, env)

            if exp == None:
                x = ("Error: error en la declaracion no puedes asignar un null")
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                return

        tipo: Type = None

       

        if self.tipo_declaracion == "variable":
            #declaration 1
            if self.tipo != None and self.value != None:
                correctAsignation = False

                if self.tipo == 'number':
                    if exp.type == Type.INTEGER:
                        correctAsignation = True
                        tipo = Type.INTEGER
                elif self.tipo == 'string':
                    if exp.type == Type.STRING:
                        correctAsignation = True
                        tipo = Type.STRING
                elif self.tipo == 'float':
                    if exp.type == Type.FLOAT:
                        correctAsignation = True
                    if exp.type == Type.INTEGER:
                        correctAsignation = True
                        exp.value = float(exp.value)
                    tipo = Type.FLOAT
                elif self.tipo == 'char':
                    if exp.type == Type.CHAR:
                        correctAsignation = True
                        tipo = Type.CHAR
                elif self.tipo == 'boolean':
                    if exp.type == Type.BOOLEAN:
                        correctAsignation = True
                        tipo = Type.BOOLEAN

                if correctAsignation:
                    env.saveVariable(out, self.identificador, tipo, exp.value,self.line, self.column)
                else:
                    x = ("Error: Tipo de variable incompatible con el valor asignado ","Linea:",self.line, "Columna:",self.column)
                    out.addErrores(x, env.name, self.line, self.column, "Semantico")

            #declaracion 2
            elif self.tipo == None:

                tipo = exp.type

                env.saveVariable(out, self.identificador, tipo, exp.value, self.line, self.column)
            
            #declaracion 3
            elif self.value == None:

                valor = ''
                if self.tipo == 'number':
                    tipo = Type.INTEGER
                    valor = 0
                elif self.tipo == 'string':
                    tipo = Type.STRING
                    valor = ""
                elif self.tipo == 'float':
                    tipo = Type.FLOAT
                    valor = 0.0
                elif self.tipo == 'char':
                    tipo = Type.CHAR
                    valor = ''
                elif self.tipo == 'boolean':
                    tipo = Type.BOOLEAN
                    valor = True

                env.saveVariable(out, self.identificador, tipo, valor, self.line, self.column)

            else:

                x = ("Error: Ha ocurrido un error en la asignacion de variable", "Linea:",self.line, "Columna:",self.column)
                out.addErrores(x, env.name, self.line, self.column, "Semantico")

        elif self.tipo_declaracion == "constante":

            if self.tipo != None and self.value != None:
                correctAsignation = False

                if self.tipo == 'number':
                    if exp.type == Type.INTEGER:
                        correctAsignation = True
                        tipo = Type.INTEGER
                elif self.tipo == 'string':
                    if exp.type == Type.STRING:
                        correctAsignation = True
                        tipo = Type.STRING
                elif self.tipo == 'float':
                    if exp.type == Type.FLOAT:
                        correctAsignation = True
                    if exp.type == Type.INTEGER:
                        correctAsignation = True
                        exp.value = float(exp.value)
                    tipo = Type.FLOAT
                elif self.tipo == 'char':
                    if exp.type == Type.CHAR:
                        correctAsignation = True
                        tipo = Type.CHAR
                elif self.tipo == 'boolean':
                    if exp.type == Type.BOOLEAN:
                        correctAsignation = True
                        tipo = Type.BOOLEAN

                if correctAsignation:
                    env.saveConstante(out, self.identificador, tipo, exp.value,self.line, self.column)
                else:
                    x = ("Error: Tipo de constante incompatible con el valor asignado ","Linea:",self.line, "Columna:",self.column)
                    out.addErrores(x, env.name, self.line, self.column, "Semantico")

            elif self.tipo == None:

                    tipo = exp.type

                    env.saveConstante(out, self.identificador, tipo, exp.value, self.line, self.column)

    def generateASM(self, out, env: Enviroment, generator):
        

        exp: Asmbol = self.value.generateASM(out, env, generator)
       

        if self.tipo_declaracion == "variable":
            #declaration 1
            if self.tipo != None and self.value != None:
                correctAsignation = False

                if self.tipo == 'number':
                    if exp.type == Type.INTEGER:
                        correctAsignation = True
                        tipo = Type.INTEGER
                elif self.tipo == 'string':
                    if exp.type == Type.STRING:
                        correctAsignation = True
                        tipo = Type.STRING
                elif self.tipo == 'float':
                    if exp.type == Type.FLOAT:
                        correctAsignation = True
                    if exp.type == Type.INTEGER:
                        correctAsignation = True
                        exp.value = float(exp.value)
                    tipo = Type.FLOAT
                elif self.tipo == 'char':
                    if exp.type == Type.CHAR:
                        correctAsignation = True
                        tipo = Type.CHAR
                elif self.tipo == 'boolean':
                    if exp.type == Type.BOOLEAN:
                        correctAsignation = True
                        tipo = Type.BOOLEAN

                if correctAsignation:
                    env.saveVariableASM(self.identificador, tipo, exp.valuePos,exp.value)
            
            #declaracion 2
            elif self.tipo == None:

                tipo = exp.type

                env.saveVariableASM(self.identificador, tipo,exp.valuePos,exp.value)
            
            #declaracion 3
            elif self.value == None:

                valor = ''
                if self.tipo == 'number':
                    tipo = Type.INTEGER
                    valor = 0
                elif self.tipo == 'string':
                    tipo = Type.STRING
                    valor = ""
                elif self.tipo == 'float':
                    tipo = Type.FLOAT
                    valor = 0.0
                elif self.tipo == 'char':
                    tipo = Type.CHAR
                    valor = ''
                elif self.tipo == 'boolean':
                    tipo = Type.BOOLEAN
                    valor = True

                env.saveVariableASM(self.identificador, tipo, exp.valuePos ,exp.value)


        elif self.tipo_declaracion == "constante":

            if self.tipo != None and self.value != None:
                correctAsignation = False

                if self.tipo == 'number':
                    if exp.type == Type.INTEGER:
                        correctAsignation = True
                        tipo = Type.INTEGER
                elif self.tipo == 'string':
                    if exp.type == Type.STRING:
                        correctAsignation = True
                        tipo = Type.STRING
                elif self.tipo == 'float':
                    if exp.type == Type.FLOAT:
                        correctAsignation = True
                    if exp.type == Type.INTEGER:
                        correctAsignation = True
                        exp.value = float(exp.value)
                    tipo = Type.FLOAT
                elif self.tipo == 'char':
                    if exp.type == Type.CHAR:
                        correctAsignation = True
                        tipo = Type.CHAR
                elif self.tipo == 'boolean':
                    if exp.type == Type.BOOLEAN:
                        correctAsignation = True
                        tipo = Type.BOOLEAN

                if correctAsignation:
                    env.saveConstante(out, self.identificador, tipo, exp.value,self.line, self.column)
   
            elif self.tipo == None:

                    tipo = exp.type

                    env.saveConstante(out, self.identificador, tipo, exp.value, self.line, self.column)

        