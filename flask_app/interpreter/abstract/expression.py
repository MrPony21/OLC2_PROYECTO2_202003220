from abc import ABC, abstractmethod

class Expression(ABC):

    @abstractmethod
    def ejecutar(self, out, env):
        pass

    @abstractmethod
    def generateASM(self, out, env, generator):
        pass