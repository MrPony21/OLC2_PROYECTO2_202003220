from ..abstract.instruccion import Instruccion
from ..entorno.enviroment import Enviroment
from ..entorno.types import Type
from ..entorno.out import Out
from ..entorno.symbol import Symbol

class Declaration_Interface(Instruccion):
    def __init__(self, line, column, identificador, tipo, atr_list, tipo_var):
        self.line = line
        self.column = column
        self.identificador = identificador
        self.tipo = tipo
        self.atr_list = atr_list
        self.tipo_var = tipo_var

    def ejecutar(self, out: Out, env: Enviroment):
        
        #buscar el interface  con sus atributos
        list_diccionario_interface = env.getInterface(out, self.tipo)

        if list_diccionario_interface == None:
            x = "Error: no existe el tipo de interface que se quiere declarar"
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return

        keys_interface = list_diccionario_interface.keys()
        keys_atr = self.atr_list.keys()
        
        if keys_interface != keys_atr:
            x = "Error: no se ha declarar un interface ya que los atributos no coinciden"
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return
        
        #verificar que sean los mismos tipos
        for clave in list_diccionario_interface:
            atr_sym = self.atr_list[clave].ejecutar(out, env)
            #print("estos son los atributos de cada:", atr_sym.value,"con el tipo",atr_sym.type)
            #print("se tiene que comparar: ", list_diccionario_interface[clave])
            if atr_sym.type != list_diccionario_interface[clave]:
                x = "Error: no se puede declarar una variable incompatible en el interface: "+clave
                print(x)
                out.addErrores(x, env.name, self.line, self.column, "Semantico")
                return
            
        #crear un nuevo diccionario con sus valores de symbol por si todo salio bien
        new_diccionary = {}
        for clave, value in self.atr_list.items():
            new_diccionary[clave] = value.ejecutar(out, env)

        #print(new_diccionary)


        if self.tipo_var == "var":
            env.saveVariable(out, self.identificador, Type.INTERFACE, new_diccionary, self.line, self.column)
        elif self.tipo_var == "const":
            env.saveConstante(out, self.identificador, Type.INTERFACE, new_diccionary, self.line, self.column)        


    def generateASM(self, out, env, generator):
        pass
