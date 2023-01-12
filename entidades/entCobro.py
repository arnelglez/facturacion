class eCobro:
    
    def __init__(self):
        self.__idcobro = ""
        self.__nocobro = ""
        self.__usuario = ""
        self.__cliente = ""
        self.__fecha = ""
        self.__totalcobro = ""
        self.__tipopago = ""
        self.__documento = ""
        self.__estado = ""
        self.__fechaemision = ""

    def setIdCobro(self, idcobro):
        self.__idcobro = idcobro

    def setNoCobro(self, nocobro):
        self.__nocobro = nocobro

    def setUsuario(self, usuario):
        self.__usuario = usuario

    def setCliente(self, cliente):
        self.__cliente = cliente

    def setFecha(self, fecha):
        self.__fecha = fecha

    def setTotalCobro(self, totalcobro):
        self.__totalcobro = totalcobro

    def setTipoPago(self, tipopago):
        self.__tipopago = tipopago

    def setDocumento(self, documento):
        self.__documento = documento

    def setEstado(self, estado):
        self.__estado = estado

    def setFechaEmision(self, fechaemision):
        self.__fechaemision = fechaemision


    def getIdCobro(self):
        return self.__idcobro

    def getNoCobro(self):
        return self.__nocobro
        
    def getUsuario(self):
        return self.__usuario

    def getCliente(self):
        return self.__cliente

    def getFecha(self):
        return self.__fecha

    def getTotalCobro(self):
        return self.__totalcobro

    def getTipoPago(self):
        return self.__tipopago 

    def getDocumento(self):
        return self.__documento

    def getEstado(self):
        return self.__estado

    def getFechaEmision(self):
        return self.__fechaemision

