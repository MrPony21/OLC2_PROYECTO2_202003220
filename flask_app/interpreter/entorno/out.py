

class Out():
    def __init__(self):
        self.console = ""
        self.errores = []
        self.tabla_simbolos = []

    def addConsole(self, cadena):
        self.console += cadena+ "\n"

    def addErrores(self, descripcion, ambito, linea, columna, tipo):
        json_error = {
            "descripcion": descripcion,
            "ambito": ambito,
            "linea": linea,
            "column": columna,
            "tipo": tipo
        }
        self.errores.append(json_error)

    def add_tabla_simbolos(self, json_tabla):

        if json_tabla in self.tabla_simbolos:
            return

        self.tabla_simbolos.append(json_tabla)