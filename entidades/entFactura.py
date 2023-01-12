class eFactura:
    
    def __init__(self):
        self.__idfactura = ""
        self.__nofactura = ""
        self.__usuario = ""
        self.__cliente = ""
        self.__fichacliente = ""
        self.__fecha = ""
        self.__totalfactura = ""
        self.__estado = ""
        self.__nota = ""
        self.__moneda = ""
        
    def setIdFactura(self, idfactura):
        self.__idfactura = idfactura

    def setNoFactura(self, nofactura):
        self.__nofactura = nofactura

    def setUsuario(self, usuario):
        self.__usuario = usuario

    def setCliente(self, cliente):
        self.__cliente = cliente

    def setFichaCliente(self, fichacliente):
        self.__fichacliente = fichacliente

    def setFecha(self, fecha):
        self.__fecha = fecha

    def setTotalFactura(self, totalfactura):
        self.__totalfactura = totalfactura

    def setEstado(self, estado):
        self.__estado = estado
        
    def setNota(self, nota):
        self.__nota = nota
        
    def setMoneda(self, moneda):
        self.__moneda = moneda


    def getIdFactura(self):
        return self.__idfactura

    def getNoFactura(self):
        return self.__nofactura
        
    def getUsuario(self):
        return self.__usuario

    def getCliente(self):
        return self.__cliente

    def getFichaCliente(self):
        return self.__fichacliente

    def getFecha(self):
        return self.__fecha

    def getTotalFactura(self):
        return self.__totalfactura

    def getEstado(self):
        return self.__estado

    def getNota(self):
        return self.__nota

    def getMoneda(self):
        return self.__moneda

