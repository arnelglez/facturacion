class eDuenno:
    
    def __init__(self):
        self.__idduenno = ""
        self.__nombre = ""
        self.__apellidos = ""
        self.__telefono = ""
        self.__carnet = ""
        self.__licencia = ""

    def setIdDuenno(self, idduenno):
        self.__idduenno = idduenno

    def setNombre(self, nombre):
        self.__nombre = nombre

    def setApellidos(self, apellidos):
        self.__apellidos = apellidos

    def setTelefono(self, telefono):
        self.__telefono = telefono

    def setCarnet(self, carnet):
        self.__carnet = carnet

    def setLicencia(self, licencia):
        self.__licencia = licencia


    def getIdDuenno(self):
        return self.__idduenno
        
    def getNombre(self):
        return self.__nombre

    def getApellidos(self):
        return self.__apellidos

    def getTelefono(self):
        return self.__telefono

    def getCarnet(self):
        return self.__carnet

    def getLicencia(self):
        return self.__licencia

