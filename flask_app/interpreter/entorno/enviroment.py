from ..entorno.symbol import Symbol
from ..entorno.types import Type
from ..entorno.out import Out
from ..entorno.asmbol import Asmbol
from ..entorno.asmvar import Asmvar

class Enviroment():
    def __init__(self, prev, name):
        self.prev: Enviroment = prev
        self.name = name
        self.variables = {}
        self.constantes = {}
        self.funciones = {}
        self.interfaces = {}
        


    def saveVariable(self,out: Out,variable, tipo, valor, line, column):

        if variable in self.constantes:
            x = ("Error: La variable ",variable," ya ha sido declarada como constante")
            out.addErrores(x, self.name , line, column, "Semantico")
            return

        if variable in self.variables:
            x = ("Error: La variable ",variable ," ya existe")
            out.addErrores(x, self.name , line, column, "Semantico")
            return
        self.variables[variable] = Symbol(line=line, col=column, value=valor, type=tipo)
        table_symbol = {
            "ID": str(variable),
            "Tipo_simbolo": "variable",
            "Tipo de dato": str(tipo),
            "Ambito": str(self.name),
            "linea": str(line),
            "columna": (column)
        }
        out.add_tabla_simbolos(table_symbol)

    def changeVariable(self, out, variable, tipo, valor, line, column):
        
        if variable in self.constantes:
            x = ("Error: El valor de una constante no puede ser cambiado: ", variable)
            out.addErrores(x, self.name , line, column, "Semantico")
            return

        if variable in self.variables:

            tipo_declarado = self.variables[variable].type
            #print(tipo_declarado, tipo)
            if tipo_declarado == tipo:
                self.variables[variable] = Symbol(line=line, col=column, value=valor, type=tipo)
            else:
                #conversion de number a variable tipo float
                if tipo_declarado == Type.FLOAT and tipo == Type.INTEGER:
                    new_float = float(valor)
                    self.variables[variable] = Symbol(line=line, col=column, value=new_float, type=Type.FLOAT)
                else:
                    #Se asigna valor a null para fines practicos segun el enunciado
                    x = ("Error: asignacion de tipos incompatible")
                    out.addErrores(x, self.name , line, column, "Semantico")
                    self.variables[variable] = Symbol(line=line, col=column, value=None, type=Type.NULL)
                    return False
            return True
        else:

            prev_env = self.prev
            while prev_env != None:
                change_asignation = prev_env.changeVariable(out, variable, tipo, valor, line, column)
                if change_asignation == True:
                    return True
                prev_env = prev_env.prev

            x = ("Error: se quiere cambiar variable sin haber sido declararada")
            out.addErrores(x, self.name , line, column, "Semantico")
            return False

    def getVariable(self,out, id):
        
        if id in self.variables:
            return self.variables[id]
        elif id in self.constantes:
            return self.constantes[id]
        else:

            prev_env = self.prev
            while prev_env != None:
                variable = prev_env.getVariable(out, id)
                if variable.type != Type.NULL:
                    return variable
                prev_env = prev_env.prev

            x = ("Error: No existe la variable a la cual se quiere acceder: ",id)
            out.addErrores(x, self.name , "", "", "Semantico")
            return Symbol('0','0', None, Type.NULL)

    def cleanVariables(self):
        primer_clave = next(iter(self.variables))
        primer_valor = self.variables[primer_clave]
        self.variables.clear()
        self.variables[primer_clave] = primer_valor

    def showVariables(self):

        for index in self.variables:
            print("variables:",index,self.variables[index].value, self.variables[index].type)

    def saveConstante(self, out: Out, constante, tipo, valor, line, column):
        
        if constante in self.variables:
            x = ("Error: La constante ",constante," ya ha sido declarada como variable")
            out.addErrores(x, self.name , "", "", "Semantico")
            return

        if constante in self.constantes:
            x = ("Error: La constante ",constante," ya existe")
            out.addErrores(x, self.name , "", "", "Semantico")
            return
        self.constantes[constante] = Symbol(line=line, col=column, value=valor, type=tipo)
        table_symbol = {
            "ID": str(constante),
            "Tipo_simbolo": "constante",
            "Tipo de dato": str(tipo),
            "Ambito": str(self.name),
            "linea": str(line),
            "columna": (column)
        }
        out.add_tabla_simbolos(table_symbol)

    def showConstantes(self):

        for index in self.constantes:
            print("Constantes:",index, self.constantes[index].value, self.constantes[index].type)

    def saveFunction(self, out: Out, funcion):

        #Error: si se quiere declarar una funcion dentro de otro entorno que no sea el global
        if self.prev != None:
            x = ("Error: no se puede declarar una funcion dentro de otro ambito: ",funcion.identificador)
            out.addErrores(x, self.name , "", "", "Semantico")
            return

        if funcion.identificador in self.funciones:
            x = ("Error: la funcion", funcion.identificador, "ya ha sido declarada ")
            out.addErrores(x, self.name , self.line, self.column, "Semantico")
            return
        
        self.funciones[funcion.identificador] = funcion
        table_symbol = {
            "ID": str(funcion.identificador),
            "Tipo_simbolo": "Funcion",
            "Tipo de dato": str(funcion.tipo),
            "Ambito": str(self.name),
            "linea": str(funcion.line),
            "columna": (funcion.column)
        }
        out.add_tabla_simbolos(table_symbol)

    def getFunction(self, out,identificador):

        entornoGlobal = self.getGlobal()

        if identificador in entornoGlobal.funciones:
            return entornoGlobal.funciones[identificador]
        else:
            x = ("Error no existe la funcion a la cual se quiere acceder: ",identificador)
            out.addErrores(x, self.name , "", "", "Semantico")
            return None

    def showFunctions(self):

        for index in self.funciones:
            print("Funcion:",index, self.funciones[index].parametros, self.funciones[index].tipo, self.funciones[index].sentencias)

    def saveInterface(self, out: Out, identificador, atributos, line, column):

        if identificador in self.interfaces:
            x = ("Error: El interface ",identificador," ya ha sido definido")
            out.addErrores(x, self.name , line, column, "Semantico")
            return
        self.interfaces[identificador] = atributos

    def getInterface(self, out: Out, identificador):

        entornoGlobal = self.getGlobal()

        if identificador in entornoGlobal.interfaces:
            return entornoGlobal.interfaces[identificador]
        else:
            x = ("Error no existe el interface a la cual se quiere acceder: ",identificador)
            out.addErrores(x, self.name , "", "", "Semantico")
            return None

    def showInterfaces(self):

        for index in self.interfaces:
            print("Interfaces:" ,index, self.interfaces[index])

    def getGlobal(self):

        env_global = self.prev
        if env_global == None:
            return self    
        else:
            while env_global.prev != None:
                env_global = env_global.prev
                
            return env_global


#-----------------------AQUI IRA TODOO LO DE ASM--------------------
    def saveVariableASM(self, variable, tipo, pos, value):

        self.variables[variable] = Asmvar(variable, tipo, pos, value)

    def getVariableASM(self, id):

        if id in self.variables:
            return self.variables[id]
        elif id in self.constantes:
            return self.constantes[id]
        else:

            prev_env = self.prev
            while prev_env != None:
                variable = prev_env.getVariableASM(id)
                if variable.type != Type.NULL:
                    return variable
                prev_env = prev_env.prev

    # falta la conversion de tipo integer a tipo float
    def changeVariableASM(self, variable, tipo, pos, value):

        if variable in self.variables:
            self.variables[variable] = Asmvar(variable, tipo, pos, value)
        else:

            prev_env = self.prev
            while prev_env != None:
                change_asignation = prev_env.changeVariableASM( variable, tipo, pos, value)
                if change_asignation == True:
                    return True
                prev_env = prev_env.prev

    def saveConstanteASM(self, id, tipo, pos, value):

        self.constantes[id] = Asmvar(id, tipo, pos, value)




