
class eCliente:

    def __init__(self):
        self.__idcliente = ""
        self.__nombre = ""
        self.__contrato = ""
        self.__direccion = ""
        self.__cuenta = ""
        self.__activo = ""

    def setIdCliente(self, idcliente):
        self.__idcliente = idcliente

    def setNombre(self, nombre):
        self.__nombre = nombre

    def setContrato(self, contrato):
        self.__contrato = contrato

    def setDireccion(self, direccion):
        self.__direccion = direccion

    def setCuenta(self, cuenta):
        self.__cuenta = cuenta

    def setActivo(self, activo):
        self.__activo = activo


    def getIdCliente(self):
        return self.__idcliente
        
    def getNombre(self):
        return self.__nombre

    def getContrato(self):
        return self.__contrato

    def getDireccion(self):
        return self.__direccion

    def getCuenta(self):
        return self.__cuenta

    def getActivo(self):
        return self.__activo

