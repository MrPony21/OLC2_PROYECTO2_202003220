from ..abstract.instruccion import Instruccion
from ..abstract.expression import Expression
from ..entorno.enviroment import Enviroment
from ..entorno.types import Type
from ..entorno.generator import Generator

class Function(Instruccion):
    def __init__(self, line, column, identificador, parametros, tipo, sentencias):
        self.line = line
        self.column = column
        self.identificador = identificador 
        self.parametros = parametros
        self.tipo = tipo
        self.sentencias = sentencias

    def ejecutar(self, out, env: Enviroment):

        if env.name != "global":
            x = ("Error: unicamente se pueden declarar funciones en el ambito global")
            out.addErrores(x, env.name, self.line, self.column, "Semantico")
            return

        if self.tipo == "number":
             self.tipo = Type.INTEGER
        elif self.tipo == "float":
             self.tipo = Type.FLOAT
        elif self.tipo == "char":
            self.tipo = Type.CHAR
        elif self.tipo == "string":
            self.tipo = Type.STRING
        elif self.tipo == "boolean":
            self.tipo = Type.BOOLEAN
        elif self.tipo == "array":
            self.tipo = Type.ARRAY
        
        
        env.saveFunction(out, self)

    #aqui se debe generar toda la funcion con sus sentencias en asm
    def generateASM(self, out, env: Enviroment, generator: Generator):
        
        generator.add_br()
        
        #creamos otro generator donde contendra todo el codigo de la funcion para luego sumarla al general
        new_generator = Generator()

        #primero vamos a poner los valores actualizados del temporal y msg en el generator    
        temp = generator.get_temp()
        msg = generator.get_msg()
        label_num = generator.get_num_label()

        new_generator.temporal = temp
        new_generator.msg = msg
        new_generator.label = label_num

        #generamos el label de la funcion
        func_label = str(self.identificador)
        new_generator.write_label(func_label)
        new_generator.add_br()

        #parametros
        #cargarmos los parametros desde la pila
        iteracion = 0
        apilador = 0

        if self.parametros != None:
            for parametro in self.parametros:
                new_generator.add_lw('a'+str(iteracion), str(apilador)+"(sp)")
                iteracion+=1
                apilador+=4




        #Apilamos los valores

        #generar sentencias
        self.sentencias.generateASM(out, env, new_generator)
        new_generator.add_br()
        new_generator.add_ret()

        #lo mandamos a escribir al codigo principal
        func_code = new_generator.get_code()
        func_data = new_generator.getDataSection()
        generator.add_code_function(func_code)
        generator.add_data_func(func_data)
        
        #ademas actualizamos los valores del temporal label y msg para no alterar el flujo
        final_temp = new_generator.get_temp()
        final_msg = new_generator.get_msg()
        final_label = new_generator.get_num_label()\
        
        generator.temporal = final_temp
        generator.msg = final_msg
        generator.label = final_label

        env.saveFunctionASM(self)

        

        
