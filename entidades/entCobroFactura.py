class eCobroFactura:

    def __init__(self):
        self.__idcobrofactura = ""
        self.__cobro = ""
        self.__tipo = ""
        self.__factura = ""
        self.__monto = ""

    def setIdCobroFactura(self, idcobrofactura):
        self.__idcobrofactura = idcobrofactura

    def setCobro(self, cobro):
        self.__cobro = cobro

    def setTipo(self, tipo):
        self.__tipo = tipo

    def setFactura(self, factura):
        self.__factura = factura

    def setMonto(self, monto):
        self.__monto= monto


    def getIdCobroFactura(self):
        return self.__idcobrofactura 

    def getCobro(self):
        return self.__cobro 

    def getTipo(self):
        return self.__tipo 

    def getFactura(self):
        return self.__factura

    def getMonto(self):
        return self.__monto
