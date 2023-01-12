class eFichaCliente:
    
    def __init__(self):
        self.__idfichacliente = ""
        self.__nombre = ""
        self.__apellidos = ""
        self.__carnet = ""
        self.__cargo = ""
        self.__cliente = ""
        self.__activo = ""

    def setIdFichaCliente(self, idfichacliente):
        self.__idfichacliente = idfichacliente

    def setNombre(self, nombre):
        self.__nombre = nombre

    def setApellidos(self, apellidos):
        self.__apellidos = apellidos

    def setCarnet(self, carnet):
        self.__carnet = carnet

    def setCargo(self, cargo):
        self.__cargo = cargo
    
    def setCliente(self, cliente):
        self.__cliente = cliente

    def setActivo(self, activo):
        self.__activo = activo


    def getIdFichaCliente(self):
        return self.__idfichacliente
        
    def getNombre(self):
        return self.__nombre

    def getApellidos(self):
        return self.__apellidos

    def getCarnet(self):
        return self.__carnet

    def getCargo(self):
        return self.__cargo

    def getCliente(self):
        return self.__cliente

    def getActivo(self):
        return self.__activo