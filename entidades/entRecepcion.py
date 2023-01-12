class eRecepcion:
    
    def __init__(self):
        self.__idrecepcion = ""
        self.__norecepcion = ""
        self.__usuario = ""
        self.__cliente = ""
        self.__fecha = ""
        self.__estado = ""

    def setIdRecepcion(self, idrecepcion):
        self.__idrecepcion = idrecepcion

    def setNoRecepcion(self, norecepcion):
        self.__norecepcion = norecepcion

    def setUsuario(self, usuario):
        self.__usuario = usuario

    def setCliente(self, cliente):
        self.__cliente = cliente

    def setFecha(self, fecha):
        self.__fecha = fecha

    def setEstado(self, estado):
        self.__estado = estado


    def getIdRecepcion(self):
        return self.__idrecepcion

    def getNoRecepcion(self):
        return self.__norecepcion
        
    def getUsuario(self):
        return self.__usuario

    def getCliente(self):
        return self.__cliente

    def getFecha(self):
        return self.__fecha

    def getEstado(self):
        return self.__estado

