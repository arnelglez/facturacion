class eFacturaDesglose:
    
    def __init__(self):
        self.__idfacdesglose = ""
        self.__factura = ""
        self.__tipo = ""
        self.__servicio = ""
        self.__inventario = ""
        self.__cantidad = ""
        self.__precio = ""
        self.__preciototal = ""

    def setIdFacturaDesglose(self, idfacdesglose):
        self.__idfacdesglose = idfacdesglose

    def setFactura(self, factura):
        self.__factura = factura

    def setTipo(self, tipo):
        self.__tipo = tipo

    def setServicio(self, servicio):
        self.__servicio = servicio

    def setInventario(self, inventario):
        self.__inventario = inventario

    def setCantidad(self, cantidad):
        self.__cantidad = cantidad

    def setPrecio(self, precio):
        self.__precio = precio

    def setPrecioTotal(self, preciototal):
        self.__preciototal = preciototal


    def getIdFacturaDesglose(self):
        return self.__idfacdesglose
        
    def getFactura(self):
        return self.__factura
        
    def getTipo(self):
        return self.__tipo

    def getServicio(self):
        return self.__servicio

    def getInventario(self):
        return self.__inventario

    def getCantidad(self):
        return self.__cantidad

    def getPrecio(self):
        return self.__precio

    def getPrecioTotal(self):
        return self.__preciototal