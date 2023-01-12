class eTaller:

    def __init__(self):
        self.__idtaller = ""
        self.__nombre = "Control de Talleres"
        self.__direccion = ""
        self.__cuenta = ""
        self.__cuentaMLC = ""
        self.__sucursal = ""
        self.__logo = "../img/Taller.jpeg"
        self.__licencia = ""

    def setIdTaller(self, idtaller):
        self.__idtaller = idtaller

    def setNombre(self, nombre):
        self.__nombre = nombre

    def setDireccion(self, direccion):
        self.__direccion = direccion

    def setCuenta(self, cuenta):
        self.__cuenta = cuenta

    def setCuentaMLC(self, cuentaMLC):
        self.__cuentaMLC = cuentaMLC

    def setSucursal(self, sucursal):
        self.__sucursal = sucursal

    def setLogo(self, logo):
        self.__logo = logo

    def setLicencia(self, licencia):
        self.__licencia = licencia


    def getIdTaller(self):
        return self.__idtaller
        
    def getNombre(self):
        return self.__nombre

    def getDireccion(self):
        return self.__direccion

    def getCuenta(self):
        return self.__cuenta
    
    def getCuentaMLC(self):
        return self.__cuentaMLC

    def getSucursal(self):
        return self.__sucursal

    def getLogo(self):
        return self.__logo

    def getLicencia(self):
        return self.__licencia
