from flask import Flask, request, jsonify
from flask_cors import CORS
from interpreter.parser.gramatica import Parser
from interpreter.entorno.enviroment import Enviroment
from interpreter.instrucciones.function import Function
from interpreter.entorno.out import Out
from interpreter.entorno.generator import Generator
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>hello_world</p>"

@app.route('/interpreter', methods=['POST'])
def ejecutar():
    
    jsonobj = request.json
    input = jsonobj.get("code")
    print("emtrada",input)
    errores = []

    parse = Parser()
    env = Enviroment(None, 'global')
    out = Out()

    instrucciones = parse.interpretar(input)
    errores = parse.getErrors()

    try:
        for inst in instrucciones:
            if isinstance(inst, Function):
                inst.ejecutar(out,env)


        for inst in instrucciones:
            if not (isinstance(inst, Function)):
                #print(inst)
                inst.ejecutar(out,env)
    except TypeError:
        pass

    tabla = json.dumps(out.tabla_simbolos)  
    errores_lexicos_sintacticos = errores
    errores_semanticos = out.errores
    errores_final = errores_lexicos_sintacticos + errores_semanticos
    err_json = json.dumps(errores_final)
    #print("esta es mi tabla",tabla)
    #print("Estos son mis erroers semanticos", err_json)
    res = {"console": out.console, "tabla": tabla, "errores": err_json}
    return jsonify(res)
    

@app.route('/traducir', methods=['POST'])
def traducir():

    jsonobj = request.json
    input = jsonobj.get("code")
    print("emtrada",input)
    errores = []

    parse = Parser()
    env = Enviroment(None, 'global')
    out = Out()
    generator = Generator()
    

    instrucciones = parse.interpretar(input)
    errores = parse.getErrors()

    #vamos a ejecutar nuestro interpreter tambien esto unicamente para la busqueda de errores
    try:
        for inst in instrucciones:
            if isinstance(inst, Function):
                inst.ejecutar(out,env)


        for inst in instrucciones:
            if not (isinstance(inst, Function)):
                #print(inst)
                inst.ejecutar(out,env)
    except TypeError:
        pass

    code = []
    #aqui verificamos si hay errores para no generar ASM y retornar los errores
    if len(errores) != 0 or len(out.errores) != 0:
        pass
    else:
        for inst in instrucciones:
            inst.generateASM(out, env , generator)

        code = generator.get_final_code()

    #env.showVariables() 

    #recuperacion de errores y tabla de simbolos
    tabla = json.dumps(out.tabla_simbolos)  
    errores_lexicos_sintacticos = errores
    errores_semanticos = out.errores
    errores_final = errores_lexicos_sintacticos + errores_semanticos
    err_json = json.dumps(errores_final)

    #retorno de respuesta
    res = {"console": code, "tabla": tabla, "errores": err_json}
    return jsonify(res)



if __name__ == "__main__":
    app.run(port=5000)


# with open("entrada.txt", 'r') as archivo:
#     input = archivo.read()
#     archivo.close()


# parse = Parser()
# #parse.lexical(input)
# env = Enviroment(None, 'global')
# out = Out()
# gen = Generator()

# instrucciones = parse.interpretar(input)
# for inst in instrucciones:
#         inst.generateASM(out,env, gen)

# code = gen.get_final_code()
# print(code)


# env.showVariables()
# env.showConstantes()
# env.showFunctions()
# env.showInterfaces()
