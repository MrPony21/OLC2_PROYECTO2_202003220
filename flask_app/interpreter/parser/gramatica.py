import interpreter.parser.ply.lex as Lex
import interpreter.parser.ply.yacc as yacc

#importacion de expresiones
from ..entorno.types import Type
from ..expresiones.primitivo import Primitivo
from ..expresiones.aritmetica import Aritmetica
from ..expresiones.accedervar import Accedervar
from ..expresiones.comparation import Comparation
from ..expresiones.relacionales import Relacionales
from ..expresiones.logicas import Logicas
from ..expresiones.parametro import Parametro
from ..expresiones.callFunction import CallFunction
from ..expresiones.ternario import Ternario
from ..expresiones.parseint import ParseInt
from ..expresiones.parsefloat import ParseFloat
from ..expresiones.tostring import ToString
from ..expresiones.tolowercase import ToLowerCase
from ..expresiones.touppercase import ToUpperCase
from ..expresiones.typeof import TypeOf
from ..expresiones.array_expresion import Array_expresion
from ..expresiones.accederarray import AccederArray
from ..expresiones.array_functions import Array_Function
from ..expresiones.accederinterface import AccederInterface
from ..expresiones.interface_functions import Interface_Function
from ..expresiones.accedermatriz import AccederMatriz

#importacion de instrucciones
from ..instrucciones.console import Console
from ..instrucciones.declaration import Declaration
from ..instrucciones.asignation import Asignation
from ..instrucciones.sentencias import Sentencias
from ..instrucciones.ifelse import IfElse
from ..instrucciones.inst_while import Inst_While
from ..instrucciones.transferencia import Transferencia
from ..instrucciones.inst_for import Inst_For
from ..instrucciones.unario import Unario
from ..instrucciones.function import Function
from ..instrucciones.switch import Switch
from ..instrucciones.case import Case
from ..instrucciones.declaration_array import Declaration_array
from ..instrucciones.push_array import Push_Array
from ..instrucciones.asignation_array import Asignation_Array
from ..instrucciones.definition_interface import Definition_Interface
from ..instrucciones.declaration_interface import Declaration_Interface
from ..instrucciones.asignacion_interface import Asignacion_Interface
from ..instrucciones.inst_for_array import Inst_For_Array
from ..instrucciones.declaration_matriz import Declaration_Matriz
from ..instrucciones.asignacion_matriz import Asignacion_Matriz

class codeParams:
    def __init__(self, line, column):
        self.line = line
        self.column = column

errores = []

#--------------------------------------------------------ANALISIS LEXICO------------------------------------------------------

reservadas = {
    'var': 'VAR',
    'const': 'CONST',
    'interface': 'INTERFACE',
    'function': 'FUNCTION',
    'console': 'CONSOLE',
    'log': 'LOG',
    'if': 'IF',
    'else': 'ELSE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'while': 'WHILE',
    'for': 'FOR',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'string': 'RES_STRING',
    'number': 'RES_NUMBER',
    'float': 'RES_FLOAT',
    'char': 'RES_CHAR',
    'boolean': 'RES_BOOLEAN',
    'parseInt': 'RES_PARSEINT',
    'parseFloat': 'RES_PARSEFLOAT',
    'toString' : 'RES_TOSTRING',
    'toLowerCase': 'RES_TOLOWER',
    'toUpperCase': 'RES_TOUPPER',
    'typeof': 'RES_TYPEOF',
    'push': 'RES_PUSH',
    'pop': 'RES_POP',
    'indexOf': 'RES_INDEXOF',
    'join': 'RES_JOIN',
    'length': 'RES_LENGTH',
    'Object': 'RES_OBJECT',
    'keys': 'RES_KEYS',
    'values': 'RES_VALUES',
    'of' : 'RES_OF'

}



tokens = [
    #SIMBOLOS RESERVADOS
    'LLAVEIZQ',
    'LLAVEDER',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'PUNTO',
    'COMA',
    'PUNTOCOMA',
    'DOSPUNTOS',
    'INTER',
    #RESERVADAS ARITMETICAS
    'MAS',
    'MENOS',
    'MULT',
    'DIV',
    'MOD',
    'DOBLEMAS',
    'DOBLEMENOS',
    #RACIONALES
    'IGUAL',
    'IGUALDAD',
    'DESIGUALDAD',
    'MAYOR',
    'MAYORIGUAL',
    'MENOR',
    'MENORIGUAL',
    #LOGICOS
    'AND',
    'OR',
    'NOT',
    #---CON EXPRESION REGULAR----
    #TIPO DE DATO
    'CADENA',
    'NUMBER',
    'FLOAT',
    'CHAR',
    'BOOL',
    'IDENTIFICADOR'

] + list(reservadas.values())



#SIMBOLOS RESERVADOS
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_PUNTO = r'\.'
t_COMA = r'\,'
t_PUNTOCOMA = r'\;'
t_DOSPUNTOS = r'\:'
t_INTER = r'\?'

#RESERVADAS ARITMETICAS
t_MAS = r'\+'
t_MENOS = r'\-'
t_MULT = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_DOBLEMAS = r'\+\+'
t_DOBLEMENOS = r'\-\-'

#RESERVADAS RACIONALES
t_IGUAL = r'='
t_IGUALDAD = r'=='
t_DESIGUALDAD = r'!='
t_MAYOR = r'>'
t_MAYORIGUAL = r'>='
t_MENOR = r'<'
t_MENORIGUAL = r'<='

#RESERVADAS LOGICAS
t_AND = r'&&'
t_OR = r'\|\|' 
t_NOT = r'!'

#expresiones regulares
def t_CADENA(t):
    r'"([^"\\]|\\.)*"'
    try:
        strValue = str(t.value)
        strValue = strValue[1:-1]
        strValue = strValue.replace(r'\"', '"')
        strValue = strValue.replace(r'\\', '\\')
        strValue = strValue.replace(r'\n', '\n')
        strValue = strValue.replace(r'\r', '\r')
        strValue = strValue.replace(r'\t', '\t')
        line = t.lexer.lexdata.rfind('\n',0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitivo(line, column, strValue, Type.STRING)
    except ValueError:
        print("Error al convertir en string %d", t.value)
        descripcion = "Error al convertir en string %d "+ t.value
        error = {
            "descripcion": descripcion,
            "ambito": "global",
            "linea": line,
            "column": column,
            "tipo": "lexico"
        }
        errores.append(error)
        t.value = None
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    try:
        floatValue = float(t.value)
        line = t.lexer.lexdata.rfind('\n',0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitivo(line, column, floatValue, Type.FLOAT)
    except ValueError:
        print("Error al convertir en float %d", t.value)
        descripcion = "Error al convertir en float %d "+ t.value
        error = {
            "descripcion": descripcion,
            "ambito": "global",
            "linea": line,
            "column": column,
            "tipo": "lexico"
        }
        errores.append(error)
        t.value = 0
    return t

def t_NUMBER(t):
    r'\d+'
    try:
        intValue = int(t.value)
        line = t.lexer.lexdata.rfind('\n',0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitivo(line, column, intValue, Type.INTEGER)
    except ValueError:
        print("Error al convertir en entero %d", t.value)
        descripcion = "Error al convertir en entero %d "+ t.value
        error = {
            "descripcion": descripcion,
            "ambito": "global",
            "linea": line,
            "column": column,
            "tipo": "lexico"
        }
        errores.append(error)

        t.value = 0
    return t


def t_CHAR(t):
    r"\'[^']\'"
    try:
        charValue = str(t.value)
        line = t.lexer.lexdata.rfind('\n',0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitivo(line,column, charValue.replace("'",""), Type.CHAR)
    except ValueError:
        print("Error al convertir en char %d", t.value)
        descripcion = "Error al convertir en char %d "+ t.value
        error = {
            "descripcion": descripcion,
            "ambito": "global",
            "linea": line,
            "column": column,
            "tipo": "lexico"
        }
        errores.append(error)
    return t

def t_BOOL(t):
    r'(true|false)'
    try:
        if t.value == 'false':
            boolValue = bool(False)
        elif t.value == 'true':
            boolValue = bool(True)
        line = t.lexer.lexdata.rfind('\n',0, t.lexpos) + 1
        column = t.lexpos - line
        t.value = Primitivo(line, column, boolValue, Type.BOOLEAN)
    except ValueError:
        print("Error al convertir a booleano %d", t.value)
        descripcion = "Error al convertir a booleano %d "+ t.value
        error = {
            "descripcion": descripcion,
            "ambito": "global",
            "linea": line,
            "column": column,
            "tipo": "lexico"
        }
        errores.append(error)
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'IDENTIFICADOR')
    return t

t_ignore = " \t"

t_ignore_COMMENTLINE = r'\/\/.*'

def t_ignore_COMMENTBLOCK(t):
    r'\/\*[^*]*\*+(?:[^/*][^*]*\*+)*\/'
    t.lexer.lineno += t.value.count('\n')

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    line = t.lexer.lexdata.rfind('\n',0, t.lexpos) + 1
    column = t.lexpos - line
    print("Error Léxico '%s'" % t.value[0])
    descripcion = "Error Léxico '%s'" % t.value[0]
    error = {
        "descripcion": descripcion,
        "ambito": "global",
        "linea": line,
        "column": column,
        "tipo": "lexico"
    }
    errores.append(error)
    t.lexer.skip(1)



#----------------------------------------------------ANALISIS SINTACTICO--------------------------------------------------------------
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUALDAD', 'DESIGUALDAD'),
    ('left', 'MENOR', 'MENORIGUAL', 'MAYORIGUAL', 'MAYOR'),
    ('left', 'MAS','MENOS'),
    ('left','DIV','MOD','MULT'),
    ('right','UNMENOS'),
    ('right', 'NOT'),
    ('left', 'PARIZQ', 'PARDER', 'CORIZQ', 'CORDER'),
)





#INICIO DE SINTACTICO
def p_instrucciones_lista(t):
    '''instrucciones : instrucciones instruccion
                    | instruccion '''
    
    if 2 < len(t):
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
    
#-----------------------------------------------------------------INSTRUCCIONES----------------------------------------------------------
def p_instruccion_console(t):
    '''instruccion : CONSOLE PUNTO LOG PARIZQ expresiones PARDER PUNTOCOMA'''
    params = get_params(t)
    t[0] = Console(params.line, params.column, t[5])

def p_declaraciones(t):
    '''instruccion : declaracion
                    | declaracion_const
                    | declaracion_array
                    | definition_interface
                    | declaration_interface '''
    t[0] = t[1]
def p_instruccion_declaration1(t):
    'declaracion : VAR IDENTIFICADOR DOSPUNTOS tipo IGUAL expresion PUNTOCOMA'
    params = get_params(t)
    t[0] = Declaration(params.line, params.column, "variable", t[2],t[4] ,t[6])

def p_instruccion_declaration2(t):
    'declaracion : VAR IDENTIFICADOR IGUAL expresion PUNTOCOMA'
    params = get_params(t)
    t[0] = Declaration(params.line, params.column,"variable", t[2], None,t[4])

def p_instruccion_declaration3(t):
    'declaracion : VAR IDENTIFICADOR DOSPUNTOS tipo PUNTOCOMA'
    params = get_params(t)
    t[0] = Declaration(params.line, params.column,"variable", t[2], t[4], None)

def p_instruccion_declaration_constante(t):
    'declaracion_const : CONST IDENTIFICADOR DOSPUNTOS tipo IGUAL expresion PUNTOCOMA'
    params = get_params(t)
    t[0] = Declaration(params.line, params.column, "constante", t[2], t[4], t[6])

def p_instruccion_declaration_constante2(t):
    'declaracion_const : CONST IDENTIFICADOR IGUAL expresion PUNTOCOMA'
    params = get_params(t)
    t[0] = Declaration(params.line, params.column, "constante", t[2], None, t[4])


def p_instruccion_asignacion(t):
    'instruccion : IDENTIFICADOR IGUAL expresion PUNTOCOMA'
    params = get_params(t)
    t[0] = Asignation(params.line, params.column, t[1], t[3], '=')

def p_instruccion_asignacion2(t):
    'instruccion : IDENTIFICADOR MAS IGUAL expresion PUNTOCOMA'
    params = get_params(t)
    t[0] = Asignation(params.line, params.column, t[1], t[4], '+=')

def p_instruccion_asignacion3(t):
    'instruccion : IDENTIFICADOR MENOS IGUAL expresion PUNTOCOMA'
    params = get_params(t)
    t[0] = Asignation(params.line, params.column, t[1], t[4], '-=')

def p_instruccion_flujo(t):
    '''instruccion : inst_if
                | inst_while
                | inst_for
                | inst_switch'''
    t[0] = t[1]

def p_if(t):
    '''inst_if : IF PARIZQ expresion PARDER sentencias ELSE sentencias
                | IF PARIZQ expresion PARDER sentencias
                | IF PARIZQ expresion PARDER sentencias ELSE inst_if'''
    params = get_params(t)

    if len(t) == 8 and isinstance(t[7], IfElse):
        t[0] = IfElse(params.line, params.column, t[3], t[5], t[7])
    elif len(t) == 6:
        t[0] = IfElse(params.line, params.column, t[3], t[5], None)
    elif len(t) == 8:
        t[0] = IfElse(params.line, params.column, t[3], t[5], t[7])

def p_while(t):
    'inst_while : WHILE PARIZQ expresion PARDER sentencias'
    params = get_params(t)
    t[0] = Inst_While(params.line, params.column, t[3], t[5])

def p_for_numerico(t):
    'inst_for : FOR PARIZQ declaracion expresion PUNTOCOMA unario PARDER sentencias'
    params = get_params(t)
    t[0] = Inst_For(params.line, params.column, t[3], t[4], t[6], t[8])

def p_for_array(t):
    'inst_for : FOR PARIZQ VAR IDENTIFICADOR RES_OF expresion PARDER sentencias'
    params = get_params(t)
    t[0] = Inst_For_Array(params.line, params.column, t[4], t[6], t[8])


def p_unario(t):
    '''unario : IDENTIFICADOR DOBLEMAS
                | IDENTIFICADOR DOBLEMENOS'''
    params = get_params(t)
    if t[2] == "++":
        t[0] = Unario(params.line, params.column, t[1],  '++')
    elif t[2] == "--":
        t[0] = Unario(params.line, params.column, t[1], "--")

def p_switch(t):
    '''inst_switch : SWITCH PARIZQ expresion PARDER LLAVEIZQ list_case LLAVEDER '''
    params = get_params(t)
    t[0] = Switch(params.line, params.column, t[3], t[6], None)

def p_list_case(t):
    '''list_case : list_case inst_case
                | inst_case'''

    arr = []
    if len(t) > 2:
        arr = t[1] + [t[2]]
        t[0] = t[1]
    else:
        arr.append(t[1])
    t[0] = arr

def p_case(t):
    '''inst_case : CASE expresion DOSPUNTOS instrucciones
                | DEFAULT DOSPUNTOS instrucciones'''
    params = get_params(t)
    if len(t) == 5:
        t[0] = Case(params.line, params.column, t[2], t[4])
    elif len(t) == 4:
        t[0] = Case(params.line, params.column, t[1], t[3])

def p_function(t):
    '''instruccion : FUNCTION IDENTIFICADOR PARIZQ PARDER DOSPUNTOS tipo sentencias
                | FUNCTION IDENTIFICADOR PARIZQ PARDER sentencias
                | FUNCTION IDENTIFICADOR PARIZQ parametros_lista PARDER DOSPUNTOS tipo sentencias
                | FUNCTION IDENTIFICADOR PARIZQ parametros_lista PARDER sentencias'''
    params = get_params(t)
    if len(t) == 8:
        t[0] = Function(params.line, params.column, t[2], None, t[6], t[7])
    elif len(t) == 6:
        t[0] = Function(params.line, params.column, t[2], None, None, t[5])
    elif len(t) == 9: 
        t[0] = Function(params.line, params.column, t[2], t[4], t[7], t[8])
    elif len(t) == 7:
        t[0] = Function(params.line, params.column, t[2], t[4], None, t[6])

def p_parametro_lista(t):
    '''parametros_lista : parametros_lista COMA parametro
                        | parametro'''
    arr = []
    if len(t) > 2:
        arr = t[1] + [t[3]]
        t[0] = t[1]
    else:
        arr.append(t[1])
    t[0] = arr

def p_parametro(t):
    '''parametro : IDENTIFICADOR DOSPUNTOS tipo
                | IDENTIFICADOR DOSPUNTOS tipo CORIZQ CORDER'''
    params = get_params(t)
    if len(t) == 4:
        t[0] = Parametro(params.line, params.column, t[1], t[3])
    elif len(t) == 6:
        t[0] = Parametro(params.line, params.column, t[1], "array")

def p_callfuncion_instruccion(t):
    '''instruccion : IDENTIFICADOR PARIZQ expresiones PARDER PUNTOCOMA
                    | IDENTIFICADOR PARIZQ PARDER PUNTOCOMA'''
    params = get_params(t)
    if len(t) == 6:
        t[0] = CallFunction(params.line, params.column, t[1], t[3])
    elif len(t) == 5:
        t[0] = CallFunction(params.line, params.column, t[1], None)

def p_sentencias(t):
    'sentencias : LLAVEIZQ instrucciones LLAVEDER'
    params = get_params(t)
    t[0] = Sentencias(params.line, params.column, t[2])

def p_transferencia(t):
    '''instruccion : BREAK PUNTOCOMA
                    | CONTINUE PUNTOCOMA
                    | RETURN PUNTOCOMA
                    | RETURN expresion PUNTOCOMA'''
    params = get_params(t)
    if t[1] == ("break"):
        t[0] = Transferencia(params.line, params.column, "break", None)
    if  t[1] == ("continue"):
        t[0] = Transferencia(params.line, params.column, "continue", None)
    if  t[1] == ("return") and len(t) == 4:
        t[0] = Transferencia(params.line, params.column, "return", t[2])
    if  t[1] == ("return") and len(t) == 3:
        t[0] = Transferencia(params.line, params.column, "return", None)

#arrays
def p_array_declaration(t):
    '''declaracion_array : VAR IDENTIFICADOR DOSPUNTOS tipo tamano_matriz IGUAL array PUNTOCOMA
                        | CONST IDENTIFICADOR DOSPUNTOS tipo tamano_matriz IGUAL array PUNTOCOMA'''
    params = get_params(t)
    if t[5] == 1:
        t[0] = Declaration_array(params.line, params.column, t[4], t[2], t[7], t[1])
    elif t[5] > 1:
        t[0] = Declaration_Matriz(params.line, params.column, t[4], t[2], t[5], t[7], t[1])

def p_tamano_matriz(t):
    '''tamano_matriz : tamano_matriz CORIZQ CORDER
                    | CORIZQ CORDER'''

    dimension = 0
    if len(t) > 3:
        dimension = int(t[1]) + 1
    else:
        dimension += 1 
    t[0] = dimension

def p_list_valores(t):
    '''list_valores : CORIZQ list_valores2 CORDER'''
    t[0] = t[2]

def p_list_valores2(t):
    '''list_valores2 : list_valores2 COMA CORIZQ arg CORDER
                    | CORIZQ arg CORDER'''
    arr = []
    if len(t) > 4:
        arr = t[1] + [t[4]]
        t[0] = t[1]
    else:
        arr.append(t[2])
    t[0] = arr
        
    

def p_args(t):
    '''arg : list_valores2
            | expresiones'''
    t[0] = t[1]


def p_array_push(t):
    '''instruccion : IDENTIFICADOR PUNTO RES_PUSH PARIZQ expresion PARDER PUNTOCOMA'''
    params = get_params(t)
    t[0] = Push_Array(params.line, params.column, t[1], t[5])

def p_array_asignation_matriz(t):
    '''instruccion : IDENTIFICADOR index_matriz IGUAL expresion PUNTOCOMA'''
    params = get_params(t)
    if len(t[2]) == 1:
        t[0] = Asignation_Array(params.line, params.column, t[1], t[2], t[4])
    elif len(t[2]) > 1:
        t[0] = Asignacion_Matriz(params.line, params.column, t[1], t[2], t[4])

#INTERFACE
def p_interface_definition(t):
    '''definition_interface : INTERFACE IDENTIFICADOR LLAVEIZQ atributos_list LLAVEDER'''
    params = get_params(t)
    t[0] = Definition_Interface(params.line, params.column, t[2], t[4])

def p_interface_atributos(t):
    '''atributos_list : atributos_list IDENTIFICADOR DOSPUNTOS tipos_interface PUNTOCOMA
                    | IDENTIFICADOR DOSPUNTOS tipos_interface PUNTOCOMA'''

    arr = {}
    arr2 = {}
    if len(t) > 5:
        arr = t[1]
        arr2[t[2]] = t[4]
        arr.update(arr2)
    else:
        arr[t[1]] = t[3]
    t[0] = arr

def p_tipos_interface(t):
    '''tipos_interface : RES_STRING
                        | RES_NUMBER
                        | RES_FLOAT
                        | RES_CHAR
                        | RES_BOOLEAN
                        | IDENTIFICADOR '''
    t[0] = t[1]

def p_interface_declaration(t):
    '''declaration_interface : VAR IDENTIFICADOR DOSPUNTOS IDENTIFICADOR IGUAL LLAVEIZQ atributos_insta LLAVEDER PUNTOCOMA
                            | CONST IDENTIFICADOR DOSPUNTOS IDENTIFICADOR IGUAL LLAVEIZQ atributos_insta LLAVEDER PUNTOCOMA'''
    params = get_params(t)
    if t[1] == "var":
        t[0] = Declaration_Interface(params.line, params.column, t[2], t[4], t[7], "var")
    elif t[1] == "const":
        t[0] = Declaration_Interface(params.line, params.column, t[2], t[4], t[7], "const")

def p_intanciacion_atributos(t):
    '''atributos_insta : atributos_insta COMA IDENTIFICADOR DOSPUNTOS expresion
                        | IDENTIFICADOR DOSPUNTOS expresion'''
    
    arr = {}
    arr2 = {}
    if len(t) > 5:
        arr = t[1]
        arr2[t[3]] = t[5]
        arr.update(arr2)
    else:
        arr[t[1]] = t[3]
    t[0] = arr
    
def p_asignation_interface(t):
    '''instruccion : IDENTIFICADOR PUNTO atributos_anidados IGUAL expresion PUNTOCOMA'''
    params = get_params(t)
    t[0] = Asignacion_Interface(params.line, params.column, t[1], t[3], t[5])


#-------------------------------------------------------------EXPRESIONES--------------------------------------------------------------------
def p_expresiones_lista(t):
    '''expresiones : expresiones COMA expresion
                | expresion '''
    
    arr = []
    if len(t) > 2:
        arr = t[1] + [t[3]]
        t[0] = t[1]
    else:
        arr.append(t[1])
    t[0] = arr

def p_suma(t):
    'expresion : expresion MAS expresion'
    params = get_params(t)
    t[0] = Aritmetica(params.line, params.column, t[1], t[3], "+")

def p_resta(t):
    'expresion : expresion MENOS expresion'
    params = get_params(t)
    t[0] = Aritmetica(params.line, params.column, t[1], t[3], "-")

def p_mult(t):
    'expresion : expresion MULT expresion'
    params = get_params(t)
    t[0] = Aritmetica(params.line, params.column, t[1], t[3], "*")

def p_div(t):
    'expresion : expresion DIV expresion'
    params = get_params(t)
    t[0] = Aritmetica(params.line, params.column, t[1], t[3], "/")

def p_mod(t):
    'expresion : expresion MOD expresion'
    params = get_params(t)
    t[0] = Aritmetica(params.line, params.column, t[1], t[3], "%")

def p_exp_unaria(t):
    'expresion : MENOS expresion %prec UNMENOS'
    params = get_params(t)
    t[0] = Aritmetica(params.line, params.column, t[2], t[2], 'umenos')


def p_parentesis(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_accedervar(t):
    'expresion : IDENTIFICADOR'
    params = get_params(t)
    t[0] = Accedervar(params.line, params.column, t[1])

def p_comparation1(t):
    'expresion : expresion IGUALDAD expresion'
    params = get_params(t)
    t[0] = Comparation(params.line, params.column, t[1], t[3], "igualdad")

def p_comparation2(t):
    'expresion : expresion DESIGUALDAD expresion'
    params = get_params(t)
    t[0] = Comparation(params.line, params.column, t[1], t[3], "noigual")

def p_relacional1(t):
    'expresion : expresion MAYOR expresion'
    params = get_params(t)
    t[0] = Relacionales(params.line, params.column, t[1], t[3], ">")

def p_relacional2(t):
    'expresion : expresion MAYORIGUAL expresion'
    params = get_params(t)
    t[0] = Relacionales(params.line, params.column, t[1], t[3], ">=")

def p_relacional3(t):
    'expresion : expresion MENOR expresion'
    params = get_params(t)
    t[0] = Relacionales(params.line, params.column, t[1], t[3], "<")

def p_relacional4(t):
    'expresion : expresion MENORIGUAL expresion'
    params = get_params(t)
    t[0] = Relacionales(params.line, params.column, t[1], t[3], "<=")

def p_logicas1(t):
    'expresion : expresion AND expresion'
    params = get_params(t)
    t[0] = Logicas(params.line, params.column, t[1], t[3], "and")

def p_logica2(t):
    'expresion : expresion OR expresion'
    params = get_params(t)
    t[0] = Logicas(params.line, params.column, t[1], t[3], "or")

def p_logicas(t):
    'expresion : NOT expresion'
    params = get_params(t)
    t[0] = Logicas(params.line, params.column, t[2], t[2], "not")
    

def p_primitiva(t):
    '''expresion : NUMBER
                | CADENA
                | FLOAT
                | CHAR
                | BOOL'''
    t[0] = t[1]

def p_tipo(t):
    '''tipo : RES_STRING
            | RES_NUMBER
            | RES_FLOAT
            | RES_CHAR
            | RES_BOOLEAN'''
    t[0] = t[1]


def p_callfuncion_expresion(t):
    '''expresion : IDENTIFICADOR PARIZQ expresiones PARDER
                    | IDENTIFICADOR PARIZQ PARDER '''
    params = get_params(t)
    if len(t) == 5:
        t[0] = CallFunction(params.line, params.column, t[1], t[3])
    elif len(t) == 4:
        t[0] = CallFunction(params.line, params.column, t[1], None)

def p_ternario(t):
    '''expresion : expresion INTER expresion DOSPUNTOS expresion '''
    params = get_params(t)
    t[0] = Ternario(params.line, params.column, t[1], t[3], t[5])

#FUNCIONES EMBEBIDAS
def p_parseint(t):
    '''expresion : RES_PARSEINT PARIZQ expresion PARDER'''
    params = get_params(t)
    t[0] = ParseInt(params.line, params.column, t[3])

def p_parsefloat(t):
    '''expresion : RES_PARSEFLOAT PARIZQ expresion PARDER'''
    params = get_params(t)
    t[0] = ParseFloat(params.line, params.column, t[3])

def p_tostring(t):
    '''expresion : expresion PUNTO RES_TOSTRING PARIZQ PARDER'''
    params = get_params(t)
    t[0] = ToString(params.line, params.column, t[1])

def p_tolower(t):
    '''expresion : expresion PUNTO RES_TOLOWER PARIZQ PARDER'''
    params = get_params(t)
    t[0] = ToLowerCase(params.line, params.column, t[1])

def p_toupper(t):
    '''expresion : expresion PUNTO RES_TOUPPER PARIZQ PARDER'''
    params = get_params(t)
    t[0] = ToUpperCase(params.line, params.column, t[1])

def p_typeof(t):
    '''expresion : RES_TYPEOF expresion'''
    params = get_params(t)
    t[0] = TypeOf(params.line, params.column, t[2])

#ARRAYS
def p_array(t):
    '''array : CORIZQ expresiones CORDER
            | CORIZQ CORDER
            | expresion
            | list_valores'''
    params = get_params(t)
    if len(t) == 4:
        t[0] = Array_expresion(params.line, params.column, t[2])
    elif len(t) == 3:
        t[0] = Array_expresion(params.line, params.column, None)
    elif len(t) == 2:
        t[0] = t[1]

def p_accederarray_matriz(t):
    '''expresion : expresion index_matriz'''
    params = get_params(t)
    if len(t[2]) == 1:
        t[0] = AccederArray(params.line, params.column, t[1], t[2])
    elif len(t[2]) > 1:
        t[0] = AccederMatriz(params.line, params.column, t[1], t[2])

def p_index_matriz(t):
    '''index_matriz : index_matriz CORIZQ expresion CORDER
                    | CORIZQ expresion CORDER'''
    arr = []
    if len(t)>4:
        arr = t[1] + [t[3]]
        t[0] = t[1]
    else:
        arr.append(t[2])
    t[0] = arr


def p_array_function(t):
    '''expresion : expresion PUNTO RES_POP PARIZQ PARDER
                | expresion PUNTO RES_INDEXOF PARIZQ expresion PARDER
                | expresion PUNTO RES_JOIN PARIZQ PARDER
                | expresion PUNTO RES_LENGTH '''
    params = get_params(t)
    if t[3] == "pop":
        t[0] = Array_Function(params.line, params.column, t[1], "pop", None)
    elif t[3] == "indexOf":
        t[0] = Array_Function(params.line, params.column, t[1], "indexof", t[5])
    elif t[3] == "join":
        t[0] = Array_Function(params.line, params.column, t[1], "join", None)
    elif t[3] == "length":
        t[0] = Array_Function(params.line, params.column, t[1], "length", None)


#INTERFACE
def p_acceder_interface(t):
    '''expresion : expresion PUNTO atributos_anidados'''
    params = get_params(t)
    t[0] = AccederInterface(params.line, params.column, t[1], t[3])


def p_atributos_anidados(t):
    '''atributos_anidados : atributos_anidados PUNTO IDENTIFICADOR
                        | IDENTIFICADOR'''
    
    arr = []
    if len(t) > 3:
        arr = t[1] + [t[3]]
        t[0] = t[1]
    else:
        arr.append(t[1])
    t[0] = arr

def p_interface_function(t):
    '''expresion : RES_OBJECT PUNTO RES_KEYS PARIZQ expresion PARDER
                | RES_OBJECT PUNTO RES_VALUES PARIZQ expresion PARDER'''
    params = get_params(t)
    if t[3] == "keys":
        t[0] = Interface_Function(params.line, params.column, t[5], t[3])
    elif t[3] == "values":
        t[0] = Interface_Function(params.line, params.column, t[5], t[3])



#ERRORES
def p_error(p):
    if p:
        print(f"Error de sintaxis en línea {p.lineno}, columna {p.lexpos}: Token inesperado '{p.value}'")
        descripcion = f"Error de sintaxis en línea {p.lineno}, columna {p.lexpos}: Token inesperado '{p.value}'"
        error = {
            "descripcion": descripcion,
            "ambito": "global",
            "linea": p.lineno,
            "column": p.lexpos,
            "tipo": "sintactico"
        }
        errores.append(error)
    else:
        
        print("Error de sintaxis")
        descripcion = "Error de sintaxis"
        error = {
            "descripcion": descripcion,
            "ambito": "global",
            "linea": "",
            "column": "",
            "tipo": "sintactico"
        }
        errores.append(error)


def get_params(t):
    line = t.lexer.lineno
    lexpos = t.lexpos if isinstance(t.lexpos, int) else 0
    column = lexpos - t.lexer.lexdata.rfind('\n', 0, lexpos)
    return codeParams(line,column)





class Parser:
    def __init__(self):
        pass

    def interpretar(self, input):
        lexer = Lex.lex()
        parser = yacc.yacc()
        result = parser.parse(input)
        return result


    def lexical(self, input):
        lexer = Lex.lex()
    
        lexer.input(input)
        for token in lexer:
            print(token)


    def getErrors(self):
        global errores 
        err = errores
        errores = []
        return err

