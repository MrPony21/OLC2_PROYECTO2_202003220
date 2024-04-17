from abc import ABC, abstractmethod

class Instruccion(ABC):

    @abstractmethod
    def ejecutar(self, out, env):
        pass

    def generateASM(self, out, env, generator):
        pass