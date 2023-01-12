
class eAnticipo:

    def __init__(self):

        self.__idanticipo = ""
        self.__cobrofactura = ""
        self.__usuario = ""
        self.__cliente = ""
        self.__noanticipo = ""
        self.__fecha = ""
        self.__documento = ""
        self.__fechaemision = ""
        self.__factura = ""
        self.__monto = ""
        self.__estado = ""

    def setIdAnticipo(self, idanticipo):
        self.__idanticipo = idanticipo

    def setCobroFactura(self, cobrofactura):
        self.__cobrofactura = cobrofactura

    def setUsuario(self, usuario):
        self.__usuario = usuario

    def setCliente(self, cliente):
        self.__cliente = cliente

    def setNoAnticipo(self, noanticipo):
        self.__noanticipo = noanticipo

    def setFecha(self, fecha):
        self.__fecha = fecha

    def setDocumento(self, documento):
        self.__documento = documento

    def setFechaEmision(self, fechaemision):
        self.__fechaemision = fechaemision

    def setFactura(self, factura):
        self.__factura = factura

    def setMonto(self, monto):
        self.__monto = monto

    def setEstado(self, estado):
        self.__estado = estado


    def getIdAnticipo(self):
        return self.__idanticipo

    def getCobroFactura(self):
        return self.__cobrofactura

    def getUsuario(self):
        return self.__usuario

    def getCliente(self):
        return self.__cliente

    def getNoAnticipo(self):
        return self.__noanticipo

    def getFecha(self):
        return self.__fecha

    def getDocumento(self):
        return self.__documento

    def getFechaEmision(self):
        return self.__fechaemision

    def getFactura(self):
        return self.__factura

    def getMonto(self):
        return self.__monto

    def getEstado(self):
        return self.__estado