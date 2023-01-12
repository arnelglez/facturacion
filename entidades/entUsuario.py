class eUsuario:
    
    def __init__(self):
        self.__idusuario = ""
        self.__username = ""
        self.__passwd = ""
        self.__carnet = ""
        self.__nombre = ""
        self.__apellidos = ""
        self.__activo = ""

    def setIdUsuario(self, idusuario):
        self.__idusuario = idusuario

    def setUsername(self, username):
        self.__username = username

    def setPasswd(self, passwd):
        self.__passwd = passwd

    def setCarnet(self, carnet):
        self.__carnet = carnet

    def setNombre(self, nombre):    
        self.__nombre = nombre

    def setApellidos(self, apellidos):
        self.__apellidos = apellidos

    def setActivo(self, activo):
        self.__activo = activo

    def getIdUsuario(self):
        return self.__idusuario
    
    def getUsername(self):
        return self.__username

    def getPasswd(self):
        return self.__passwd

    def getCarnet(self):
        return self.__carnet
    
    def getNombre(self):
        return self.__nombre
    
    def getApellidos(self):
        return self.__apellidos

    def getActivo(self):
        return self.__activo