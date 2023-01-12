class eTipoPago:
    
    def __init__(self):
        self.__idtipopago = ""
        self.__descripcion = ""
        self.__activo = ""

    def setIdTipoPago(self, idtipopago):
        self.__idtipopago = idtipopago

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion

    def setActivo(self, activo):
        self.__activo = activo

 
    def getIdTipoPago(self):
        return self.__idtipopago
        
    def getDescripcion(self):
        return self.__descripcion

    def getActivo(self):
        return self.__activo

   