class eInventario:
    
    def __init__(self):
        self.__idinventario = ""
        self.__recepcion = ""
        self.__noinventario = ""
        self.__observaciones = ""
        self.__equipo = ""
        self.__marca = ""
        self.__modelo = ""
        self.__activo = ""
        self.__cantidad = ""

    def setIdInventario(self, idinventario):
        self.__idinventario = idinventario

    def setRecepcion(self, recepcion):
        self.__recepcion = recepcion

    def setNoInventario(self, noinventario):
        self.__noinventario = noinventario

    def setObservaciones(self, observaciones):
        self.__observaciones = observaciones

    def setEquipo(self, equipo):    
        self.__equipo = equipo

    def setMarca(self, marca):    
        self.__marca = marca

    def setModelo(self, modelo):    
        self.__modelo = modelo

    def setActivo(self, activo):
        self.__activo = activo

    def setCantidad(self, cantidad):
        self.__cantidad = cantidad

    def getIdInventario(self):
        return self.__idinventario
    
    def getRecepcion(self):
        return self.__recepcion

    def getNoInventario(self):
        return self.__noinventario

    def getObservaciones(self):
        return self.__observaciones
    
    def getEquipo(self):
        return self.__equipo

    def getMarca(self):    
        return self.__marca

    def getModelo(self):    
        return self.__modelo
    
    def getActivo(self):
        return self.__activo
    
    def getCantidad(self):
        return self.__cantidad
